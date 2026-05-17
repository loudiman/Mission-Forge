# MissionForge Development Implementation Plan

This document is intended for development planning, task decomposition, issue creation, sprint planning, and ownership assignment.

It includes the necessary context for understanding what MissionForge does before breaking the work into two implementation phases.

---

# Product Context

## What MissionForge Is

MissionForge is a CLI-first harness for making AI-assisted refactor and modernization work more scoped, measurable, reviewable, and auditable.

It is designed for IBM Bob-assisted development, but it is not dependent on Bob as a platform. The core idea is that Bob performs the reasoning-heavy work, while MissionForge manages the mission structure and deterministic evidence.

MissionForge turns a vague task like:

```text
Modernize matchmaking from CORBA to REST without breaking the rest of the game.
```

into a structured mission with:

- a clear goal
- forbidden paths
- allowed paths
- measurable baseline values
- target values
- sub-missions
- dependency order
- validation results
- test evidence
- a final evidence report

The key principle is:

> Bob measures the code. MissionForge measures the mission.

Bob understands source code. MissionForge does not try to understand source code semantics. MissionForge manages state, scope, validation flow, files, git diff checks, test execution, and reporting.

---

## What Problem MissionForge Solves

AI coding agents can refactor quickly, but reviewers often need answers to questions like:

- What exactly was the agent supposed to change?
- What files was it not allowed to touch?
- What was the baseline before the change?
- What metric proves the refactor worked?
- Were tests run?
- Did the agent accidentally modify unrelated code?
- Can the result be attached to a pull request as evidence?
- Can the work be broken into smaller reviewable units?

Without a harness, these answers are usually buried in chat history, terminal logs, or the agent's final summary.

MissionForge makes these answers explicit through mission files, validation files, and generated reports.

---

## What MissionForge Is Not

MissionForge is not a semantic code analyzer.

The CLI does not:

- inspect source code meaning
- resolve symbols
- understand imports
- count language-specific references
- decide whether a refactor is correct
- replace Bob's reasoning

Instead, the CLI handles deterministic operations such as:

- creating mission folders
- validating YAML and JSON structure
- tracking mission state
- checking changed files through git
- comparing changed files against allowed and forbidden paths
- running test commands
- storing baseline and validation records
- generating Markdown reports

---

## Roles and Responsibilities

## Bob's Role

Bob is responsible for reasoning-heavy work:

- reading the codebase
- understanding the refactor goal
- decomposing the parent mission into sub-missions
- defining meaningful metrics
- filling baseline measurements
- implementing code changes
- filling validation measurements
- explaining the work when needed

Bob should use MissionForge as a workflow harness, not bypass it.

## MissionForge CLI's Role

The CLI is responsible for deterministic mission management:

- initializing mission workspaces
- validating mission and sub-mission schemas
- resolving dependency order
- producing baseline and validation todo files
- running git diff checks
- running user-provided test commands
- committing structured baseline and validation records
- generating evidence reports

The CLI is the source of truth for mission state.

## Mission Board's Role

The Mission Board is the Phase 2 web UI.

It reads MissionForge state and makes it visible through:

- Kanban-style mission cards
- parent mission and sub-mission progress
- dependency visualization
- validation status
- evidence report rendering
- stakeholder-friendly summaries
- watsonx.ai mission chat

The Board is optional. The CLI must still work without it.

## Watsonx.ai's Role

Watsonx.ai is used in Phase 2 for browser-side synthesis over mission state.

It can support:

- Mission Chat
- Stakeholder Translation
- business-friendly summaries
- risk explanations
- standup summaries

Watsonx.ai should answer from MissionForge's structured mission state, not from unrestricted speculation about the source code.

---

# Core Workflow

MissionForge follows a parent mission and sub-mission model.

## 1. Parent Mission

A parent mission describes the overall modernization or refactor goal.

Example:

```yaml
id: FG-001
goal: |
  Modernize matchmaking from CORBA to REST while preserving
  multiplayer functionality across both the Java Swing client
  and the Python TUI client.

forbidden_paths:
  - server/src/game/**
  - server/src/scoring/**
  - server/src/session/**

aggregate_metrics:
  - id: corba_refs_in_matchmaking
    description: Count of CORBA references in matchmaking code.
    baseline_target: 7
    final_target: 0

test_command: ./gradlew integrationTest && pytest tests/integration
```

The parent mission defines the high-level goal, global safety boundaries, aggregate metrics, and final validation command.

---

## 2. Decomposition into Sub-Missions

Bob decomposes the parent mission into smaller sub-missions.

Example sub-missions:

```text
FG-001-A: Add REST endpoint for matchmaking
FG-001-B: Migrate Swing client to REST matchmaking
FG-001-C: Migrate Python client to REST matchmaking
FG-001-D: Add dual-client REST matchmaking integration test
```

Each sub-mission has:

- its own goal
- its own allowed paths
- its own metrics
- its own test command
- its own dependencies

Example dependency structure:

```text
FG-001-A
  ├── FG-001-B
  └── FG-001-C
        └── FG-001-D waits for both B and C
```

This allows MissionForge to make modernization work smaller, reviewable, and eventually parallelizable.

---

## 3. Baseline Capture

Before implementation, each sub-mission captures baseline measurements.

The CLI generates a baseline todo file. Bob fills it by reading only the relevant scoped code.

Example:

```json
{
  "metric_id": "corba_matchmaking_imports_in_swing",
  "description": "CORBA imports related to matchmaking in the Swing client.",
  "baseline_target": 3,
  "value": 3
}
```

The CLI commits the completed baseline as immutable evidence.

---

## 4. Implementation

Bob implements the sub-mission while staying within the allowed paths and parent-level forbidden paths.

MissionForge does not write the code. It only gives Bob and the developer a structured mission contract to follow.

---

## 5. Validation Capture

After implementation, the CLI captures deterministic evidence:

- changed files from git diff
- whether changed files are within allowed paths
- whether forbidden paths were touched
- test command output
- test command exit code
- validation todo file for Bob-filled semantic metrics

Bob fills the final metric values.

---

## 6. Validation Commit

The CLI compares final metric values against targets.

The sub-mission passes only if:

- metric targets are satisfied
- changed files are within scope
- forbidden paths were not touched
- test command passes

---

## 7. Parent Mission Validation

The parent mission passes only if:

- all sub-missions passed
- aggregate metrics are satisfied
- parent-level tests pass
- no parent-level forbidden paths were touched

This catches integration issues that may not appear inside a single sub-mission.

---

## 8. Evidence Report

MissionForge generates a Markdown report containing:

- mission goal
- decomposition summary
- dependency structure
- baseline values
- final values
- sub-mission results
- test results
- files changed
- scope violations
- final pass/fail status

This report should be suitable for pull requests, judging artifacts, and team review.

---

# Expected Repository Structure

MissionForge stores its state in a `.missionforge/` workspace.

```text
.missionforge/
├── config.yaml
└── missions/
    └── FG-001/
        ├── mission.yaml
        ├── plan.yaml
        ├── validation.json
        ├── report.md
        └── sub-missions/
            ├── FG-001-A/
            │   ├── sub-mission.yaml
            │   ├── baseline.todo.json
            │   ├── baseline.json
            │   ├── validation.todo.json
            │   └── validation.json
            ├── FG-001-B/
            ├── FG-001-C/
            └── FG-001-D/
```

The CLI owns this state format. The Board reads from it.

---

# Product Architecture

## Phase 1 Architecture

Phase 1 is terminal-first.

```text
Bob
 │
 │ uses commands and fills structured files
 ▼
MissionForge CLI
 │
 │ creates, validates, and updates
 ▼
.missionforge/ workspace
 │
 │ produces
 ▼
Evidence report
```

Phase 1 must be fully functional without the web UI.

---

## Phase 2 Architecture

Phase 2 adds a web UI and watsonx.ai integrations.

```text
MissionForge CLI
 │
 ▼
.missionforge/ workspace
 │
 ▼
Mission Board Backend
 │
 ├── reads mission state
 ├── optionally triggers safe CLI commands
 └── sends mission context to watsonx.ai
          │
          ▼
Mission Board Frontend
 ├── Kanban board
 ├── mission detail panel
 ├── report renderer
 ├── Mission Chat
 └── Stakeholder View
```

The CLI remains the source of truth.

---

# Development Phases

# Phase 1: Core CLI Harness and Bob Workflow

## Phase Goal

Build the minimum complete version of MissionForge as a CLI-first harness that can support a full mission lifecycle from mission creation to validation and evidence reporting.

Phase 1 should prove the core product claim:

> Bob measures the code. MissionForge measures the mission.

The output of this phase should be a working CLI, a usable Bob Skill, slash commands, and a successful terminal-driven demo using a real modernization mission.

---

## 1. CLI Project Setup

### Objective

Create the basic CLI application structure and establish the local MissionForge workspace format.

### Tasks

- Set up the CLI project structure.
- Choose and configure the CLI framework.
- Implement the base `missionforge` command.
- Add CLI help text and command grouping.
- Define the `.missionforge/` workspace directory.
- Implement workspace path resolution from the repository root.
- Add basic error handling for missing workspace, invalid paths, and invalid mission IDs.

### Expected Output

A developer can run:

```bash
missionforge --help
```

and see the available MissionForge commands.

---

## 2. Mission Workspace Initialization

### Objective

Allow developers to initialize a new parent mission workspace.

### Tasks

- Implement:

```bash
missionforge init FG-001
```

- Generate the parent mission directory.
- Create the initial mission file template.
- Create the expected folder structure for the mission.
- Prevent accidental overwrite of existing missions.
- Validate mission ID format.
- Add helpful terminal output after successful initialization.

### Expected Output

The command creates:

```text
.missionforge/
└── missions/
    └── FG-001/
        ├── mission.yaml
        ├── plan.yaml
        ├── sub-missions/
        └── report.md
```

---

## 3. Parent Mission Schema and Validation

### Objective

Validate the parent mission contract before Bob begins decomposition.

### Tasks

- Define the parent mission YAML schema.
- Required fields should include:
  - `id`
  - `goal`
  - `forbidden_paths`
  - `aggregate_metrics`
  - `test_command`
  - `sub_missions`
- Validate YAML syntax.
- Validate required fields.
- Validate mission ID consistency.
- Validate path/glob format.
- Validate aggregate metric fields.
- Validate test command presence.
- Implement:

```bash
missionforge mission FG-001 --validate
```

### Expected Output

The CLI clearly reports whether the mission file is valid or what must be fixed.

---

## 4. Sub-Mission Schema

### Objective

Define the structure for independently executable sub-missions.

### Tasks

- Define the sub-mission YAML schema.
- Required fields should include:
  - `id`
  - `parent`
  - `title`
  - `goal`
  - `depends_on`
  - `allowed_paths`
  - `metrics`
  - `test_command`
- Validate sub-mission ID format.
- Validate parent mission reference.
- Validate dependency references.
- Validate allowed paths.
- Validate metric definitions.
- Validate test command presence.

### Expected Output

MissionForge can validate whether Bob-generated sub-missions are structurally correct.

---

## 5. Bob Decomposition Workflow

### Objective

Support the step where Bob decomposes a parent mission into smaller sub-missions.

### Tasks

- Implement:

```bash
missionforge decompose FG-001
```

- Make the command produce clear instructions for Bob.
- Ensure Bob writes sub-mission files through the expected structure.
- Ensure Bob writes or updates `plan.yaml`.
- Define what information `plan.yaml` must contain:
  - parent mission ID
  - sub-mission list
  - dependency graph
  - execution order
  - decomposition rationale
- Add validation after decomposition.
- Add clear terminal output showing generated sub-missions.

### Expected Output

After decomposition, the mission has a set of valid sub-mission files and a plan file that explains the execution structure.

---

## 6. Dependency Graph Planning

### Objective

Allow the CLI to validate and resolve the execution order of sub-missions.

### Tasks

- Implement:

```bash
missionforge plan FG-001
```

- Read all sub-mission definitions.
- Validate that all dependencies exist.
- Detect dependency cycles.
- Detect invalid parent references.
- Detect overlapping or conflicting allowed paths.
- Compute topological execution order.
- Write the resolved plan to `plan.yaml`.
- Display ready and blocked sub-missions.

### Expected Output

MissionForge can determine the correct order of execution and identify invalid dependency structures before implementation begins.

---

## 7. Next Sub-Mission Selection

### Objective

Allow the developer or Bob to determine which sub-mission is ready to execute next.

### Tasks

- Implement:

```bash
missionforge next FG-001
```

- Read the dependency graph.
- Read validation status of completed sub-missions.
- Determine which sub-missions are ready.
- Mark blocked sub-missions and explain why they are blocked.
- For Phase 1, return one recommended next sub-mission.
- Also display all currently ready sub-missions to show latent parallelism.

### Expected Output

The CLI can guide the team through a sequential execution flow while still showing which work could eventually run in parallel.

---

## 8. Baseline Capture Flow

### Objective

Create the baseline measurement workflow for each sub-mission.

### Tasks

- Implement:

```bash
missionforge baseline FG-001-A --capture
```

- Generate `baseline.todo.json` from the sub-mission metrics.
- Include metric IDs, descriptions, expected baseline targets, and empty value fields.
- Make the file easy for Bob to fill.
- Prevent capture if a baseline has already been committed unless explicitly reset.

### Expected Output

Each sub-mission can produce a structured baseline measurement file that Bob can fill after reading the scoped code.

---

## 9. Baseline Commit Flow

### Objective

Freeze completed baseline measurements before implementation begins.

### Tasks

- Implement:

```bash
missionforge baseline FG-001-A --commit
```

- Validate that all baseline fields are filled.
- Validate field types against metric definitions.
- Write immutable `baseline.json`.
- Prevent accidental modification after commit.
- Record timestamp and status metadata.
- Report baseline summary in the terminal.

### Expected Output

Each sub-mission has an auditable baseline that can be compared against final validation results.

---

## 10. Sub-Mission Validation Capture

### Objective

Capture deterministic validation evidence after Bob completes a sub-mission.

### Tasks

- Implement:

```bash
missionforge validate FG-001-A --capture
```

- Run git diff to identify changed files.
- Compare changed files against allowed paths.
- Compare changed files against parent forbidden paths.
- Run the sub-mission test command.
- Record test command output and exit code.
- Generate `validation.todo.json` for Bob-filled metric results.
- Include deterministic evidence in the validation todo file.

### Expected Output

MissionForge captures scope, diff, and test evidence without needing to understand source code semantics.

---

## 11. Sub-Mission Validation Commit

### Objective

Finalize sub-mission validation by comparing metric results against targets.

### Tasks

- Implement:

```bash
missionforge validate FG-001-A --commit
```

- Validate that Bob-filled metric values are complete.
- Compare final values against target values.
- Determine pass/fail status for each metric.
- Determine overall sub-mission status.
- Write `validation.json`.
- Report result clearly in the terminal.
- Block dependent sub-missions if validation fails.

### Expected Output

Each sub-mission has a structured pass/fail validation record.

---

## 12. Parent Mission Validation

### Objective

Validate the full mission after all sub-missions are complete.

### Tasks

- Implement:

```bash
missionforge validate FG-001
```

- Confirm all sub-missions have passed validation.
- Run parent-level test command.
- Check aggregate mission metrics.
- Check that no forbidden paths were touched across all sub-missions.
- Generate parent-level `validation.json`.
- Clearly report whether the parent mission passed or failed.

### Expected Output

MissionForge can prove that the full mission passed both local sub-mission checks and global integration checks.

---

## 13. Evidence Report Generation

### Objective

Generate a PR-ready report summarizing the completed mission.

### Tasks

- Implement:

```bash
missionforge report FG-001
```

- Generate `report.md`.
- Include:
  - mission goal
  - mission status
  - decomposition summary
  - dependency graph summary
  - sub-mission results
  - baseline and final metric values
  - test results
  - changed files
  - forbidden path violations
  - next suggested mission, if available
- Use a clean Markdown template.
- Ensure the report can be attached to a pull request or submitted as a judging artifact.

### Expected Output

A readable evidence report exists for the completed mission.

---

## 14. Bob Skill

### Objective

Teach Bob how to use MissionForge correctly.

### Tasks

- Write `SKILL.md`.
- Explain the core rule:

```text
Bob measures the code. MissionForge measures the mission.
```

- Define the workflow:
  - initialize
  - validate parent mission
  - decompose
  - plan
  - capture baseline
  - implement
  - capture validation
  - commit validation
  - generate report
- Explain what Bob should and should not do.
- Explain that Bob should not bypass the CLI by directly mutating MissionForge state files unless explicitly allowed.
- Include example prompts and command usage.

### Expected Output

Bob can follow the MissionForge workflow consistently during the demo.

---

## 15. Slash Commands

### Objective

Create convenient Bob slash commands for common MissionForge actions.

### Tasks

Create slash commands such as:

- `/mf-init`
- `/mf-decompose`
- `/mf-plan`
- `/mf-next`
- `/mf-baseline`
- `/mf-validate`
- `/mf-report`

Each command should:

- Explain what it does.
- Run the relevant CLI command.
- Tell Bob what to read next.
- Tell Bob what file to fill or inspect.
- Keep Bob aligned with the MissionForge workflow.

### Expected Output

Bob can operate MissionForge through short, repeatable workflow commands.

---

## 16. Demo Mission Preparation

### Objective

Prepare the first end-to-end modernization mission for the hackathon demo.

### Tasks

- Confirm the demo codebase runs end-to-end.
- Select the first mission scope.
- Write the parent `mission.yaml`.
- Define forbidden paths.
- Define aggregate metrics.
- Define test commands.
- Prepare integration tests.
- Confirm the modernization is manually achievable.
- Run a dry-run of the mission flow.
- Adjust scope if the mission is too large.

### Expected Output

The team has a realistic and recordable mission that can be executed through MissionForge.

---

## 17. Phase 1 Acceptance Criteria

Phase 1 is complete when:

- The CLI can initialize a mission.
- Parent mission validation works.
- Bob can decompose a parent mission into sub-missions.
- The CLI can validate the dependency graph.
- The CLI can identify the next executable sub-mission.
- Baseline capture and commit work.
- Sub-mission validation capture and commit work.
- Parent-level validation works.
- Evidence report generation works.
- Bob Skill and slash commands are usable.
- A terminal-only demo can show the complete mission lifecycle.

---

# Phase 2: Mission Board and Watsonx.ai Layer

## Phase Goal

Build the visual and stakeholder-facing layer on top of the Phase 1 CLI harness.

Phase 2 should make MissionForge easier to understand, easier to demo, and more useful for non-engineering stakeholders.

The CLI remains the source of truth. The Mission Board is a view and control layer over the `.missionforge/` state.

---

## 1. Board Backend Setup

### Objective

Create a backend that reads MissionForge state and exposes it to the web UI.

### Tasks

- Create the backend project structure.
- Use FastAPI or a similar lightweight backend.
- Implement repository root detection.
- Read `.missionforge/` mission state.
- Expose mission list endpoint.
- Expose mission detail endpoint.
- Expose sub-mission detail endpoint.
- Add error handling for missing or invalid mission state.
- Keep backend read-only initially.

### Expected Output

The frontend can request mission data through HTTP endpoints.

---

## 2. CLI Wrapper Endpoints

### Objective

Allow the Board to trigger selected CLI commands through the backend.

### Tasks

- Add backend endpoints for safe CLI actions.
- Supported actions may include:
  - validate mission
  - generate report
  - refresh mission state
  - approve mission
- Execute CLI commands as subprocesses.
- Capture command output.
- Return structured success or failure responses.
- Avoid allowing arbitrary shell command execution.

### Expected Output

The Board can trigger safe MissionForge commands while the CLI remains the source of truth.

---

## 3. Frontend Project Setup

### Objective

Create the Mission Board frontend.

### Tasks

- Set up Next.js project.
- Configure Tailwind CSS.
- Create base layout.
- Create mission board route.
- Create mission detail route or side panel.
- Set up frontend API client.
- Add loading, empty, and error states.

### Expected Output

A basic web UI can connect to the backend and display mission data.

---

## 4. Parent Mission Board

### Objective

Display parent missions in a Kanban-style board.

### Tasks

- Create parent mission card component.
- Create parent mission status columns:
  - Drafted
  - Approved
  - Decomposing
  - In Progress
  - Validating
  - Done
  - Blocked
- Show mission ID.
- Show one-line goal summary.
- Show overall progress.
- Show test status.
- Show forbidden path violation count.
- Add expand or click behavior.

### Expected Output

Users can see the status of all parent missions at a glance.

---

## 5. Sub-Mission Visualization

### Objective

Show sub-missions under their parent mission.

### Tasks

- Create sub-mission card component.
- Display:
  - sub-mission ID
  - title
  - status
  - dependencies
  - test status
  - metric progress
- Render sub-missions when a parent mission is expanded.
- Group sub-missions by dependency level.
- Highlight ready sub-missions.
- Highlight blocked sub-missions.
- Show the latent parallelism when multiple sub-missions are ready.

### Expected Output

The Board visually explains how the mission is decomposed and what can be worked on next.

---

## 6. Dependency Graph View

### Objective

Render the sub-mission dependency structure in a clear visual format.

### Tasks

- Read dependency data from `plan.yaml`.
- Create a simple dependency diagram.
- Show arrows or connectors between sub-missions.
- Highlight completed, ready, blocked, and failed nodes.
- Keep the graph readable for the demo mission.

### Expected Output

Users can understand mission order and dependencies without reading YAML.

---

## 7. Mission Detail Panel

### Objective

Show detailed evidence for a selected mission or sub-mission.

### Tasks

For parent missions, display:

- mission goal
- aggregate metrics
- dependency graph
- sub-mission list
- parent validation status
- parent test result
- rendered evidence report

For sub-missions, display:

- sub-mission goal
- allowed paths
- dependencies
- baseline metrics
- final metrics
- changed files
- test result
- validation status

### Expected Output

Clicking a mission card gives enough information to review the mission.

---

## 8. Report Renderer

### Objective

Render the generated Markdown evidence report in the Board.

### Tasks

- Read `report.md`.
- Render Markdown in the UI.
- Style headings, tables, code blocks, and lists.
- Add download or copy button.
- Show report generation status.
- Show a helpful message if no report exists yet.

### Expected Output

Reviewers can read the evidence report directly inside the Mission Board.

---

## 9. Polling-Based Updates

### Objective

Make the Board update as the CLI state changes.

### Tasks

- Poll the backend every few seconds.
- Refresh mission list and selected mission details.
- Avoid excessive requests.
- Preserve selected mission state while refreshing.
- Show a subtle refresh indicator.
- No WebSockets required for Phase 2.

### Expected Output

The Board updates during the demo while Bob and the CLI change mission state.

---

## 10. Watsonx.ai Mission Chat

### Objective

Allow users to ask questions about mission state from the Board.

### Tasks

- Add Watsonx.ai credentials through environment variables.
- Implement backend mission chat endpoint.
- Gather grounding context from:
  - mission file
  - plan file
  - baseline files
  - validation files
  - report file
  - git diff summary, if available
- Create a system prompt that restricts answers to mission state.
- Add chat UI in the mission detail panel.
- Stream or display responses.
- Add loading and error states.
- Cache repeated responses where appropriate.

### Expected Output

Users can ask questions like:

```text
Why is this mission blocked?
Which files changed?
Why are these two sub-missions independent?
Summarize this mission for a standup update.
```

and receive grounded answers from mission state.

---

## 11. Stakeholder Translation

### Objective

Translate technical mission state into business-friendly summaries.

### Tasks

- Implement backend stakeholder summary endpoint.
- Use Watsonx.ai to generate:
  - one-sentence business summary
  - status
  - percent complete
  - risk callouts
  - user impact
- Return structured JSON.
- Cache output until mission state changes.
- Add stakeholder view toggle in the frontend.
- Display business-friendly mission cards or detail panels.

### Expected Output

Non-engineers can understand what the mission accomplished and whether it is risky.

---

## 12. Demo Polish

### Objective

Make the Mission Board visually compelling for the final video.

### Tasks

- Improve card spacing and layout.
- Add clear status colors.
- Add progress indicators.
- Add metric progress strips.
- Add empty states.
- Add success and failure states.
- Make the dependency diamond clear.
- Ensure the UI is readable in screen recordings.
- Prepare a stable demo dataset if live state becomes unreliable.

### Expected Output

The Mission Board clearly communicates the value of MissionForge in a recorded demo.

---

## 13. Final Submission Assets

### Objective

Package the project for hackathon judging.

### Tasks

- Write README.
- Document installation steps.
- Document CLI workflow.
- Document Bob Skill setup.
- Document Mission Board setup.
- Add screenshots.
- Add demo video script.
- Record final video.
- Export Bob session evidence.
- Attach generated report.
- Prepare judging explanation.

### Expected Output

The team has a complete submission package with code, documentation, demo video, and evidence artifacts.

---

## 14. Phase 2 Acceptance Criteria

Phase 2 is complete when:

- The Board can read MissionForge mission state.
- Parent missions are shown in a Kanban-style view.
- Sub-missions can be expanded and reviewed.
- Dependency structure is visible.
- Mission detail panel works.
- Evidence reports render in the UI.
- The Board updates as mission state changes.
- Mission Chat works with Watsonx.ai.
- Stakeholder Translation works with Watsonx.ai.
- The UI is polished enough for a recorded demo.

---

# Development Priority

## Must Finish

These are required for the project to be viable:

1. CLI mission initialization
2. Parent mission validation
3. Sub-mission validation
4. Dependency planning
5. Baseline capture and commit
6. Validation capture and commit
7. Parent mission validation
8. Evidence report generation
9. Bob Skill
10. Demo mission

## Should Finish

These make the project easier to demo and explain:

1. Slash commands
2. Mission Board backend
3. Mission Board frontend
4. Mission detail panel
5. Report renderer

## Nice to Have

These increase polish and judging impact:

1. Watsonx.ai Mission Chat
2. Stakeholder Translation
3. Dependency graph visualization
4. Board-triggered CLI actions
5. Final UI polish

## Cut First If Time Runs Short

Cut in this order:

1. Board-triggered CLI actions
2. Stakeholder Translation
3. Mission Chat
4. Dependency graph visual polish
5. Mission Board entirely

Do not cut the CLI harness, Bob workflow, evidence report, or demo mission.
