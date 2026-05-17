# MF-012 Implementation Plan: Bob Skill and Slash Commands

## Overview
Create a cross-agent SKILL.md and 8 slash commands for MissionForge workflow, installable via `npx skills add` (skills.sh ecosystem).

**Core Principle:** "Bob measures the code. MissionForge measures the mission."

---

## Files to Create (12 total)

### 1. CLAUDE.md (Project Root)
**Location:** `/CLAUDE.md`

**Purpose:** Points Claude Code to the MissionForge skill

**Content:**
```markdown
# missionforge
- **missionforge** (`skills/missionforge/SKILL.md`) — MissionForge workflow skill.
Use when running any MissionForge mission workflow.
```

---

### 2. skills/missionforge/SKILL.md (Installable Skill)
**Location:** `/skills/missionforge/SKILL.md`

**Purpose:** Main skill file installable via `npx skills add <owner>/Mission-Forge`

**Frontmatter:**
```yaml
---
name: missionforge
description: "MissionForge mission workflow for AI agents. Bob measures the code; MissionForge measures the mission. Use when managing missions: init, decompose, plan, baseline capture/commit, validate, and report generation. Works with Claude Code, OpenCode, Cursor, Codex, and any agent that runs shell commands."
---
```

**Content Sections:**

1. **Core Principle & Division of Responsibility**
   - Bob's role: Code measurement, metric filling, implementation
   - CLI's role: Deterministic operations (git diff, test execution, file paths)
   - Clear boundaries between agent and CLI responsibilities

2. **Full Ordered Workflow**
   - Step-by-step workflow with exact CLI commands
   - ASCII workflow diagram:
     ```
     init → validate → decompose → plan → baseline → implement → validate → report
     ```

3. **What Bob MUST Do**
   - Fill `.todo.json` files with measured metrics
   - Read scoped code within `allowed_paths`
   - Measure metrics accurately (test coverage, line counts, etc.)
   - Implement changes within scope
   - Never mutate committed `.json` files directly

4. **What Bob MUST NOT Do**
   - Bypass CLI commands
   - Skip validation steps
   - Modify committed baseline.json/validation.json
   - Work outside allowed_paths

5. **Mission ID Format**
   - Parent: `^[A-Z]{2,4}-\d{3}[A-Z]?$` (e.g., `MF-001`, `FG-042A`)
   - Sub-mission: `^[A-Z]{2,4}-\d{3}-[A-Z]$` (e.g., `MF-001-A`, `MF-001-B`)

6. **Workspace File Structure**
   ```
   .missionforge/
   └── missions/
       └── MF-001/
           ├── mission.yaml
           ├── plan.yaml
           ├── sub-missions/
           │   ├── MF-001-A.yaml
           │   ├── MF-001-A/
           │   │   ├── baseline.todo.json  # Bob fills this
           │   │   ├── baseline.json       # Immutable after commit
           │   │   ├── validation.todo.json
           │   │   └── validation.json
           │   └── ...
           └── report.md
   ```

7. **Metric Measurement Details**
   - How to measure test coverage
   - How to count lines added/removed
   - How to verify boolean metrics
   - How to aggregate metrics across files
   - Common metric types and their measurement strategies

8. **Bob's Responsibilities by Phase**
   - **Decompose:** Analyze codebase, create sub-mission YAMLs
   - **Baseline:** Measure current state, fill baseline.todo.json
   - **Implementation:** Make changes within allowed_paths
   - **Validation:** Measure final state, fill validation.todo.json

9. **Example Prompts**
   - "Initialize mission MF-001 for REST API migration"
   - "Decompose MF-001 into sub-missions for auth, data, and UI layers"
   - "Capture baseline for MF-001-A and measure test coverage"
   - "Implement MF-001-A: migrate auth module to REST"
   - "Validate MF-001-A and verify all metrics met targets"

10. **Troubleshooting**
    - **Error:** "baseline.json is immutable"
      - **Fix:** Use `missionforge baseline reset MF-001-A --force` to reset
    - **Error:** "Metric value missing in todo.json"
      - **Fix:** Fill all metric values before running commit
    - **Error:** "Path outside allowed_paths"
      - **Fix:** Only modify files matching allowed_paths patterns
    - **Error:** "Circular dependency detected"
      - **Fix:** Remove one dependency to break the cycle
    - **Error:** "Sub-mission validation failed"
      - **Fix:** Check validation.json for specific metric failures
    - **Error:** "Parent validation failed despite all sub-missions passing"
      - **Fix:** Check aggregate metrics and forbidden_paths violations

11. **Best Practices**
    - Always validate after each step
    - Fill metrics accurately - they're auditable
    - Keep sub-missions focused and independent
    - Use meaningful metric targets
    - Document rationale in decomposition

---

### 3-10. .bob/commands/mf-*.md (8 Canonical Command Docs)
**Location:** `.bob/commands/mf-{command}.md`

**Purpose:** Agent-agnostic canonical documentation for each slash command

**Template Structure:**
```markdown
# /mf-{command}

{One-sentence description}

## Usage
/mf-{command} {args}

## Runs
missionforge {cli-command} $ARGUMENTS

## What Bob Does Next
- **Read:** {file to inspect}
- **Fill:** {file agent must populate} (if applicable)
- **Next command:** /mf-{next-step}

## Example Prompts
- "{example prompt 1}"
- "{example prompt 2}"
- "{example prompt 3}"

## Common Issues
- **Issue:** {common error}
  - **Fix:** {solution}
```

#### Command Details:

**a) /mf-init**
- **CLI:** `missionforge init <ID>`
- **Next:** Edit `mission.yaml`, then `/mf-mission`
- **Example Prompts:**
  - "Initialize mission MF-001 for REST API migration"
  - "Create new mission PROJ-042 for authentication refactor"

**b) /mf-mission**
- **CLI:** `missionforge mission <ID> --validate`
- **Next:** Fix errors, then `/mf-decompose`
- **Example Prompts:**
  - "Validate mission MF-001 configuration"
  - "Check if mission.yaml is properly formatted"

**c) /mf-decompose**
- **CLI:** `missionforge decompose <ID>`
- **Next:** Fill sub-mission YAMLs, validate each with `validate-submission`, then `/mf-plan`
- **Example Prompts:**
  - "Decompose MF-001 into sub-missions for auth, data, and UI"
  - "Break down the migration into logical sub-missions"
  - "Create sub-missions for MF-001 based on module structure"

**d) /mf-plan**
- **CLI:** `missionforge plan <ID>`
- **Next:** Read `plan.yaml`, then `/mf-next`
- **Example Prompts:**
  - "Generate execution plan for MF-001"
  - "Create dependency graph and execution order"

**e) /mf-next**
- **CLI:** `missionforge plan <ID>` (shows next ready sub-mission)
- **Next:** Run `/mf-baseline` on next ready sub-mission
- **Example Prompts:**
  - "What's the next sub-mission to work on?"
  - "Show me which sub-missions are ready to start"

**f) /mf-baseline**
- **CLI:** 
  - Capture: `missionforge baseline capture <SUB_ID>`
  - Commit: `missionforge baseline commit <SUB_ID>`
- **Next:** 
  - After capture: Fill `baseline.todo.json`, then commit
  - After commit: Implement changes
- **Example Prompts:**
  - "Capture baseline for MF-001-A"
  - "Measure current test coverage for auth module"
  - "Commit baseline after filling metrics"

**g) /mf-validate**
- **CLI:**
  - Capture: `missionforge validate capture <SUB_ID>`
  - Commit: `missionforge validate commit <SUB_ID>`
- **Next:**
  - After capture: Fill `validation.todo.json`, then commit
  - After commit: Check if more sub-missions remain, or `/mf-report`
- **Example Prompts:**
  - "Validate MF-001-A implementation"
  - "Measure final metrics for auth module"
  - "Commit validation after verifying all targets met"

**h) /mf-report**
- **CLI:** `missionforge plan <ID>` (generates report.md)
- **Next:** Read `report.md`, confirm evidence
- **Example Prompts:**
  - "Generate final report for MF-001"
  - "Show me the mission completion evidence"

---

### 11. .claude/commands/mf-*.md (8 Claude Code Slash Commands)
**Location:** `.claude/commands/mf-{command}.md`

**Purpose:** Enable `/mf-*` slash commands in Claude Code's command picker

**Content:** Exact copies of `.bob/commands/mf-*.md` files

---

## Implementation Order

1. ✅ Create `CLAUDE.md` (project root)
2. ✅ Create `skills/missionforge/SKILL.md` (the installable skill)
3. ✅ Create `.bob/commands/mf-init.md`
4. ✅ Create `.bob/commands/mf-mission.md`
5. ✅ Create `.bob/commands/mf-decompose.md`
6. ✅ Create `.bob/commands/mf-plan.md`
7. ✅ Create `.bob/commands/mf-next.md`
8. ✅ Create `.bob/commands/mf-baseline.md`
9. ✅ Create `.bob/commands/mf-validate.md`
10. ✅ Create `.bob/commands/mf-report.md`
11. ✅ Create `.claude/commands/` directory
12. ✅ Copy all 8 `.bob/commands/mf-*.md` to `.claude/commands/`

---

## Verification Checklist

- [ ] `npx skills add <owner>/Mission-Forge` installs cleanly
- [ ] Claude Code shows `/mf-*` commands in slash command picker
- [ ] `/mf-init MF-TEST` executes `missionforge init MF-TEST`
- [ ] `/mf-baseline MF-TEST-A --capture` provides guidance for `baseline.todo.json`
- [ ] All CLI command references match README.md
- [ ] All CLI command references match actual implementation in source code
- [ ] No references to nonexistent CLI commands
- [ ] All file paths are correct
- [ ] All metric measurement guidance is accurate
- [ ] Troubleshooting covers common workflow errors

---

## Key Design Decisions

1. **Two-Location Strategy:**
   - `.bob/commands/` = canonical, agent-agnostic
   - `.claude/commands/` = Claude Code specific (copies)
   - Rationale: Single source of truth, easy to sync

2. **skills.sh Compatibility:**
   - Standard frontmatter format
   - Location: `skills/missionforge/SKILL.md`
   - Enables `npx skills add` installation

3. **Command Naming:**
   - Prefix: `/mf-` (short, memorable)
   - Matches CLI command structure
   - Easy to discover via autocomplete

4. **Example Prompts:**
   - Natural language, task-focused
   - Show real-world usage patterns
   - Help agents understand context

5. **Troubleshooting:**
   - Common errors from actual usage
   - Clear, actionable fixes
   - Prevents workflow blockers

---

## Success Criteria

✅ External devs can install with one command: `npx skills add <owner>/Mission-Forge`

✅ Any AI agent (Bob, Claude Code, OpenCode, Cursor, Codex) can follow the workflow

✅ All 8 slash commands work in Claude Code

✅ Clear guidance at every step of the workflow

✅ Agents understand division of responsibility (Bob vs CLI)

✅ Metric measurement is well-documented

✅ Common errors have documented solutions

---

**Made with Bob** 🤖