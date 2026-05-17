---
name: missionforge
description: "MissionForge mission workflow for AI agents. Bob measures the code; MissionForge measures the mission. Use when managing missions: init, decompose, plan, baseline capture/commit, validate, and report generation. Works with Claude Code, OpenCode, Cursor, Antigravity, GitHub Copilot, and any agent that runs shell commands."
---

# MissionForge Workflow Skill

## Core Principle

**"Bob measures the code. MissionForge measures the mission."**

This skill guides AI agents through the complete MissionForge workflow for managing complex software development missions with measurable outcomes.

### Division of Responsibility

**Bob (AI Agent) Responsibilities:**
- Analyze codebase structure and understand code
- Create sub-mission decomposition
- Measure metrics (test coverage, line counts, complexity, etc.)
- Fill `.todo.json` files with measured values
- Implement code changes within `allowed_paths`
- Make architectural decisions

**MissionForge CLI Responsibilities:**
- Run git diff (deterministic file changes)
- Execute test commands
- Validate file paths against patterns
- Check scope (`allowed_paths`, `forbidden_paths`)
- Resolve dependency graphs
- Validate YAML schemas
- Create immutable audit files (`.json`)
- Generate reports

---

## Complete Workflow

```
┌──────────────┐
│  1. INIT     │  missionforge init MF-001
└──────┬───────┘
       ▼
┌──────────────┐
│  2. MISSION  │  missionforge mission MF-001 --validate
│   VALIDATE   │  (Bob edits mission.yaml)
└──────┬───────┘
       ▼
┌──────────────┐
│ 3. DECOMPOSE │  missionforge decompose MF-001
│              │  (Bob creates sub-mission YAMLs)
└──────┬───────┘
       ▼
┌──────────────┐
│  4. PLAN     │  missionforge plan MF-001
└──────┬───────┘
       ▼
┌──────────────┐
│  5. NEXT     │  missionforge plan MF-001
│              │  (Shows next ready sub-mission)
└──────┬───────┘
       ▼
┌─────────────────────────────────────┐
│  FOR EACH SUB-MISSION:              │
│  6. BASELINE CAPTURE                │
│  7. BASELINE COMMIT                 │
│  8. IMPLEMENT                       │
│  9. VALIDATE CAPTURE                │
│  10. VALIDATE COMMIT                │
└─────────────────┬───────────────────┘
                  ▼
┌──────────────┐
│11. VALIDATE  │  missionforge validate parent MF-001
│    PARENT    │
└──────┬───────┘
       ▼
┌──────────────┐
│12. REPORT    │  missionforge plan MF-001
└──────────────┘
```

---

## Installation

### For Claude Code Users
Commands are automatically available when you open this project.
Use `/mf-*` slash commands in the chat.

### For OpenCode Users
Commands are automatically discovered from `.opencode/commands/`.
Use `/mf-*` commands in the chat interface.

### For Antigravity Users
Commands are automatically discovered from `.antigravity/commands/`.
Use `/mf-*` commands in the chat interface.

### For GitHub Copilot Users
Workspace commands are automatically available.
Use `/mf-*` commands in Copilot Chat.

### For Cursor Users
Commands are automatically discovered from `.cursor/commands/`.
Use `/mf-*` commands in the chat interface.

### For Codex Users
Commands are automatically discovered from `.codex/commands/`.
Use `/mf-*` commands in the chat interface.

### For Other Agents (Universal)
Install via skills.sh:
```bash
npx skills add <owner>/Mission-Forge
```

Then follow the workflow documentation in this skill file.

---

## Mission ID Format

### Parent Mission
**Pattern:** `^[A-Z]{2,4}-\d{3}[A-Z]?$`

**Examples:**
- `MF-001` ✓
- `PROJ-042` ✓
- `FG-123A` ✓
- `MF-001-A` ✗ (this is a sub-mission)

### Sub-Mission
**Pattern:** `^[A-Z]{2,4}-\d{3}-[A-Z]$`

**Examples:**
- `MF-001-A` ✓
- `PROJ-042-B` ✓
- `FG-123-C` ✓
- `MF-001` ✗ (this is a parent mission)

---

## Workspace File Structure

```
.missionforge/
└── missions/
    └── MF-001/
        ├── mission.yaml          # Parent mission definition
        ├── plan.yaml             # Execution plan (generated)
        ├── report.md             # Final report (generated)
        └── sub-missions/
            ├── MF-001-A.yaml     # Sub-mission definition
            ├── MF-001-A/
            │   ├── baseline.todo.json   # Bob fills this
            │   ├── baseline.json        # Immutable after commit
            │   ├── validation.todo.json # Bob fills this
            │   └── validation.json      # Immutable after commit
            ├── MF-001-B.yaml
            ├── MF-001-B/
            │   └── ...
            └── ...
```

---

## What Bob MUST Do

✅ **Fill `.todo.json` files** with measured metric values  
✅ **Read scoped code** within `allowed_paths` only  
✅ **Measure metrics accurately** (test coverage, line counts, etc.)  
✅ **Implement changes** within scope  
✅ **Use exact measurement methods** for baseline and validation  
✅ **Validate after each step** to catch errors early  
✅ **Document rationale** in decomposition  

---

## What Bob MUST NOT Do

❌ **Mutate committed `.json` files** directly (baseline.json, validation.json)  
❌ **Bypass CLI commands** (always use missionforge CLI)  
❌ **Skip validation steps** (validate after each phase)  
❌ **Work outside `allowed_paths`** (respect scope boundaries)  
❌ **Modify `forbidden_paths`** (these are off-limits)  
❌ **Leave metrics unfilled** (all values required before commit)  
❌ **Use different measurement methods** between baseline and validation  

---

## Metric Measurement Guide

### Common Metric Types

#### 1. Test Coverage (float)
**Measure:**
```bash
# Python
pytest --cov=src/module --cov-report=term

# JavaScript
jest --coverage
```
**Example:** `78.5` → `87.2` (target: `85.0`)

#### 2. Lines Added/Removed (int)
**Measure:**
```bash
git diff --stat baseline_commit..HEAD
```
**Example:** `0` → `342`

#### 3. Boolean Metrics (bool)
**Measure:** Pattern search, file existence
```bash
grep -r "RestEndpoint" src/module/
test -f src/api/rest_endpoint.py && echo "true"
```
**Example:** `rest_endpoint_exists: false` → `true`

#### 4. Count Metrics (int)
**Measure:**
```bash
grep -r "CORBA" src/module/ | wc -l
```
**Example:** `corba_references_count: 7` → `0`

#### 5. Complexity Metrics (int/float)
**Measure:**
```bash
# Python
radon cc src/module/ -a

# JavaScript
cr src/module/
```
**Example:** `avg_complexity: 12.3` → `7.5`

#### 6. Performance Metrics (float)
**Measure:** Benchmarks, timing
```bash
pytest tests/benchmark_test.py --benchmark-only
time python src/module/main.py
```
**Example:** `api_response_time_ms: 250.0` → `85.0`

### Measurement Best Practices

1. **Consistency:** Use the SAME measurement method for baseline and validation
2. **Scope Awareness:** Only measure within `allowed_paths`
3. **Accuracy:** Take time to measure correctly, verify edge cases
4. **Documentation:** Comment your measurement approach if non-obvious
5. **Automation:** Create measurement scripts for repeatability

### Measurement Workflow

**Baseline Phase:**
1. CLI creates `baseline.todo.json` with empty metric values
2. Bob analyzes code within `allowed_paths`
3. Bob measures each metric using appropriate tools
4. Bob fills all metric values in `baseline.todo.json`
5. Bob runs `missionforge baseline commit <SUB_ID>`
6. CLI validates and creates immutable `baseline.json`

**Validation Phase:**
1. CLI creates `validation.todo.json` with empty metric values
2. Bob analyzes FINAL code state within `allowed_paths`
3. Bob measures each metric using SAME methods as baseline
4. Bob fills all metric values in `validation.todo.json`
5. Bob runs `missionforge validate commit <SUB_ID>`
6. CLI compares baseline → target → final, determines PASS/FAIL

---

## Bob's Responsibilities by Phase

### Phase 1: Decompose
- Analyze codebase structure
- Understand parent mission goal
- Break down into logical sub-missions
- Create sub-mission YAML files
- Define `allowed_paths` for each sub-mission
- Set dependencies between sub-missions
- Validate each sub-mission with `validate-submission`

### Phase 2: Baseline
- Read sub-mission `allowed_paths`
- Analyze current code state
- Measure all metrics accurately
- Fill `baseline.todo.json` with measured values
- Verify no values are null/missing
- Commit baseline

### Phase 3: Implementation
- Implement changes within `allowed_paths` only
- Respect `forbidden_paths` boundaries
- Run tests locally
- Ensure code quality
- Stay within scope

### Phase 4: Validation
- Measure final code state
- Use SAME measurement methods as baseline
- Fill `validation.todo.json` with final values
- Compare against targets
- Commit validation
- Review PASS/FAIL status

---

## Example Prompts

### Initialization
- "Initialize mission MF-001 for REST API migration"
- "Create new mission PROJ-042 for authentication refactor"
- "Set up mission workspace for database migration"

### Mission Validation
- "Validate mission MF-001 configuration"
- "Check if mission.yaml is properly formatted"
- "Fix validation errors in parent mission"

### Decomposition
- "Decompose MF-001 into sub-missions for auth, data, and UI layers"
- "Break down the migration into logical sub-missions"
- "Create sub-missions for MF-001 based on module structure"
- "Analyze codebase and create 3-5 sub-missions"

### Planning
- "Generate execution plan for MF-001"
- "Create dependency graph and execution order"
- "Show me the plan for mission MF-001"

### Baseline
- "Capture baseline for MF-001-A"
- "Measure current test coverage for auth module"
- "Fill baseline metrics for sub-mission A"
- "Commit baseline after filling all metrics"

### Implementation
- "Implement MF-001-A: migrate auth module to REST"
- "Complete the authentication refactor for sub-mission A"
- "Make changes for MF-001-B within allowed paths"

### Validation
- "Validate MF-001-A implementation"
- "Measure final metrics for auth module"
- "Fill validation metrics and check against targets"
- "Commit validation after verifying all targets met"

### Reporting
- "Generate final report for MF-001"
- "Show me the mission completion evidence"
- "Create report for completed mission"

---

## Troubleshooting

### Error: "baseline.json is immutable"
**Cause:** Trying to modify committed baseline  
**Fix:** Use `missionforge baseline reset MF-001-A --force` to reset

### Error: "Metric value missing in todo.json"
**Cause:** Not all metrics filled before commit  
**Fix:** Fill all metric values in `.todo.json` file before running commit

### Error: "Path outside allowed_paths"
**Cause:** Modified files not matching `allowed_paths` patterns  
**Fix:** Only modify files within `allowed_paths`, check patterns

### Error: "Circular dependency detected"
**Cause:** Sub-missions have circular dependencies  
**Fix:** Remove one dependency to break the cycle, update sub-mission YAMLs

### Error: "Sub-mission validation failed"
**Cause:** One or more metrics didn't meet targets  
**Fix:** Check `validation.json` for specific metric failures, review implementation

### Error: "Parent validation failed despite all sub-missions passing"
**Cause:** Aggregate metrics or forbidden_paths violations  
**Fix:** Check aggregate metrics and forbidden_paths violations in parent validation

### Error: "Invalid mission ID format"
**Cause:** Mission ID doesn't match required pattern  
**Fix:** Use format `[A-Z]{2,4}-\d{3}[A-Z]?` for parent, `[A-Z]{2,4}-\d{3}-[A-Z]` for sub-mission

### Error: "Cannot find .missionforge directory"
**Cause:** Not in a MissionForge workspace  
**Fix:** Run `missionforge init <ID>` to create workspace, or navigate to project root

### Error: "Dependency not found"
**Cause:** Sub-mission depends on non-existent sub-mission  
**Fix:** Create the dependency first or remove it from `depends_on`

### Error: "Test command failed"
**Cause:** Tests didn't pass  
**Fix:** Fix failing tests before committing validation

---

## Best Practices

### 1. Logical Decomposition
Break missions into logical, independent units:
- ✓ By feature/module
- ✓ By layer (frontend/backend)
- ✓ By concern (data/logic/UI)
- ✗ Too granular (creates overhead)
- ✗ Too broad (loses focus)

### 2. Clear Dependencies
Define dependencies explicitly:
```yaml
# Backend must complete before frontend
depends_on:
  - MF-001-A  # Backend API
```

### 3. Non-Overlapping Paths
Keep sub-missions independent:
```yaml
# Good - separate modules
MF-001-A: ["src/auth/**"]
MF-001-B: ["src/api/**"]

# Bad - overlapping
MF-001-A: ["src/**"]
MF-001-B: ["src/api/**"]  # Overlaps with A
```

### 4. Meaningful Metrics
Set realistic, measurable targets:
```yaml
metrics:
  test_coverage:
    min: 80.0      # Minimum acceptable
    target: 90.0   # Ideal goal
  lines_added:
    max: 500       # Keep changes manageable
```

### 5. Validate Frequently
Validate after each step to catch errors early:
```bash
# After creating sub-mission
missionforge validate-submission MF-001 MF-001-A

# After filling baseline
missionforge baseline commit MF-001-A

# After implementation
missionforge validate commit MF-001-A
```

### 6. Document Rationale
Explain your decomposition decisions:
```yaml
decomposition_rationale: |
  Split by architectural layers:
  - MF-001-A: Data layer (models, migrations)
  - MF-001-B: API layer (endpoints, serializers)
  - MF-001-C: UI layer (components, views)
  
  This allows parallel development after data layer completes.
```

### 7. Accurate Measurement
Take time to measure correctly:
- Run tools multiple times
- Verify edge cases
- Document measurement method
- Use consistent tools

---

## CLI Command Reference

### Initialization
```bash
missionforge init <MISSION_ID>
```

### Mission Validation
```bash
missionforge mission <MISSION_ID> --validate
```

### Decomposition
```bash
missionforge decompose <MISSION_ID>
missionforge validate-submission <MISSION_ID> <SUB_MISSION_ID>
```

### Planning
```bash
missionforge plan <MISSION_ID>
```

### Baseline
```bash
missionforge baseline capture <SUB_MISSION_ID>
missionforge baseline commit <SUB_MISSION_ID>
missionforge baseline reset <SUB_MISSION_ID> --force
```

### Validation
```bash
missionforge validate capture <SUB_MISSION_ID>
missionforge validate commit <SUB_MISSION_ID>
missionforge validate parent <MISSION_ID>
```

### Workspace
```bash
missionforge workspace status
missionforge workspace init <MISSION_ID>
```

---

## Quick Reference Card

| Phase | Command | Bob's Action |
|-------|---------|--------------|
| Init | `missionforge init MF-001` | Edit mission.yaml |
| Validate | `missionforge mission MF-001 --validate` | Fix errors |
| Decompose | `missionforge decompose MF-001` | Create sub-mission YAMLs |
| Plan | `missionforge plan MF-001` | Review execution order |
| Baseline | `missionforge baseline capture MF-001-A` | Fill baseline.todo.json |
| Baseline | `missionforge baseline commit MF-001-A` | Verify committed |
| Implement | (Bob makes changes) | Code within allowed_paths |
| Validate | `missionforge validate capture MF-001-A` | Fill validation.todo.json |
| Validate | `missionforge validate commit MF-001-A` | Check PASS/FAIL |
| Parent | `missionforge validate parent MF-001` | Review aggregate results |
| Report | `missionforge plan MF-001` | Read report.md |

---

## Support

For issues and questions:
- Check troubleshooting section above
- Review example prompts for guidance
- Consult CLI command reference
- Read metric measurement guide

---

**Made with Bob** 🤖