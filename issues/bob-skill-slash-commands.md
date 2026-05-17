# MF-012: Bob Skill and Slash Commands

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 through MF-011 (all CLI commands must exist)

## Parallel Work
Can work independently once CLI commands are complete

## Objective
Create Bob Skill documentation and slash commands that teach Bob how to use MissionForge correctly and provide ergonomic shortcuts.

## Tasks

### Bob Skill (SKILL.md)
- [ ] Write comprehensive SKILL.md documentation
- [ ] Explain core principle: "Bob measures the code. MissionForge measures the mission."
- [ ] Document complete workflow:
  - Initialize mission
  - Validate parent mission
  - Decompose into sub-missions
  - Plan dependency graph
  - Capture baseline
  - Implement changes
  - Capture validation
  - Commit validation
  - Generate report
- [ ] Explain what Bob should do (reasoning, measurement, implementation)
- [ ] Explain what Bob should NOT do (bypass CLI, mutate state files directly)
- [ ] Include example prompts and command usage
- [ ] Add troubleshooting section
- [ ] Add best practices section

### Slash Commands
- [ ] Create `/mf-init` - Initialize new mission
- [ ] Create `/mf-mission` - Validate parent mission
- [ ] Create `/mf-decompose` - Decompose into sub-missions
- [ ] Create `/mf-plan` - Validate dependency graph
- [ ] Create `/mf-next` - Show next ready sub-mission
- [ ] Create `/mf-baseline` - Baseline capture/commit workflow
- [ ] Create `/mf-validate` - Validation capture/commit workflow
- [ ] Create `/mf-report` - Generate evidence report

Each slash command should:
- [ ] Explain what it does
- [ ] Run the relevant CLI command
- [ ] Tell Bob what to read next
- [ ] Tell Bob what file to fill or inspect
- [ ] Keep Bob aligned with workflow

## Acceptance Criteria
- [ ] SKILL.md is comprehensive and clear
- [ ] Workflow is explained step-by-step
- [ ] Bob's responsibilities are clearly defined
- [ ] CLI's responsibilities are clearly defined
- [ ] All slash commands work correctly
- [ ] Slash commands provide helpful guidance
- [ ] Bob can follow workflow without confusion
- [ ] Commands handle errors gracefully
- [ ] Documentation includes examples

## Example Slash Command Structure
```markdown
# /mf-baseline

Captures or commits baseline measurements for a sub-mission.

## Usage
/mf-baseline <sub-mission-id> [--capture|--commit]

## What it does
- `--capture`: Generates baseline.todo.json for Bob to fill
- `--commit`: Validates and commits baseline.json

## Next steps
After capture: Read the scoped code and fill baseline.todo.json
After commit: Begin implementation of the sub-mission
```

## Technical Notes
- SKILL.md should be in `.bob/skills/missionforge/`
- Slash commands should be in `.bob/commands/`
- Commands should provide context-aware help
- Include workflow diagram in SKILL.md
- Reference official CLI documentation

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Technical Writer + CLI Developer (depends on all CLI commands)
