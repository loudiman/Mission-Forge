# MF-012 Plan Summary: Bob Skill and Slash Commands

## Executive Summary

This plan creates a comprehensive skill system for MissionForge that enables any AI coding agent (Claude Code, OpenCode, Antigravity, GitHub Copilot, Cursor, and more) to effectively manage the full mission workflow through guided shortcuts and clear documentation.

**Core Innovation:** "Bob measures the code. MissionForge measures the mission."

---

## Deliverables

### 52 Files to Create (Multi-Agent Support)

| # | File | Purpose | Lines |
|---|------|---------|-------|
| 1 | `CLAUDE.md` | Points Claude Code to skill | ~5 |
| 2 | `skills/missionforge/SKILL.md` | Installable skill (skills.sh) | ~400 |
| 3-10 | `.bob/commands/mf-*.md` × 8 | Canonical command docs | ~420 |
| 11-18 | `.claude/commands/mf-*.md` × 8 | Claude Code slash commands | ~420 |
| 19-26 | `.opencode/commands/mf-*.md` × 8 | OpenCode commands | ~420 |
| 27-34 | `.antigravity/commands/mf-*.md` × 8 | Antigravity commands | ~420 |
| 35-42 | `.copilot/commands/mf-*.md` × 8 | GitHub Copilot commands | ~420 |
| 43-50 | `.cursor/commands/mf-*.md` × 8 | Cursor commands | ~420 |
| 51-52 | Config files | Optional agent configs | ~20 |

**Total:** 52 files, ~2,945 lines of documentation

---

## Key Features

### 1. Universal Multi-Agent Support
- Works with Claude Code, OpenCode, Antigravity, GitHub Copilot, Cursor, and any agent via skills.sh
- Agent-agnostic canonical docs in `.bob/commands/`
- Agent-specific command directories for 5 major agents
- Single source of truth, easy to maintain

### 2. One-Command Installation
```bash
npx skills add <owner>/Mission-Forge
```
External developers get the full skill system instantly.

### 3. Complete Workflow Coverage
```
init → validate → decompose → plan → next → baseline → implement → validate → report
```
Every step has a dedicated slash command with clear guidance.

### 4. Enhanced Documentation

#### SKILL.md Includes:
- **Core Principle:** Division of responsibility (Bob vs CLI)
- **Full Workflow:** Step-by-step with exact commands
- **ASCII Diagram:** Visual workflow representation
- **Bob's Responsibilities:** What agents MUST and MUST NOT do
- **Metric Measurement:** Detailed guide for all metric types
- **Example Prompts:** Natural language task examples
- **Troubleshooting:** Common errors with solutions
- **Best Practices:** Proven patterns for success

#### Command Docs Include:
- **Usage:** Exact syntax
- **CLI Mapping:** What command it runs
- **Next Steps:** Clear guidance on what to do after
- **Example Prompts:** 3+ real-world usage examples
- **Common Issues:** Errors and fixes

---

## Workflow Overview

### Complete Mission Lifecycle

```
┌──────────────┐
│  1. INIT     │  /mf-init MF-001
└──────┬───────┘
       ▼
┌──────────────┐
│  2. MISSION  │  /mf-mission MF-001 --validate
└──────┬───────┘
       ▼
┌──────────────┐
│ 3. DECOMPOSE │  /mf-decompose MF-001
└──────┬───────┘
       ▼
┌──────────────┐
│  4. PLAN     │  /mf-plan MF-001
└──────┬───────┘
       ▼
┌──────────────┐
│  5. NEXT     │  /mf-next MF-001
└──────┬───────┘
       ▼
┌─────────────────────────────────┐
│  FOR EACH SUB-MISSION:          │
│  6. BASELINE CAPTURE            │
│  7. BASELINE COMMIT             │
│  8. IMPLEMENT                   │
│  9. VALIDATE CAPTURE            │
│  10. VALIDATE COMMIT            │
└─────────────────────────────────┘
       ▼
┌──────────────┐
│11. VALIDATE  │  missionforge validate parent MF-001
│    PARENT    │
└──────┬───────┘
       ▼
┌──────────────┐
│12. REPORT    │  /mf-report MF-001
└──────────────┘
```

---

## Division of Responsibility

### Bob (AI Agent) Responsibilities
✅ Analyzes codebase structure  
✅ Creates sub-mission decomposition  
✅ Measures metrics (coverage, lines, complexity)  
✅ Fills `.todo.json` files with measured values  
✅ Implements code changes within `allowed_paths`  
✅ Reads and understands code  
✅ Makes architectural decisions  

### MissionForge CLI Responsibilities
✅ Runs git diff (deterministic file changes)  
✅ Executes test commands  
✅ Validates file paths against patterns  
✅ Checks scope (`allowed_paths`, `forbidden_paths`)  
✅ Resolves dependency graphs  
✅ Validates YAML schemas  
✅ Creates immutable audit files (`.json`)  
✅ Generates reports  

---

## Metric Measurement Guide

### Common Metric Types

1. **Test Coverage (float)**
   - Measure: `pytest --cov=src/module --cov-report=term`
   - Example: `78.5` → `87.2` (target: `85.0`)

2. **Lines Added/Removed (int)**
   - Measure: `git diff --stat`
   - Example: `0` → `342`

3. **Boolean Metrics (bool)**
   - Measure: Pattern search, file existence
   - Example: `rest_endpoint_exists: false` → `true`

4. **Count Metrics (int)**
   - Measure: `grep -r "PATTERN" | wc -l`
   - Example: `corba_references_count: 7` → `0`

5. **Complexity Metrics (int/float)**
   - Measure: `radon cc src/module/ -a`
   - Example: `avg_complexity: 12.3` → `7.5`

6. **Performance Metrics (float)**
   - Measure: Benchmarks, timing
   - Example: `api_response_time_ms: 250.0` → `85.0`

### Measurement Workflow

**Baseline Phase:**
1. CLI creates `baseline.todo.json`
2. Bob measures current state
3. Bob fills metric values
4. CLI commits to immutable `baseline.json`

**Validation Phase:**
1. CLI creates `validation.todo.json`
2. Bob measures final state (same methods!)
3. Bob fills metric values
4. CLI compares baseline → target → final
5. CLI commits to immutable `validation.json`

---

## Troubleshooting Guide

### Common Errors & Solutions

| Error | Solution |
|-------|----------|
| "baseline.json is immutable" | Use `missionforge baseline reset MF-001-A --force` |
| "Metric value missing in todo.json" | Fill all metric values before commit |
| "Path outside allowed_paths" | Only modify files matching allowed_paths |
| "Circular dependency detected" | Remove one dependency to break cycle |
| "Sub-mission validation failed" | Check validation.json for metric failures |
| "Parent validation failed" | Check aggregate metrics and forbidden_paths |

---

## Example Prompts

### Initialization
- "Initialize mission MF-001 for REST API migration"
- "Create new mission PROJ-042 for authentication refactor"

### Decomposition
- "Decompose MF-001 into sub-missions for auth, data, and UI layers"
- "Break down the migration into logical sub-missions"
- "Create sub-missions for MF-001 based on module structure"

### Baseline
- "Capture baseline for MF-001-A"
- "Measure current test coverage for auth module"
- "Commit baseline after filling metrics"

### Implementation
- "Implement MF-001-A: migrate auth module to REST"
- "Complete the authentication refactor for sub-mission A"

### Validation
- "Validate MF-001-A implementation"
- "Measure final metrics for auth module"
- "Commit validation after verifying all targets met"

### Reporting
- "Generate final report for MF-001"
- "Show me the mission completion evidence"

---

## Implementation Strategy

### Phase 1: Core Files (Priority)
1. Create `CLAUDE.md` (project root)
2. Create `skills/missionforge/SKILL.md` (installable skill)
3. Create `.bob/commands/` directory structure

### Phase 2: Command Documentation
4. Create all 8 `.bob/commands/mf-*.md` files
5. Verify CLI command references against source code

### Phase 3: Claude Code Integration
6. Create `.claude/commands/` directory
7. Copy all 8 command files from `.bob/commands/`

### Phase 4: Verification
8. Test `npx skills add` installation
9. Verify slash commands in Claude Code
10. Cross-check all CLI references
11. Test example prompts

---

## Success Criteria

✅ **Installation:** `npx skills add <owner>/Mission-Forge` works  
✅ **Universal:** Works with any AI coding agent  
✅ **Complete:** All 8 workflow steps have slash commands  
✅ **Clear:** Every command has usage examples and next steps  
✅ **Accurate:** All CLI references match implementation  
✅ **Helpful:** Metric measurement is well-documented  
✅ **Robust:** Common errors have documented solutions  

---

## File Structure After Implementation

```
Mission-Forge/
├── CLAUDE.md                          # ← NEW: Points to skill
├── skills/
│   └── missionforge/
│       └── SKILL.md                   # ← NEW: Installable skill
├── .bob/
│   └── commands/                      # ← NEW: Canonical docs (source of truth)
│       └── [8 mf-*.md files]
├── .claude/
│   └── commands/                      # ← NEW: Claude Code commands
│       └── [8 mf-*.md files]
├── .opencode/
│   └── commands/                      # ← NEW: OpenCode commands
│       └── [8 mf-*.md files]
├── .antigravity/
│   └── commands/                      # ← NEW: Antigravity commands
│       └── [8 mf-*.md files]
├── .copilot/
│   ├── commands/                      # ← NEW: GitHub Copilot commands
│   │   └── [8 mf-*.md files]
│   └── config.json                    # ← NEW: Optional config
├── .cursor/
│   ├── commands/                      # ← NEW: Cursor commands
│   │   └── [8 mf-*.md files]
│   └── config.json                    # ← NEW: Optional config
└── [existing files...]
```

---

## Design Decisions

### 1. Multi-Agent Strategy
- **`.bob/commands/`** = Canonical, agent-agnostic (single source of truth)
- **`.claude/`, `.opencode/`, `.antigravity/`, `.copilot/`, `.cursor/`** = Agent-specific copies
- **Rationale:** Universal compatibility, easy maintenance, consistent experience

### 2. skills.sh Compatibility
- Standard frontmatter format
- Location: `skills/missionforge/SKILL.md`
- Enables one-command installation

### 3. Command Naming
- Prefix: `/mf-` (short, memorable)
- Matches CLI command structure
- Easy to discover via autocomplete

### 4. Enhanced Documentation
- Metric measurement guide
- Example prompts for every command
- Troubleshooting for common errors
- Clear division of responsibility

---

## Next Steps

### For Implementation (Code Mode)
1. Create all 12 files as specified
2. Verify CLI command references
3. Test installation flow
4. Validate slash commands work

### For Testing
1. Install via `npx skills add`
2. Test each slash command
3. Verify example prompts work
4. Check troubleshooting accuracy

### For Documentation
1. Update main README with skill reference
2. Add installation instructions
3. Link to workflow diagram
4. Document metric measurement

---

## References

- **Implementation Plan:** `IMPLEMENTATION_PLAN.md`
- **Workflow Diagram:** `WORKFLOW_DIAGRAM.md`
- **Metric Guide:** `METRIC_MEASUREMENT_GUIDE.md`
- **CLI Source:** `src/missionforge/cli/`
- **README:** `README.md`
- **Decompose Docs:** `docs/DECOMPOSE_COMMAND.md`

---

## Estimated Effort

- **Planning:** ✅ Complete (this document + MULTI_AGENT_SUPPORT.md)
- **Implementation:** ~3-4 hours
  - Core files: 30 min
  - Canonical command docs: 1 hour
  - 5 agent directories: 1 hour
  - Configuration files: 30 min
  - Documentation updates: 1 hour
- **Testing:** ~1 hour (test in each agent)
- **Documentation:** ~30 min

**Total:** ~5-6 hours for complete multi-agent implementation and testing

---

**Status:** ✅ Planning Complete - Ready for Implementation

**Next Action:** Switch to Code mode to implement all 12 files

---

**Made with Bob** 🤖