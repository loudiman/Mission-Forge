# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Status
This is a **planning repository** for a 24-hour hackathon project. No implementation exists yet - only detailed specifications in [`issues/`](../../issues/).

## Planning Mode Context (Non-Obvious)

### Baseline Flow Independence
[`baseline-flow.md`](../../issues/baseline-flow.md) does NOT depend on [`decompose-command.md`](../../issues/decompose-command.md). Baseline operates on any conforming `sub-mission.yaml` - hand-authored fixtures work for development/testing. This is intentional for parallel development.

### Two-Level Validation Architecture
Sub-missions validate individually, then parent validates aggregate metrics. Parent can fail even if all sub-missions pass. This catches integration issues that individual sub-missions miss.

### CLI Never Reads Source Code
Language-agnostic by design. CLI handles deterministic operations (git diff, test execution, file paths). Bob handles code understanding (exploration, measurement, implementation). This separation is architectural.

### Immutable baseline.json
Once committed via `missionforge baseline <id> --commit`, baseline.json cannot be modified without `--reset` flag. This is intentional for audit trail and prevents baseline drift.

### Critical Path Dependencies
See [`development_roadmap.md`](../../development_roadmap.md):
- Critical path runs through Dev A and Dev B (CLI core and validation)
- Dev C and Dev D (Board backend/frontend) have slack time
- Hour 0-2: API contract sync (blocks everyone)
- Hour ~6: Fixtures published (unblocks Board development)
- Hour ~14: Backend live (enables real API integration)
- Hour ~22: Feature freeze (full team on demo prep)

### Parallel Work Opportunities
- Schemas + Git utilities can work in parallel after CLI foundation
- Baseline flow + Plan/Next commands can work in parallel
- Board backend/frontend can work against fixtures before CLI completes

### Mission ID Format Constraints
- Parent: `^[A-Z]{2,4}-\d{3}[A-Z]?$` (e.g., `MF-001`, `FG-042A`)
- Sub-mission: `^[A-Z]{2,4}-\d{3}-[A-Z]$` (e.g., `MF-001-A`, `MF-001-B`)

These patterns are enforced at validation time, not just convention.

## Workspace Structure
```
.missionforge/
└── missions/
    └── MF-001/
        ├── mission.yaml          # Parent mission definition
        ├── plan.yaml             # Dependency graph + execution order
        ├── sub-missions/
        │   ├── MF-001-A.yaml
        │   ├── MF-001-A/
        │   │   ├── baseline.todo.json  # Bob fills this
        │   │   ├── baseline.json       # Immutable after commit
        │   │   ├── validation.todo.json
        │   │   └── validation.json
        │   └── ...
        └── report.md             # Generated evidence report