# MissionForge Workflow Diagram

## Complete Mission Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MISSIONFORGE WORKFLOW                                │
│                  "Bob measures the code. MissionForge measures the mission." │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│  1. INIT     │  /mf-init MF-001
│              │  → Creates mission workspace
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  2. MISSION  │  /mf-mission MF-001 --validate
│   VALIDATE   │  → Bob edits mission.yaml
│              │  → Validates structure
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 3. DECOMPOSE │  /mf-decompose MF-001
│              │  → Bob analyzes codebase
│              │  → Creates sub-mission YAMLs (MF-001-A, MF-001-B, etc.)
│              │  → Validates each with validate-submission
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  4. PLAN     │  /mf-plan MF-001
│              │  → Resolves dependencies
│              │  → Generates execution order
│              │  → Creates plan.yaml
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  5. NEXT     │  /mf-next MF-001
│              │  → Shows next ready sub-mission
│              │  → Displays parallelism levels
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOR EACH SUB-MISSION (e.g., MF-001-A)                    │
└─────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│ 6. BASELINE  │  /mf-baseline MF-001-A --capture
│   CAPTURE    │  → CLI runs git diff, scope check
│              │  → Creates baseline.todo.json
│              │  → Bob measures metrics (test coverage, line counts, etc.)
│              │  → Bob fills metric values
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 7. BASELINE  │  /mf-baseline MF-001-A --commit
│   COMMIT     │  → Validates all metrics filled
│              │  → Creates immutable baseline.json
│              │  → ⚠️  baseline.json is now locked
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 8. IMPLEMENT │  Bob implements changes
│              │  → Works within allowed_paths
│              │  → Makes code changes
│              │  → Runs tests locally
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ 9. VALIDATE  │  /mf-validate MF-001-A --capture
│   CAPTURE    │  → CLI runs git diff, scope check, tests
│              │  → Creates validation.todo.json
│              │  → Bob measures final metrics
│              │  → Bob fills metric values
└──────┬───────┘
       │
       ▼
┌──────────────┐
│10. VALIDATE  │  /mf-validate MF-001-A --commit
│   COMMIT     │  → Compares final vs baseline vs target
│              │  → Determines PASSED/FAILED/BLOCKED
│              │  → Creates immutable validation.json
│              │  → ⚠️  validation.json is now locked
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   REPEAT     │  Return to step 5 (/mf-next) for next sub-mission
│              │  Until all sub-missions complete
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PARENT VALIDATION                                    │
└─────────────────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│11. VALIDATE  │  missionforge validate parent MF-001
│    PARENT    │  → Verifies all sub-missions PASSED
│              │  → Runs parent test_command
│              │  → Validates aggregate metrics
│              │  → Checks forbidden_paths across all changes
│              │  → Creates parent validation.json
└──────┬───────┘
       │
       ▼
┌──────────────┐
│12. REPORT    │  /mf-report MF-001
│              │  → Generates report.md
│              │  → Shows evidence summary
│              │  → Mission complete! 🎉
└──────────────┘
```

## Division of Responsibility

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BOB (AI Agent)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Analyzes codebase structure                                               │
│ • Creates sub-mission decomposition                                         │
│ • Measures metrics (test coverage, line counts, complexity)                 │
│ • Fills .todo.json files with measured values                               │
│ • Implements code changes within allowed_paths                              │
│ • Reads and understands code                                                │
│ • Makes architectural decisions                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         MISSIONFORGE CLI                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Runs git diff (deterministic file changes)                                │
│ • Executes test commands                                                    │
│ • Validates file paths against patterns                                     │
│ • Checks scope (allowed_paths, forbidden_paths)                             │
│ • Resolves dependency graphs                                                │
│ • Validates YAML schemas                                                    │
│ • Creates immutable audit files (.json)                                     │
│ • Generates reports                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## File State Transitions

```
Sub-Mission MF-001-A Lifecycle:

1. MF-001-A.yaml (created by Bob)
   ↓
2. baseline.todo.json (created by CLI, filled by Bob)
   ↓
3. baseline.json (committed by CLI, immutable ⚠️)
   ↓
4. [Bob implements changes]
   ↓
5. validation.todo.json (created by CLI, filled by Bob)
   ↓
6. validation.json (committed by CLI, immutable ⚠️)
```

## Metric Measurement Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BASELINE CAPTURE                                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  CLI creates baseline.todo.json │
                    │  with empty metric values      │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Bob analyzes code           │
                    │  • Runs coverage tools       │
                    │  • Counts lines              │
                    │  • Checks boolean conditions │
                    │  • Measures complexity       │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Bob fills metric values     │
                    │  in baseline.todo.json       │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  CLI commits to baseline.json │
                    │  (now immutable)             │
                    └──────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      VALIDATION CAPTURE                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  CLI creates validation.todo.json │
                    │  with empty metric values      │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Bob measures final state    │
                    │  (same process as baseline)  │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Bob fills metric values     │
                    │  in validation.todo.json     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  CLI compares:               │
                    │  baseline → target → final   │
                    │  Determines PASS/FAIL        │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  CLI commits to validation.json │
                    │  (now immutable)             │
                    └──────────────────────────────┘
```

## Parallelism Levels (Future Phase 3)

```
Level 0 (Ready):     MF-001-A, MF-001-B
                     ↓         ↓
Level 1 (Blocked):   MF-001-C (depends on A)
                     ↓
Level 2 (Blocked):   MF-001-D (depends on C)

Note: Phase 1 executes sequentially.
Parallel execution coming in Phase 3.
```

---

**Made with Bob** 🤖