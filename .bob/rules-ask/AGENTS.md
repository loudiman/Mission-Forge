# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Status
This is a **planning repository** for a 24-hour hackathon project. No implementation exists yet - only detailed specifications in [`issues/`](../../issues/).

## Documentation Context (Non-Obvious)

### Issues Directory Structure
[`issues/`](../../issues/) contains GitHub issue drafts organized by phase and dependency. Each issue has:
- Priority (MUST FINISH vs SHOULD FINISH vs NICE TO HAVE)
- Dependencies (what must complete first)
- Parallel work opportunities
- Estimated effort at hackathon pace

### Baseline Flow Independence
[`baseline-flow.md`](../../issues/baseline-flow.md) does NOT depend on [`decompose-command.md`](../../issues/decompose-command.md). This is counterintuitive - baseline can work with hand-authored YAML fixtures for development/testing.

### Two-Level Validation Architecture
Sub-missions validate individually ([`sub-mission-validation.md`](../../issues/sub-mission-validation.md)), then parent validates aggregate metrics ([`parent-validation.md`](../../issues/parent-validation.md)). Parent can fail even if all sub-missions pass - this catches integration issues.

### CLI vs Bob Responsibilities
CLI handles deterministic operations (git diff, test execution, file paths). Bob handles code understanding (exploration, measurement, implementation). This separation is architectural, not just a convenience.

### Development Roadmap
[`development_roadmap.md`](../../development_roadmap.md) shows 4-developer parallel work streams with critical path of 22 hours wall-clock time. The critical path runs through Dev A and Dev B.

### Workspace Structure
`.missionforge/missions/` contains mission state. Each sub-mission has both `.yaml` definition and a directory with `baseline.json` and `validation.json` files. The `.todo.json` files are for Bob to fill.

## Key Files
- [`README.md`](../../README.md) - Core principle and architecture
- [`development_roadmap.md`](../../development_roadmap.md) - Parallel work streams
- [`issues/README.md`](../../issues/README.md) - Issue organization and dependencies