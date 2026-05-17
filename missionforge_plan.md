# MissionForge

## Measurable Refactor Missions for IBM Bob

MissionForge is a deterministic CLI harness plus Bob Skill that turns refactor and modernization work into scoped, measurable, reviewable missions. Bob does the reasoning and code work. MissionForge manages the mission contract: scope boundaries, baseline-to-target metrics, validation gates, and evidence reports.

**Tagline:** Give Bob a map, a mission, and a validation gate.

---

## 1. Positioning

### What MissionForge Is

A harness, not a plugin. MissionForge runs as a standalone CLI any developer can use from their terminal. A thin Bob Skill teaches Bob how to drive it. There is no server to configure, no transport layer to debug, and no AI-tool lock-in. If you uninstall Bob tomorrow, MissionForge still works.

That last property is the differentiator. Most hackathon entries build tools that only work *because* Bob exists. MissionForge works regardless and gets *better* with Bob.

### What MissionForge Is Not

| Misconception | Correction |
|---|---|
| The CLI measures code | No. Bob measures code. The CLI manages mission state. |
| The CLI is language-aware | No. The CLI is language-agnostic by construction. It never reads source files. |
| It replaces Bob's reasoning | No. Bob writes goals, missions, measurements, implementation, and explanations. |
| It is a code-intelligence tool | No. It is a mission-accounting tool. |

### Core Principle

**Bob measures the code. MissionForge measures the mission.**

The CLI handles file paths, git operations, JSON state, schema validation, test command execution, and report templating. Bob handles everything that requires understanding code.

---

## 2. Why This Matters for Bob

### The Token Waste Problem

In a normal refactor session, Bob typically:

1. Reads several files broadly to understand the codebase
2. Plans the refactor
3. Re-reads some of those files while implementing
4. Runs grep/find to verify scope
5. Re-reads files again to check work
6. Generates a summary, possibly re-reading to confirm

The same files enter context two or three times each. The waste is not the initial exploration. Bob has to explore once. The waste is the *re-exploration* because Bob has no stable place to store what it learned.

### How the Harness Saves Tokens

MissionForge saves tokens not by doing measurement, but by giving Bob a structured place to record findings once and reference them by ID afterward.

**Save 1: Persistent mission state means no re-discovery.** When Bob writes the mission file with allowed paths, forbidden paths, and metric definitions, those become durable facts. Bob references the mission file later instead of re-reading source.

**Save 2: Baseline values are recorded once and never re-measured.** Bob measures a baseline once and writes it to disk. When validating, the CLI reads from disk. Bob does not recount.

**Save 3: The CLI handles cheap deterministic operations.** Things like *which files did I change* (git diff), *are any of those forbidden* (set intersection), *did tests pass* (exit code), and *what does the report look like* (template rendering) all happen in the CLI with zero token cost.

**Save 4: Structured prompts focus Bob's reads.** When Bob needs to measure a metric, the CLI gives Bob a narrow prompt with scope. Compare to Bob freely exploring "let me understand the coupling situation" — same information, far fewer tokens.

**Save 5: The mission file is Bob's compressed context.** A few hundred tokens of mission YAML replaces thousands of tokens of raw file reads in subsequent turns.

---

## 3. Architecture

Four components. No MCP server, no transport layer between Bob and the CLI, no schema duplication. The web UI is a downstream view of CLI state, not a parallel writer.

```
                  MissionForge Skill (SKILL.md)
                          │  teaches Bob the workflow
                          ▼
                  MissionForge Slash Commands
                          │  ergonomic shortcuts: /mf-init, /mf-mission, /mf-baseline,
                          │  /mf-validate, /mf-report
                          ▼
                  MissionForge CLI
                          │  the harness, deterministic and language-agnostic
                          ▼
                  .missionforge/ workspace
                          │  mission files, baseline state, validation results,
                          │  evidence reports
                          ▲
                          │  reads state, renders visualization
                  ┌───────┴──────────────┐
                  │                      │
                  ▼                      ▼
        MissionForge Board (web UI)   watsonx.ai
        ───────────────────────    ─────────────────────
        Kanban view, mission       Mission Chat sidebar,
        detail, evidence reports   Stakeholder Translation
```

### Architectural Hierarchy

The CLI is the source of truth. Everything else reads from or writes through it.

- **Bob writes mission state via the CLI.** Bob does not write to `.missionforge/` directly — it always goes through CLI commands. This keeps schema validation and state transitions in one place.
- **The Board reads mission state from the CLI.** It can trigger CLI commands (clicking "approve" runs a CLI command) but never mutates state files directly.
- **Watsonx.ai reads mission state through the Board's backend.** It is a runtime synthesis layer over structured data the CLI produced. It does not read source code.

This preserves the harness identity: someone using the CLI alone, from a terminal, sees the same state the Board shows. They are two views of the same underlying truth. If you turned off the Board tomorrow, MissionForge would still work end-to-end from the command line.

### What the CLI Touches

- File paths and globs
- Git operations (diff, status)
- JSON and YAML files
- Schema validation
- Shell command execution (user-provided test commands)
- Markdown templating

### What the CLI Never Touches

- Source code semantics
- Symbol resolution
- Import graphs
- Pattern matching against code content
- Anything language-specific

### Workspace Layout

```
.missionforge/
├── config.yaml
├── missions/
│   └── MF-001/
│       ├── mission.yaml          # user writes: goal, forbidden_paths, aggregate_metrics
│       ├── plan.yaml             # CLI writes after decompose: dep graph + execution order
│       ├── sub-missions/
│       │   ├── MF-001-A/
│       │   │   ├── sub-mission.yaml      # Bob writes during decompose
│       │   │   ├── baseline.todo.json    # CLI writes, Bob fills
│       │   │   ├── baseline.json         # immutable after commit
│       │   │   ├── validation.todo.json  # CLI writes, Bob fills
│       │   │   └── validation.json       # final result
│       │   ├── MF-001-B/                 # same structure
│       │   ├── MF-001-C/                 # same structure
│       │   └── MF-001-D/                 # same structure
│       └── report.md             # aggregate parent report, CLI templates this
```

The parent `mission.yaml` contains the goal, forbidden paths, and aggregate metrics. It does not contain sub-mission definitions — those live in the `sub-missions/` directory, each in their own folder. The `plan.yaml` is the CLI's computed artifact: the validated dependency graph and topological execution order. Bob writes sub-mission YAMLs during the decompose step; the CLI validates and resolves them.

---

## 4. The Mission Contract

A mission is decomposable. Every mission has a parent definition (goal, aggregate metrics, forbidden paths) and one or more sub-missions. Each sub-mission defines its own scope, its own metrics, and its dependencies on other sub-missions. The CLI builds a dependency graph from these declarations.

The decomposition is what enables MissionForge to scale. A single large refactor becomes a structured set of smaller, independently-validated units of work. Reviewers can approve sub-missions independently. Failed sub-missions can be retried without restarting the parent. The architecture supports parallel execution in future phases without changing the contract.

### Parent Mission File

```yaml
# mission.yaml

id: MF-001
goal: |
  Modernize matchmaking from CORBA to REST while preserving
  multiplayer functionality across both the Java Swing client
  and the Python TUI client. All other CORBA flows (gameplay,
  scoring, session management) must remain untouched and working.

# Forbidden paths apply to ALL sub-missions. This is the safety
# boundary no sub-mission can override.
forbidden_paths:
  - server/src/game/**
  - server/src/scoring/**
  - server/src/session/**
  - idl/Game.idl
  - idl/Scoring.idl

# Aggregate metrics describe the final state across all sub-missions.
# Validation of the parent checks these in addition to every
# sub-mission passing its own validation.
aggregate_metrics:
  - id: corba_refs_in_matchmaking
    description: |
      Count of CORBA imports and ORB references in the matchmaking
      module across the entire codebase.
    baseline_target: 7
    final_target: 0

  - id: in_game_corba_flow_still_works
    description: |
      Regression guard. Existing gameplay still flows through
      CORBA and the full-game integration test still passes.
    baseline_target: true
    final_target: true

# Parent-level test command. Sub-missions can override or add to it.
test_command: ./gradlew integrationTest && pytest tests/integration

# Reference to the sub-missions. The CLI reads these from the
# sub-missions/ directory and builds the dependency graph.
sub_missions:
  - MF-001-A
  - MF-001-B
  - MF-001-C
  - MF-001-D
```

### Sub-Mission Files

Each sub-mission has its own YAML file under `sub-missions/`. A sub-mission is a complete unit of work with scope, metrics, and dependencies.

```yaml
# sub-missions/MF-001-A/sub-mission.yaml

id: MF-001-A
parent: MF-001
title: Add REST endpoint for matchmaking
goal: |
  Add a REST endpoint that wraps the existing matchmaking CORBA
  service. The endpoint exposes the same operations as
  Matchmaking.idl. Do not modify the CORBA service itself —
  the REST endpoint should delegate to it for now. Clients will
  be migrated in subsequent sub-missions.

depends_on: []   # No dependencies. Can run first.

allowed_paths:
  - server/src/rest/MatchmakingEndpoint.java
  - server/src/matchmaking/MatchmakingService.java   # read-only for delegation

metrics:
  - id: rest_endpoint_exists
    description: |
      A REST endpoint exists at /api/matchmaking exposing all operations
      from Matchmaking.idl.
    baseline_target: false
    final_target: true

  - id: rest_endpoint_delegates_to_corba
    description: |
      The REST endpoint internally calls the existing CORBA matchmaking
      service rather than reimplementing the logic.
    baseline_target: false
    final_target: true

test_command: ./gradlew test --tests "*MatchmakingEndpointTest*"
```

```yaml
# sub-missions/MF-001-B/sub-mission.yaml

id: MF-001-B
parent: MF-001
title: Migrate Swing client to REST matchmaking
goal: |
  Update the Java Swing client to invoke the REST matchmaking
  endpoint instead of the CORBA stub. Remove the CORBA matchmaking
  imports from the client. Preserve all existing UX behavior.

depends_on: [MF-001-A]   # REST endpoint must exist first.

allowed_paths:
  - client-java/src/.../MatchmakingClient.java
  - client-java/src/.../RestClient.java   # may be created

metrics:
  - id: swing_uses_rest_for_matchmaking
    description: |
      The Java Swing client invokes matchmaking via HTTP to the
      REST endpoint rather than via CORBA stub calls.
    baseline_target: false
    final_target: true

  - id: corba_matchmaking_imports_in_swing
    description: |
      CORBA imports related to matchmaking removed from the Swing client.
    baseline_target: 3
    final_target: 0

test_command: ./gradlew test --tests "*MatchmakingClientTest*"
```

```yaml
# sub-missions/MF-001-C/sub-mission.yaml

id: MF-001-C
parent: MF-001
title: Migrate Python client to REST matchmaking
goal: |
  Update the Python TUI client to invoke the REST matchmaking
  endpoint instead of the CORBA stub. Preserve all existing UX.

depends_on: [MF-001-A]   # REST endpoint must exist first.
                          # Independent of MF-001-B (same dependency level).

allowed_paths:
  - client-python/src/matchmaking_client.py
  - client-python/src/rest_client.py   # may be created

metrics:
  - id: python_uses_rest_for_matchmaking
    description: |
      The Python TUI client invokes matchmaking via HTTP to the
      REST endpoint rather than via CORBA stub calls.
    baseline_target: false
    final_target: true

test_command: pytest tests/unit/test_matchmaking_client.py
```

```yaml
# sub-missions/MF-001-D/sub-mission.yaml

id: MF-001-D
parent: MF-001
title: Integration test for dual-client REST matchmaking
goal: |
  Write an integration test that confirms a Swing client and a
  Python TUI client can be matched together using the REST endpoint
  and proceed into a game.

depends_on: [MF-001-B, MF-001-C]   # Both clients must be migrated first.

allowed_paths:
  - tests/integration/matchmaking/test_dual_client_rest.py

metrics:
  - id: dual_client_test_exists
    description: |
      An integration test exists that exercises matchmaking with both
      client types via REST.
    baseline_target: false
    final_target: true

  - id: dual_client_test_passes
    description: |
      The integration test passes when run.
    baseline_target: false
    final_target: true

test_command: pytest tests/integration/matchmaking/test_dual_client_rest.py
```

### The Dependency Graph

The four sub-missions form this graph:

```
              MF-001-A
              (REST endpoint)
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
    MF-001-B             MF-001-C
    (Swing client)       (Python client)
        │                    │
        └─────────┬──────────┘
                  ▼
              MF-001-D
              (integration test)
```

MF-001-A has no dependencies and runs first. MF-001-B and MF-001-C both depend only on A, so once A completes they are *both ready to execute* — this is the latent parallelism. In Phase 1 they run sequentially. In Phase 3 (future work) they could run concurrently. MF-001-D depends on both B and C, so it waits for the diamond to close.

### Decomposition by Bob

Bob produces the sub-mission breakdown. The flow:

1. User writes the parent mission goal and forbidden paths
2. User runs `missionforge decompose MF-001`
3. Bob reads the codebase, reasons about how to break the work into independently-scoped sub-missions, and writes the sub-mission files
4. Bob writes a `plan.yaml` summarizing the decomposition and its rationale
5. User reviews the proposed decomposition
6. User approves (or asks Bob to revise) before any execution begins

The decomposition is a real reasoning task. Bob is using its understanding of the codebase to propose work units that have clean boundaries, minimal interdependencies, and clear ownership of metrics. This is one of the most visible and impressive things Bob does in the demo.

### Validation Aggregation

A parent mission passes if and only if:

1. Every sub-mission passes its own validation
2. The aggregate metrics meet their targets
3. No forbidden paths were touched in any sub-mission's diff
4. The parent-level test command passes (catches integration issues)

This catches the failure mode where every sub-mission looks good in isolation but the combined result has integration problems. The aggregate validation is the safety net.

---

## 5. Command Design

Commands operate on either parent missions or sub-missions. Sub-mission IDs follow the `MF-001-A` pattern. The CLI determines whether a given ID refers to a parent or a sub-mission from the directory structure.

### Parent-level Commands

| Command | Purpose | Touches |
|---|---|---|
| `missionforge init MF-001` | Creates `.missionforge/missions/MF-001/` with parent mission template | filesystem only |
| `missionforge mission MF-001 --validate` | Validates the parent mission YAML schema and path globs | YAML parsing |
| `missionforge decompose MF-001` | Bob runs this. Reads the codebase, writes sub-mission YAMLs and plan.yaml | Bob session + filesystem |
| `missionforge plan MF-001` | Validates the dependency graph (no cycles), computes topological order | YAML parsing |
| `missionforge next MF-001` | Reports which sub-missions are ready to execute (all dependencies satisfied) | JSON + dep graph |
| `missionforge validate MF-001` | Aggregate validation: all sub-missions passed AND aggregate metrics met | JSON only |
| `missionforge report MF-001` | Templates the aggregate evidence report from parent + all sub-mission states | templating |

### Sub-mission Commands

| Command | Purpose | Touches |
|---|---|---|
| `missionforge baseline MF-001-A --capture` | Writes baseline.todo.json for one sub-mission | JSON only |
| `missionforge baseline MF-001-A --commit` | Validates baseline complete, stamps to immutable baseline.json | JSON only |
| `missionforge validate MF-001-A --capture` | Runs git diff (scoped to sub-mission paths), test command, writes validation.todo.json | git + shell |
| `missionforge validate MF-001-A --commit` | Compares filled values against sub-mission targets, writes validation.json | JSON only |

Every command is deterministic, language-agnostic, and reads or writes JSON/YAML/Markdown only. None of them read source code.

### Two-Level Validation

Sub-mission validation checks one unit of work passed its own contract. Parent validation aggregates: every sub-mission must pass *and* the parent-level aggregate metrics must meet their targets *and* the parent's test command must pass. This two-level check is what catches integration issues that individual sub-missions cannot see.

---

## 6. The Full Workflow

The workflow has six phases. Decomposition is the new front-end phase. Baseline, implementation, and validation are now per-sub-mission and happen iteratively. Reporting aggregates everything at the parent level.

### Phase 1: Parent Mission Authoring

```
1. Developer runs:  missionforge init MF-001
   CLI: creates .missionforge/missions/MF-001/ with parent mission template
   Token cost: zero

2. User writes the parent mission.yaml
   User defines: goal prose, forbidden paths, aggregate metrics
   User does NOT write sub-missions — Bob will produce those
   Token cost: zero (user work, not Bob)

3. Developer runs:  missionforge mission MF-001 --validate
   CLI: validates parent YAML schema and forbidden-path globs
   Token cost: zero
```

### Phase 2: Decomposition by Bob

```
4. Developer runs:  missionforge decompose MF-001
   Bob explores the codebase, reasons about how to break the work
   into independently-scoped sub-missions with clean boundaries.
   Bob writes sub-mission YAML files under sub-missions/
   Bob writes plan.yaml summarizing the decomposition and rationale.
   Token cost: HIGH — this is the major exploration step.
                Replaces the broad exploration that would have
                happened anyway in a single-mission flow.

5. Developer runs:  missionforge plan MF-001
   CLI: validates the dependency graph (no cycles, all references
        resolve), computes topological execution order, writes
        the resolved plan to plan.yaml
   Token cost: zero

6. Human reviews and approves the decomposition
   Human reads the proposed sub-missions and the dependency graph
   Human can ask Bob to revise specific sub-missions before approving
```

### Phase 3: Sub-Mission Execution (Loop)

For each sub-mission in topological order, the following loop runs:

```
7. Developer runs:  missionforge next MF-001
   CLI: reports the next sub-mission ready to execute
        (all its dependencies have passed validation)
   Token cost: zero

8. Developer runs:  missionforge baseline MF-001-A --capture
   CLI: writes baseline.todo.json scoped to sub-mission A's metrics
   Token cost: zero

9. Bob reads ONLY the files in sub-mission A's scope
   Bob fills in baseline values
   Token cost: focused, narrow reads

10. Developer runs:  missionforge baseline MF-001-A --commit
    CLI: validates baseline complete, stamps to immutable baseline.json
    Token cost: zero

11. Bob implements sub-mission A's scope of changes
    Bob refers to sub-mission.yaml for scope (no re-derivation)
    Token cost: implementation cost for this sub-mission only

12. Developer runs:  missionforge validate MF-001-A --capture
    CLI: runs `git diff --name-only` scoped to sub-mission A's paths
    CLI: runs sub-mission A's test_command
    CLI: writes validation.todo.json
    Token cost: zero for boundary and tests; focused for metrics

13. Bob fills validation.todo.json metric values for sub-mission A
    Token cost: focused

14. Developer runs:  missionforge validate MF-001-A --commit
    CLI: diffs current vs targets, computes pass/fail
    CLI: writes validation.json for sub-mission A
    Token cost: zero
```

This loop repeats for B, C, and D in dependency order. In Phase 1 of the product, the loop is sequential. The CLI's `next` command always returns one sub-mission at a time. In Phase 3 (future work), `next` could return multiple ready sub-missions and they could be executed in parallel.

### Phase 4: Parent Aggregation and Reporting

```
15. Developer runs:  missionforge validate MF-001
    CLI: checks every sub-mission has validation.json with PASSED status
    CLI: runs the parent-level test_command
    CLI: re-runs `git diff` against parent forbidden_paths to catch
         any sub-mission that touched a parent-forbidden file
    CLI: prompts Bob to re-measure parent aggregate metrics if needed
    CLI: writes the parent validation.json
    Token cost: zero for CLI checks; focused if aggregate re-measurement needed

16. Developer runs:  missionforge report MF-001
    CLI: templates the parent evidence report aggregating:
         - parent mission.yaml
         - plan.yaml (decomposition rationale)
         - every sub-mission's baseline.json and validation.json
         - aggregate parent metrics
         - full git diff for the whole mission
    CLI: writes report.md
    Token cost: zero
```

### Token Accounting

The decomposition step (Phase 2) is the new expensive operation. It replaces the broad exploration that would have happened in any approach. The trade-off: one expensive decomposition pass produces structured sub-missions whose subsequent baseline-and-validate steps are individually cheap and scoped.

The total token cost is roughly equal to or slightly higher than a single-mission flow, but with these benefits:

- Sub-missions can be reviewed and approved independently
- A failed sub-mission can be retried without restarting the parent
- The architecture is ready for true parallel execution in future phases
- Each sub-mission's evidence is independently auditable

### Why This Order Matters

The decomposition happens *before* baseline capture, not after. This is deliberate. Bob proposes how the work should be split based on the codebase structure, and only then does the CLI scope the baseline questions to each sub-mission. If decomposition happened after baseline, Bob would have read the codebase twice — once to measure baselines for an undecomposed mission, then again to decompose.

---

## 7. Example: Evidence Report

The CLI templates the parent evidence report from the mission, plan, every sub-mission's state, and the git diff. Bob does not write it.

```markdown
# Mission MF-001: Matchmaking Modernization

## Goal
Modernize matchmaking from CORBA to REST while preserving multiplayer
functionality across both the Java Swing client and the Python TUI
client. All other CORBA flows must remain untouched and working.

## Status: PASSED

## Decomposition
Bob decomposed this mission into 4 sub-missions with the following
dependency structure:

```
MF-001-A ───┬─── MF-001-B ───┐
            │                 │
            └─── MF-001-C ────┴─── MF-001-D
```

| Sub-mission | Title | Status |
|---|---|---|
| MF-001-A | Add REST endpoint for matchmaking | PASS |
| MF-001-B | Migrate Swing client to REST matchmaking | PASS |
| MF-001-C | Migrate Python client to REST matchmaking | PASS |
| MF-001-D | Integration test for dual-client REST matchmaking | PASS |

## Scope (Parent-level)
- Forbidden paths: server/src/game/**, server/src/scoring/**,
  server/src/session/**, idl/Game.idl, idl/Scoring.idl
- Forbidden files changed (across all sub-missions): 0
- Total files modified: 6

## Aggregate Metrics

| Metric | Baseline | Target | Final | Status |
|---|---|---|---|---|
| corba_refs_in_matchmaking | 7 | 0 | 0 | PASS |
| in_game_corba_flow_still_works | true | true | true | PASS |

## Sub-Mission Results

### MF-001-A: REST Endpoint
- Files modified: 2
- Metrics:
  - rest_endpoint_exists: false → true (PASS)
  - rest_endpoint_delegates_to_corba: false → true (PASS)
- Test result: PASS

### MF-001-B: Swing Client Migration
- Files modified: 2
- Metrics:
  - swing_uses_rest_for_matchmaking: false → true (PASS)
  - corba_matchmaking_imports_in_swing: 3 → 0 (PASS)
- Test result: PASS

### MF-001-C: Python Client Migration
- Files modified: 1
- Metrics:
  - python_uses_rest_for_matchmaking: false → true (PASS)
- Test result: PASS

### MF-001-D: Dual-Client Integration Test
- Files modified: 1 (new test file)
- Metrics:
  - dual_client_test_exists: false → true (PASS)
  - dual_client_test_passes: false → true (PASS)
- Test result: PASS

## Tests
- Parent-level command: `./gradlew integrationTest && pytest tests/integration`
- Result: PASS (Java: 42 passed; Python: 11 passed)

## Files Changed
[generated from git diff]

## Bob Session
- Decomposition session: [linked]
- Per-sub-mission sessions: [4 linked sessions]
- Total Bobcoins consumed: [tracked]

## Next Mission
MF-002 drafted: Modernize game state synchronization.
```

The report is the artifact judges and human reviewers see. It is meant to be PR-attachable. The decomposition diagram at the top is the key visual element — reviewers can see at a glance how the work was broken down and which sub-missions passed.

---

## 8. Why CLI-First, Not MCP

Earlier design iterations considered exposing MissionForge through MCP. The decision was to keep it CLI-first for these reasons.

**Server lifecycle overhead.** MCP servers need to be running, configured in Bob's MCP settings, and managed. For a judge cloning the repo, "run this CLI" beats "configure this MCP server, restart Bob, verify connection."

**Schema gymnastics.** MCP tools require JSON schemas for every input and output. The CLI's outputs are already structured JSON. Wrapping them in MCP means re-declaring schemas in two places.

**Debugging surface.** When something breaks, MCP adds a transport layer to debug in addition to the actual logic.

**Demo legibility.** In the exported Bob task session markdown, bash commands are immediately readable. MCP calls appear as opaque tool invocations. The CLI-first approach produces a more compelling judging artifact.

**It is purer harness engineering.** A harness is something Bob *uses*, not something Bob *is integrated with*. The CLI-first design is independently runnable, independently auditable, and independently valuable.

MCP earns its weight when a tool is invoked many times in tight loops where bash overhead matters, or when the integration story itself is the product. Neither applies to MissionForge. The harness is invoked at milestones — init, mission, baseline, validate, report. Five to ten calls across an entire mission. Bash subprocess overhead is irrelevant at that frequency.

---

## 9. Why Bob Measures, Not the CLI

The core architectural insight: a CLI cannot measure code agnostically. Regex pattern matching is not measurement — it is string counting dressed up as analysis. The patterns drift across languages, codebases, and conventions. A textual reference to `SOAPMessage` in a comment counts the same as an actual import. Tests mocking a legacy client count the same as production usage. The metric becomes structurally unreliable.

There are three ways out of this problem:

1. **Pattern-based evidence collection.** Be explicit that the CLI counts strings, not behavior. Honest but weak.
2. **CLI as bookkeeping only.** Bob measures using its real code understanding. CLI manages state. **This is what MissionForge uses.**
3. **Build a real semantic indexer with tree-sitter.** Multi-language, mature parsers, structural facts. Too large a build for a hackathon and reinvents LSP.

Option 2 is strictly better than option 1. It is more honest, language-agnostic by construction, and lets Bob's actual strength (code reading) do the work it is good at. The CLI handles what *it* is good at: state, schema, file paths, git, templating.

The pitch becomes tight:

> Bob measures the code. MissionForge measures the mission. Together you get refactor work with a contract — scoped paths, named metrics, before-and-after evidence, and a report your reviewer can trust.

---

## 10. Demo Strategy

The demo is a pre-recorded video, not a live presentation. This unlocks production polish, multiple takes, and tighter scope control.

### The Demo Subject

A Boggle-style multiplayer game with three components:

- A Java Swing client (modern-looking, well-built)
- A Python TUI client
- A CORBA backend that both clients communicate with via shared IDL contracts

This is a real distributed system using language-agnostic IDL the way CORBA was actually used in production. Most modern engineers have never seen this work in person. The Swing client and Python TUI playing against each other through a shared ORB is genuinely cool and instantly demonstrable.

### The Framing

The pitch is not "scary legacy code that nobody wants to touch." The pitch is warmer and more honest:

> I built a Boggle game I'm proud of. Java Swing client, Python TUI client, both play against each other in real time through a CORBA backend. The game works great — but CORBA is a 1990s technology and I want to modernize it without breaking what I built. I'm not going to rewrite it all at once. I'm going to do it one mission at a time. Watch the first one: modernizing matchmaking.

This framing works because:

- It is emotionally relatable. Every developer has built something they love on a foundation they know they need to migrate.
- It is honest about scope. The demo shows one mission, not a heroic full rewrite.
- It uses the cross-language client asset as the load-bearing technical demonstration.
- It does not require the app to look visually legacy. The legacy is in the architecture, not the UI. "Beautiful game on a fragile foundation" is a stronger story than "ugly old code."
- The "first mission" framing implies a sequence of missions, which is exactly what MissionForge is built for.

### The First Mission: Matchmaking

Matchmaking is the chosen scope for the demo because:

- **It is self-contained.** Players request a match, the system pairs them, returns connection info. One logical flow with clear inputs and outputs.
- **It is orthogonal to gameplay.** Matchmaking happens before the game starts. The mission can modernize it without touching in-game code, keeping forbidden paths meaningful.
- **It is universally recognizable.** Judges do not need to understand Boggle to understand matchmaking. The mission's purpose lands without explanation.
- **It is visibly demonstrable.** Two clients request a match, both get paired, game begins. That is a clear demo beat.
- **It has natural metrics.** CORBA references in matchmaking (target: zero), REST endpoint exists (target: yes), both clients use REST for matchmaking (target: yes), integration test passes through both clients (target: pass), rest of system still works through CORBA (target: pass — proving scope held).
- **It is *first*.** The framing "let's start with matchmaking" implies sequence. There will be more missions. The methodology shows up implicitly without overclaiming.

### Mission Scope

The first mission's contract:

- **Goal:** Modernize matchmaking from CORBA to REST while preserving multiplayer functionality across both clients.
- **Allowed paths:** The matchmaking service implementation, a new REST endpoint file, both client files where matchmaking is invoked, the matchmaking integration test.
- **Forbidden paths:** All in-game logic, all scoring logic, all auth (if present), all other CORBA services. Proves the rest of the system is untouched.
- **Metrics:**
  - CORBA references in matchmaking module: baseline N, target 0
  - REST endpoint exists with operation matching IDL signature: baseline no, target yes
  - Swing client uses REST for matchmaking: baseline no, target yes
  - Python client uses REST for matchmaking: baseline no, target yes
  - Integration test passes through both clients via REST: baseline no, target yes
  - In-game CORBA flow still works: baseline yes, target yes (regression guard)
- **Test command:** The project's integration test suite for matchmaking flow.

### Why This Is Honestly Recordable

CORBA-to-REST modernization while preserving cross-language client interop is not a one-shot task. The full-backend version of this demo would require either dishonest editing or 20+ hours of Bob session wrestling. Neither is acceptable.

By scoping to one operation:

- Bob's actual work in the session is achievable: read the existing matchmaking code, plan the REST replacement, implement the endpoint, modify both clients to call REST for this one operation, run validation.
- The Bobcoin cost is moderate (estimated 6-9 Bobcoins for one full mission).
- The recorded session reads coherently in the task session export.
- The artifacts in the repo are genuinely working, not theatrical.

The demo does not claim Bob modernized the whole backend. It claims Bob completed one scoped, measurable mission, and that the methodology scales. The viewer fills in the implied future missions.

### Acceptable Pre-Work Before Recording

To make the recorded Bob session run cleanly, the following pre-work is acceptable and not dishonest:

- Designing the REST endpoint shape (the architect role)
- Writing the integration test that the mission will be validated against (the QA role)
- Drafting the mission.yaml by hand (the planner role)
- Setting up any required dependencies (REST framework, test runner)
- Confirming the modernization is achievable by attempting it manually first

What is *not* acceptable: pre-writing the actual modernization code Bob will produce in the session. Bob must genuinely do the implementation work on camera.

The principle: you set up the conditions for success. Bob does the actual modernization the harness scopes and validates. This mirrors how a real consulting engagement works — an architect designs the target state, an implementer makes it happen.

### Video Structure

A pre-recorded video, roughly 3 minutes, tightly edited.

**Opening (15 seconds):** Both clients on screen side by side. Java Swing and Python terminal. Both running, both connected to the CORBA backend, both playing a real game. Words being submitted, scores updating. Caption: "Java client. Python client. Both play against each other through a CORBA backend."

**Pivot (15 seconds):** Cut to code. Show the IDL file. Show the ORB initialization. Show the matchmaking service implementation. Caption: "The game works great. But CORBA is from 1991. I want to modernize it — not all at once, one mission at a time."

**Introduce MissionForge (15 seconds):** Brief and clean. The harness, the mission contract, the philosophy. End with a quick shot of the Mission Board showing an empty board waiting for the first mission.

**Parent mission authoring (20 seconds):** Show the parent mission.yaml being written — the goal prose, the forbidden paths, the aggregate metrics. User types the goal. MissionForge validates. The Mission Board shows MF-001 appearing in the "Drafted" column. Caption: "The contract: what to do, what not to touch."

**Decomposition by Bob (30 seconds):** This is the wow moment of the video. Show the terminal: `missionforge decompose MF-001`. Bob reads the matchmaking code, reasons about boundaries, writes four sub-mission files. Cut to the Mission Board: MF-001 expands to reveal four child cards — MF-001-A, MF-001-B, MF-001-C, MF-001-D — arranged in the dependency diamond. Show `missionforge next MF-001` output: "MF-001-A: Ready (no dependencies). Execute now." Caption: "Bob decomposed the work. The harness resolved the dependency order."

**Bob works (50 seconds, compressed):** Split screen. Left: Bob session in the IDE working sub-mission A (REST endpoint), then B (Swing client), then C (Python client). Right: Mission Board — sub-mission cards moving through columns sequentially. After B and C are both shown starting, the Board flashes a subtle callout: "MF-001-B and MF-001-C were both ready — executing sequentially. Phase 3 will run these in parallel." Voiceover narrates. Speed up the slow parts.

**Watsonx moment (15 seconds):** Pause on the Mission Board mid-session. Open the Mission Chat sidebar. Type: "Why are B and C independent of each other?" Watsonx.ai responds: "Because the Swing client and Python client are separate files in separate paths — their migrations don't share state. They both depend on the REST endpoint (A) but not on each other." Caption: "Ask the mission anything — powered by watsonx.ai."

**Validation (15 seconds):** MF-001-D completes. `missionforge validate MF-001` runs at the parent level. All sub-missions passed. Aggregate metrics met. Parent card moves to "Done." Green checkmarks cascade across all four child cards.

**Stakeholder view (15 seconds):** Toggle the Mission Board to Stakeholder View. The technical card transforms into a business-friendly summary: "Matchmaking is now infrastructure-independent. Both game clients work. No breaking changes to the in-game experience." Caption: "Engineers see the diff. Managers see the impact."

**Closing (10 seconds):** Both clients playing a full game. Matchmaking flows through REST. Gameplay still flows through CORBA. MF-002 card appears in "Drafted" on the Board. Closing line: "One mission down. The next is already planned. One mission at a time, until the system is done."

### The Teaser Mission

Drafting a second mission file (MF-002) and showing it briefly in the closing is cheap work that does enormous narrative lifting. The cost is one YAML file. The benefit is implying methodology and scale without overclaiming what was actually shown.

The second mission's goal can be anything plausible — modernizing game state sync, modernizing the leaderboard, modernizing player session management. It does not need to be implemented. It just needs to exist as a file the viewer sees for two seconds, ideally as a card in the "Drafted" column on the Board.

---

## 11. The Mission Board (Web UI)

The Mission Board is a web frontend that visualizes MissionForge state. It is downstream of the CLI — it reads `.missionforge/` state and renders it as a Kanban-style board with detail panels for each mission. The CLI remains the source of truth and the harness still works fully standalone from the terminal.

### Why the Board Exists

The CLI is correct and complete, but text output is hard to *show*. The whole pitch of MissionForge — "scoped, measurable, reviewable" — is abstract when it lives in markdown files. The Board makes it legible:

- Mission state becomes a visual progression through phases
- Metric progress becomes a visible bar ticking toward its target
- Scope violations become red flags you cannot miss
- Evidence reports get a render pass instead of staying as raw markdown

The Board also lets non-developers participate. PMs, managers, and reviewers who do not run Bob can still see what is happening, ask questions, and approve missions.

### Kanban Columns

The board has two levels: parent missions and sub-missions. Sub-missions are visible when a parent card is expanded.

**Parent mission columns:**

- **Drafted** — Parent mission.yaml written, awaiting human review
- **Approved** — Human approved, decomposition pending
- **Decomposing** — Bob is running `missionforge decompose`, writing sub-mission files
- **In Progress** — Sub-missions are being executed sequentially
- **Validating** — All sub-missions complete, parent aggregate validation running
- **Done** — Parent validation passed, evidence report generated
- **Blocked** — One or more sub-missions failed, parent needs attention

**Sub-mission columns (visible when parent is expanded):**

- **Pending** — Waiting for a dependency to complete
- **Ready** — All dependencies passed, this sub-mission can execute next
- **In Progress** — Bob is working this sub-mission
- **Validating** — Implementation complete, sub-mission validation running
- **Done** — Sub-mission validation passed
- **Blocked** — Validation failed, needs fixes

The "Ready" state is the visual representation of latent parallelism. When MF-001-B and MF-001-C are both in "Ready" simultaneously — even though Phase 1 executes them sequentially — the Board shows this clearly. A subtle callout reads: "2 sub-missions ready. Phase 1 executes sequentially. Phase 3 will run these in parallel."

### Mission Card

**Parent card (collapsed):**

- Mission ID and one-line goal
- Current phase (matches parent column)
- Overall progress bar: count of sub-missions Done vs total
- Forbidden-path violation count (red badge if non-zero)
- Parent test status: pass, fail, not-yet-run
- Expand arrow to see sub-missions

**Parent card (expanded):**

Shows child sub-mission cards in a dependency-aware layout. Cards in the same dependency level (like MF-001-B and MF-001-C) appear side by side. Dependency arrows connect parent sub-missions to child sub-missions visually.

**Sub-mission card:**

- Sub-mission ID and title
- Current phase (matches sub-mission column)
- Metric progress strip (baseline → current → target)
- Scope evidence: files changed, forbidden violations
- Test status
- "depends on" and "unlocks" relationship badges

Clicking any card (parent or sub-mission) opens the Mission Detail panel.

### Mission Detail Panel

Opens to the right of the board when a card is clicked. For parent missions:

- **Goal** — The prose mission statement
- **Decomposition** — The dependency diamond rendered as a diagram
- **Sub-missions** — Expandable list of each sub-mission with its own metrics and status
- **Aggregate Metrics** — Parent-level metrics table with baseline, current, target, status
- **Git Diff** — Combined diff across all sub-missions, color-coded allowed/forbidden
- **Evidence Report** — The aggregate markdown rendered with proper styling
- **Stakeholder View** — Business-friendly translation (see Section 12)
- **Mission Chat** — Sidebar for asking questions about any aspect of the mission

For sub-missions:

- **Goal** — The sub-mission prose goal
- **Scope** — Allowed paths (scoped to this sub-mission)
- **Dependencies** — Which sub-missions must complete before this one
- **Metrics** — Sub-mission-level metrics table
- **Git Diff** — Files changed by this sub-mission only
- **Bob Session** — Task session for this specific sub-mission

### Trigger Actions

The Board can trigger CLI commands via buttons. The CLI does the work; the Board observes the result.

- **Approve** — Moves the mission from Drafted to Approved, runs `missionforge mission MF-001 --validate` to confirm the YAML is valid
- **Capture Baseline** — Runs `missionforge baseline MF-001 --capture` to write the baseline.todo.json
- **Commit Baseline** — Runs `missionforge baseline MF-001 --commit` after Bob fills the values
- **Validate** — Runs `missionforge validate MF-001 --capture` followed by `--commit` after Bob fills the values
- **Generate Report** — Runs `missionforge report MF-001`
- **Publish** — Sends the report to a configured destination (optional Orchestrate hook)

For the MVP and the recorded demo, the Board is primarily read-only with one or two trigger buttons enabled (approve, generate report). Full trigger support is a stretch goal.

### Real-Time Updates

The Board polls `.missionforge/` for state changes every few seconds. This is simple, demo-friendly, and adequate. WebSockets are not required for the hackathon. When the demo shows the board updating in real time as Bob works, that update happens via polling.

### Frontend Stack

- Next.js 14 with the App Router for the framework
- Tailwind CSS for styling (matches your stack experience from ESCA Mobile)
- A Kanban library like `@hello-pangea/dnd` for drag-and-drop (drag-and-drop is stretch — the cards can move between columns automatically based on state)
- Recharts or similar for the metric mini-charts
- A simple Node or Python backend that wraps the CLI and exposes mission state as JSON over HTTP

### Where the Board Lives

A small `missionforge-board/` directory at the project root contains the Next.js app and a thin backend service. The Board can be started with `missionforge board` (a new CLI command that boots the backend and opens the browser) or run as a standalone Next.js dev server.

Critically, the Board is *optional*. The CLI runs fully without it. The Board adds visualization but is not required for the harness to function.

---

## 12. Watsonx Integration

Two watsonx.ai integrations live on the Mission Board. Both fill genuine architectural gaps Bob cannot reach from the IDE. Neither duplicates Bob's work.

### Integration 1: Mission Chat Sidebar

A chat interface inside the Mission Detail panel. The user asks questions about the current mission state, and watsonx.ai answers from the mission's structured data.

**What it answers:**

- "Why did this mission fail validation?"
- "What changed between the baseline and the current state?"
- "Which forbidden file was touched and where?"
- "Summarize this mission for my standup tomorrow."
- "What is the risk if I lower this metric target?"
- "Explain the matchmaking modernization in plain English."

**How it works:**

The Board's backend gathers the mission's grounding context: `mission.yaml`, `baseline.json`, `validation.json`, `report.md`, and the git diff. This package is included as system context in a watsonx.ai chat completion call (Granite 3 8B Instruct model recommended for hackathon scope and cost). The user's question is appended as the user message. The response streams back into the chat sidebar.

**Why it shines:**

Bob lives in the IDE. The Board lives in the browser. The Board needs an AI it can call directly without context-switching to Bob. Watsonx.ai is the natural fit — runtime synthesis over structured mission data, available to non-developers.

The grounding context is small (a few hundred lines of JSON and markdown), so each query is cheap. Compare to asking Bob the same question, which would cost Bobcoins and require an IDE session.

**Implementation:**

```python
# Pseudocode for the chat endpoint
def mission_chat(mission_id: str, user_message: str):
    context = load_mission_context(mission_id)
    system_prompt = f"""
    You are a mission assistant for MissionForge. Answer questions about
    the mission below using ONLY the provided data. Do not speculate
    about code you cannot see. If a question requires reading source
    code, say so and suggest the user check with Bob in the IDE.

    Mission state:
    {json.dumps(context, indent=2)}
    """
    response = watsonx.chat(
        model="ibm/granite-3-8b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response
```

### Integration 2: Stakeholder Translation Panel

A "stakeholder view" toggle on each mission card and the detail panel. Translates technical mission state into business-friendly language for non-engineering audiences.

**What it produces:**

For each mission:

- **One-sentence business summary** ("Players in different regions can now find matches without latency spikes.")
- **Status indicator with emoji** (in progress, complete, at risk, blocked)
- **Percent complete** based on metric progress toward targets
- **Business risk callouts** if validation found scope violations or test failures
- **What changed for the user** if the mission affects user-facing behavior

**How it works:**

Same architecture as Mission Chat. The Board's backend sends mission state to watsonx.ai with a system prompt that frames the model as a technical-to-business translator. The model produces the stakeholder summary fields, which the Board renders as a styled card.

The translation is regenerated when the mission state changes, but cached between changes to avoid repeated calls.

**Why it shines:**

Engineering managers and product managers care about modernization progress but cannot read evidence reports written for engineers. The Mission Board, with the Stakeholder Translation panel, gives them a view of the same work that meets them where they are.

This solves a real organizational problem (the eng/business communication gap on legacy work) and demos beautifully — judges immediately understand the value when they see a technical mission card transform into a business-friendly summary.

**Implementation:**

```python
# Pseudocode for the stakeholder translation
def stakeholder_view(mission_id: str):
    context = load_mission_context(mission_id)
    system_prompt = """
    You are a technical translator. Convert the engineering mission state
    below into a business-friendly summary with these fields:

    - business_summary: one sentence, plain English, what this delivers
    - status: in_progress | complete | at_risk | blocked
    - percent_complete: integer 0-100 based on metric progress
    - risk_callouts: array of brief risk notes (empty if no risks)
    - user_impact: what changes for end users (empty if internal-only)

    Return JSON only.
    """
    response = watsonx.chat(
        model="ibm/granite-3-8b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(context)},
        ],
    )
    return json.loads(response)
```

### Why These Two and Not Others

Several other watsonx integrations were considered and deliberately dropped to keep scope tight:

- **Mission authoring assistant** (watsonx drafts a mission from plain English) — useful but adds another flow to the demo
- **Audience-aware evidence reports** (different report variants for different readers) — overlaps with Stakeholder Translation
- **Next-mission recommendation** (watsonx synthesizes MF-002 from MF-001 history) — strong demo moment but requires additional UI work
- **Voice integration** (IBM TTS/STT) — bonus territory, not core

The Mission Chat and Stakeholder Translation are chosen because each fills a structural gap (browser-based AI access for the Chat, non-developer access for the Translation) that Bob cannot reach from the IDE. They earn their place rather than being decoration.

### Honest Constraints

- **Watsonx.ai inferencing consumes tokens (Resource Units).** Each chat query and each stakeholder translation costs a small amount. For the demo, this is negligible. For real production use, the Board would need caching and rate limiting.
- **The Granite 3 8B Instruct model is the recommended choice** for hackathon scope. It is fast, capable enough for synthesis over small context, and well-supported. Larger models are unnecessary here.
- **Both integrations require IBM Cloud credentials** (API key, project ID, endpoint URL). The Board reads these from environment variables. Never commit them.
- **Latency target: under 5 seconds per query.** With Granite 3 8B and small context, this is comfortable.

### Why Not Orchestrate

Orchestrate is mentioned briefly in the "Publish" trigger above as an optional path, but it is not a core integration. The reason: the two chosen watsonx.ai integrations already deliver the watsonx hackathon points cleanly and demonstrate real value. Adding Orchestrate would mean another moving piece for marginal additional reward.

If time remains after the two integrations are polished, an Orchestrate "Publish" workflow can be added that takes the evidence report and posts to a configured Slack channel or drafts a GitHub PR description. This is the stretch goal closer.

---

## 13. Benchmark

A simple, falsifiable comparison.

| Metric | Without MissionForge | With MissionForge |
|---|---|---|
| Bobcoins consumed on the same refactor | measured | measured |
| Forbidden files modified | inspected manually | enforced by CLI |
| PR-attachable evidence | not produced | generated |
| Baseline metrics recorded | none | structured JSON |
| Target verification | none | per-metric pass/fail |
| Re-runnable validation | no | yes |
| Visible to non-engineers | no | yes (Mission Board + Stakeholder Translation) |

The Bobcoin claim is concrete and demo-friendly. Run the matchmaking modernization twice — once with Bob freely exploring, once with the harness — and report the Bobcoin delta. It is a single number a hackathon judge understands instantly.

Be honest about where MissionForge loses. For trivial one-file edits, the harness adds overhead. MissionForge's value lives in multi-file refactors where scope, evidence, and review matter.

---

## 14. Scope and Failure Modes

### What MissionForge Handles Well

- Multi-file refactors with clear scope boundaries
- Modernization missions with measurable before/after metrics
- Work that naturally decomposes into independently-scoped sub-tasks
- Work that needs PR-attachable evidence with independent sub-mission audit trails
- Sessions where reviewers will ask "what did Bob change and why, and in what order"
- Teams where engineering and non-engineering stakeholders need different views of the same work

### What MissionForge Does Not Handle

- One-line fixes (overhead exceeds value)
- Open-ended exploration ("understand this codebase")
- Tasks where the goal cannot be expressed as a metric ("make this code more elegant")
- Cross-repository refactors (single-repo scope only)
- Work that cannot be decomposed into sub-missions with clean boundaries (deeply tangled monoliths)

### Failure Modes

**Bob writes a poor metric definition.** The CLI validates faithfully against a bad target. The mission approval step exists for this reason — a human reviews the mission before execution begins.

**Bob mis-measures a baseline.** Validation compares against the wrong number. The capture/commit two-phase pattern gives a checkpoint where a human sanity-checks baseline values before they freeze.

**Bob decomposes poorly — overlapping allowed_paths between sub-missions.** If two sub-missions both claim the same file in their allowed_paths, they may conflict when executed sequentially. The `missionforge plan MF-001 --validate` step catches this and flags the overlap before execution begins.

**Bob proposes a dependency cycle.** If Bob declares MF-001-B depends on MF-001-C and MF-001-C depends on MF-001-B, the plan is invalid. The `missionforge plan` command validates the graph is acyclic before writing plan.yaml. Bob is asked to revise.

**Sub-mission A passes but B fails because A's output has the wrong shape.** This is an integration issue — A's REST endpoint may exist but the Swing client can't parse its response format. Each sub-mission's individual validation passes, but the parent aggregate validation fails when the parent test_command runs the integration suite. This is exactly what the two-level validation catches.

**Two sub-missions touch the same file from different allowed_paths.** The git diff validator checks each sub-mission's changes against its own allowed_paths. If a sub-mission modifies a file not in its allowed list (even if in another sub-mission's allowed list), it is flagged as a scope violation.

**The test command is wrong or missing.** MissionForge records this honestly in the report. No test command means no test evidence. A wrong test command catches fewer bugs. The mission approval step is where humans should verify the test command is meaningful.

**The mission file is invalid YAML.** Caught at `missionforge mission MF-001 --validate` before decomposition begins.

**Polyglot repositories.** MissionForge is language-agnostic because Bob handles all source reading. The CLI never reads source code. The sub-mission scope boundaries are file paths, which are language-agnostic.

---

## 15. Security and Repo Hygiene

- `.missionforge/` should be added to `.gitignore` by default, except for `mission.yaml` and `report.md` which are intended to be committed
- The CLI never makes network calls
- The CLI never reads files outside the repo root
- The test command runs in a subprocess with no special privileges
- No telemetry, no analytics, no external service dependencies
- The Mission Board's backend reads watsonx.ai credentials from environment variables only; never commit them
- The Mission Board, when run locally, binds to localhost by default and does not expose mission data over the network unless explicitly configured

---

## 16. Implementation Notes

### CLI Technology

- CLI in Python 3.11+ (Click or Typer for command structure)
- YAML parsing via PyYAML or ruamel.yaml
- Git operations via subprocess calls to system git (no GitPython dependency)
- JSON schema validation via jsonschema
- Markdown templating via Jinja2

### Mission Board Technology

- Next.js 14 with the App Router for the frontend framework
- Tailwind CSS for styling
- A Kanban library such as `@hello-pangea/dnd` for board interactions
- Recharts for the metric mini-charts on each card
- A thin FastAPI backend (Python) that wraps the CLI and exposes mission state as JSON over HTTP
- Polling-based updates every 3-5 seconds rather than WebSockets for MVP simplicity

### Watsonx Integration Technology

- Watsonx.ai Python SDK (`ibm-watsonx-ai`) for chat completion calls
- Granite 3 8B Instruct as the default model for both Mission Chat and Stakeholder Translation
- API key, project ID, and endpoint URL loaded from environment variables (`IBM_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL`)
- A small caching layer in the Board's backend to avoid re-translating unchanged mission state
- Latency target under 5 seconds per query with the recommended model and small context

### Distribution

- Single `pip install missionforge` command for the CLI
- The Mission Board ships as a Next.js app in `missionforge-board/`, started with `missionforge board` or via standard Next.js dev/build commands
- The Skill and slash commands are markdown files copied to `.bob/skills/missionforge/` and `.bob/commands/`
- For the hackathon demo, the Mission Board can be deployed to Vercel for a live URL judges can visit

### Lines of Code Estimate

- CLI core: 800-1500 lines of Python (schema validation, templating, CLI plumbing)
- Mission Board frontend: roughly 1500-2500 lines of TypeScript/TSX
- Mission Board backend: 300-500 lines of Python
- Watsonx integration code: 150-300 lines split across the Board backend

Most of the volume is in the frontend (components, layouts, styling). The actual logic remains small because the CLI does not read source code and the Board does not duplicate the CLI's responsibilities.

---

## 17. Build Plan and Time Allocation

The project has two phases with a third on the roadmap. Phase 1 is the hackathon deliverable. Phase 2 is built after Phase 1 is working. Phase 3 is future work pitched as a roadmap item.

### Phase Structure

**Phase 1 — CLI Harness (hackathon deliverable)**
Everything a developer needs to run decomposable, measurable, reviewable modernization missions from the terminal. Bob + the CLI + the Skill + slash commands. The recorded demo uses Phase 1.

**Phase 2 — Mission Board (web UI)**
The Next.js visualization layer. Built after Phase 1 is complete and the demo session is recorded. The Board is demo-friendly polish, not the core product.

**Phase 3 — True Parallel Execution (roadmap)**
Multiple Bob Shell instances executing independent sub-missions concurrently. The architecture already supports this — it just requires switching `missionforge next` from returning one ready sub-mission to returning all ready sub-missions and dispatching them in parallel.

### Go/No-Go Gate (First Day)

Before writing any code, confirm three things:

1. The Boggle game runs end-to-end: Swing client + Python TUI + CORBA backend, both clients connect, a full game completes.
2. Matchmaking is reasonably isolated — its own CORBA service, not tangled with game state.
3. The matchmaking modernization is *manually* achievable. Spend a few hours doing the REST migration by hand with no Bob. Confirm the path is clear before committing.

If any of these fail, scope adjusts: pick a different first mission, do a tiny pre-cleanup, or accept that the demo uses a simpler codebase.

### Phase 1 Build Order

**First: CLI foundation**

- `missionforge init MF-001` and workspace structure
- `missionforge mission MF-001 --validate` (parent YAML schema validation)
- `missionforge decompose MF-001` (Bob session trigger, writes sub-mission files)
- `missionforge plan MF-001` (dependency graph validation, topological sort, writes plan.yaml)
- `missionforge next MF-001` (returns next ready sub-mission, reports latent-parallel set)
- Sub-mission baseline capture/commit
- Sub-mission validate capture/commit
- Parent aggregate validate
- `missionforge report MF-001` (aggregate evidence report)

**Second: Skill and slash commands**

- SKILL.md teaching Bob the decompose-plan-execute-validate loop
- `/mf-init`, `/mf-decompose`, `/mf-next`, `/mf-baseline`, `/mf-validate`, `/mf-report`

**Third: Demo preparation**

- Write the parent mission.yaml for the Boggle matchmaking modernization
- Write the integration tests that the mission validates against
- Design the REST endpoint shape for matchmaking
- Confirm the decomposition Bob produces makes sense (run it once manually)
- Record the full Bob session end-to-end
- Capture all task session markdown exports (judging artifact)
- Polish the evidence report template

### Phase 2 Build Order

After the Phase 1 recording is done and the Bob session exports are saved:

- FastAPI backend wrapping CLI, exposing mission state as JSON
- Next.js board with parent + sub-mission card hierarchy
- Polling-based state updates every 3-5 seconds
- Mission detail panel
- Stakeholder Translation (watsonx.ai)
- Mission Chat sidebar (watsonx.ai)
- Deploy to Vercel for a live URL

### Final Stretch (both phases done)

- Script the submission video scene by scene
- Record voiceover
- Edit the video (8-12 hours — budget this seriously)
- Write the README
- Final submission packaging

### What to Cut First If Time Runs Short

In strict priority order:

1. Cut Orchestrate Publish workflow (never critical)
2. Cut Stakeholder Translation panel (keep Mission Chat)
3. Cut Mission Board entirely — fall back to CLI + terminal-only demo (Phase 1 alone is sufficient)
4. Cut the MF-002 teaser mission file
5. Cut evidence report visual polish

Do not cut: the matchmaking demo, the video, the Bob task session exports, the evidence report.

### Bobcoin Budget

Rough allocation across 40 Bobcoins:

| Activity | Estimate |
|---|---|
| CLI development with Bob's help | 6-10 Bobcoins |
| Skill/slash command tuning with Bob | 2-3 Bobcoins |
| Mission Board scaffolding with Bob | 3-5 Bobcoins |
| Decomposition session (exploratory pass on Boggle codebase) | 2-3 Bobcoins |
| Full recorded demo session (one take) | 6-9 Bobcoins |
| Retakes if first session is messy | up to 10 Bobcoins |
| Reserve | 3-5 Bobcoins |

Build the CLI by hand where you can. The Board frontend is your stack — use Bob only for the parts that genuinely need it.

---

## 18. Final Pitch

MissionForge gives Bob a map, a mission, and a validation gate.

You built something you love. It works. But it sits on a foundation you know you need to migrate — CORBA, SOAP, an old framework, a coupling problem that grew over years. You are not going to rewrite it all at once. You are going to modernize it one mission at a time.

Bob explores the codebase once and writes a mission contract: scoped paths, named metrics, target values. MissionForge enforces the contract. Bob does the modernization work. MissionForge runs the boundary checks, captures the baseline and final measurements, runs the tests, and generates a PR-ready evidence report.

The CLI never reads source code. It is language-agnostic by construction. It works on TypeScript, Python, Java, Go, or any polyglot mix because Bob handles all code reading.

The Mission Board makes the work visible. Engineers see scope boundaries and metric progress at a glance. Managers and PMs get a stakeholder-friendly translation of the same state, powered by watsonx.ai. A mission chat sidebar lets anyone ask questions about mission state without context-switching to Bob in the IDE.

The harness is independently runnable. Uninstall Bob tomorrow and MissionForge still produces clean, reviewable refactor records from the command line. The Board is a view on top, not a dependency. That is true harness engineering — not a Bob plugin, not a wrapper, but a tool that Bob happens to drive well, with a visualization layer that makes the discipline legible.

The demo: a Boggle game with a Java Swing client and a Python TUI client playing against each other through a CORBA backend. The first mission modernizes matchmaking from CORBA to REST while preserving multiplayer functionality across both clients. The Mission Board shows the work happening — card moving through columns, metrics ticking toward targets, the stakeholder translation rendering in business-friendly language. Watsonx.ai answers questions about the mission as it runs. The methodology scales. The next mission is already drafted.

**Bob measures the code. MissionForge measures the mission. The Board makes it visible. Watsonx.ai makes it conversational. One mission at a time, until the system is done.**
