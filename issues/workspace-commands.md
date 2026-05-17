# MF-004: Workspace Initialization Commands

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation) - needs base CLI structure
- MF-002 (Schemas) - needs schema definitions for templates

## Parallel Work
Can work in parallel with MF-003 (Git/Test Utilities)

## Objective
Implement mission workspace initialization and parent mission validation commands.

## Tasks
- [ ] Implement `missionforge init <mission-id>` command
- [ ] Generate parent mission directory structure
- [ ] Create initial mission.yaml template with helpful comments
- [ ] Create empty plan.yaml placeholder
- [ ] Create sub-missions/ directory
- [ ] Create empty report.md placeholder
- [ ] Prevent accidental overwrite of existing missions
- [ ] Validate mission ID format before creation
- [ ] Implement `missionforge mission <mission-id> --validate` command
- [ ] Validate parent mission YAML against schema
- [ ] Check forbidden_paths glob patterns are valid
- [ ] Check aggregate_metrics structure
- [ ] Check test_command is present
- [ ] Add helpful terminal output with next steps
- [ ] Add unit and integration tests

## Acceptance Criteria
- [ ] `missionforge init MF-001` creates proper directory structure
- [ ] Generated mission.yaml has clear template with examples
- [ ] Cannot overwrite existing mission without --force flag
- [ ] Mission ID format is validated (e.g., MF-001, FG-042)
- [ ] `missionforge mission MF-001 --validate` reports clear errors
- [ ] Validation catches missing required fields
- [ ] Validation catches invalid glob patterns
- [ ] Terminal output guides user on next steps
- [ ] Integration tests cover happy path and error cases

## Expected Directory Structure
```
.missionforge/
└── missions/
    └── MF-001/
        ├── mission.yaml
        ├── plan.yaml
        ├── sub-missions/
        └── report.md
```

## Technical Notes
- Use templates for mission.yaml with helpful comments
- Mission ID regex: `^[A-Z]{2,4}-\d{3}[A-Z]?$`
- Validate paths exist before creating workspace
- Use atomic operations where possible
- Clear error messages for common mistakes

## Estimated Effort
**2-3 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-001 and MF-002)
