# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Status
This is a **planning repository** for a 24-hour hackathon project. No implementation exists yet - only detailed specifications in [`issues/`](issues/).

## Non-Obvious Architecture Decisions

### Baseline Flow Independence
[`baseline-flow.md`](issues/baseline-flow.md) does NOT depend on [`decompose-command.md`](issues/decompose-command.md). Baseline operates on any conforming `sub-mission.yaml` - hand-authored fixtures work for development/testing.

### Two-Level Validation
Sub-missions validate individually ([`sub-mission-validation.md`](issues/sub-mission-validation.md)), then parent validates aggregate metrics ([`parent-validation.md`](issues/parent-validation.md)). Parent can fail even if all sub-missions pass.

### CLI Never Reads Source Code
Language-agnostic by design. CLI handles deterministic operations (git diff, test execution, file paths). Bob handles code understanding (exploration, measurement, implementation).

### Immutable baseline.json
Once committed via `missionforge baseline <id> --commit`, [`baseline.json`](issues/baseline-flow.md) cannot be modified without `--reset` flag. This is intentional for audit trail.

## Mission ID Format
- Parent: `^[A-Z]{2,4}-\d{3}[A-Z]?$` (e.g., `MF-001`, `FG-042A`)
- Sub-mission: `^[A-Z]{2,4}-\d{3}-[A-Z]$` (e.g., `MF-001-A`, `MF-001-B`)

## Technical Constraints

### No GitPython Dependency
Use subprocess calls to system git, not GitPython library. See [`git-test-utilities.md`](issues/git-test-utilities.md).

### Subprocess Security
NEVER use `shell=True` or `os.system()`. Use subprocess module with list arguments to prevent shell injection.

### Bob Integration
- Slash commands: `.bob/commands/`
- Skills: `.bob/skills/missionforge/`
- See [`bob-skill-slash-commands.md`](issues/bob-skill-slash-commands.md)

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
```

## Development Workflow
See [`development_roadmap.md`](development_roadmap.md) for 4-developer parallel work streams and critical path (22 hours wall-clock with proper coordination).