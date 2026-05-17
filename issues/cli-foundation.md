# MF-001: CLI Foundation and Project Setup

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
None (can start immediately)

## Parallel Work
Can be worked on independently from all other issues

## Objective
Create the basic CLI application structure and establish the local MissionForge workspace format.

## Tasks
- [ ] Set up Python 3.11+ project structure with proper package layout
- [ ] Choose and configure CLI framework (Click or Typer)
- [ ] Implement base `missionforge` command with help text
- [ ] Add command grouping for logical organization
- [ ] Define `.missionforge/` workspace directory structure
- [ ] Implement workspace path resolution from repository root
- [ ] Add basic error handling for:
  - Missing workspace
  - Invalid paths
  - Invalid mission IDs
- [ ] Add logging configuration
- [ ] Set up project dependencies (PyYAML/ruamel.yaml, jsonschema, Jinja2)

## Acceptance Criteria
- [ ] Developer can run `missionforge --help` and see available commands
- [ ] CLI displays clear help text with command descriptions
- [ ] Workspace path resolution works from any subdirectory in repo
- [ ] Error messages are clear and actionable
- [ ] Project structure follows Python best practices

## Technical Notes
- Use Click or Typer for CLI framework
- No GitPython dependency - use subprocess calls to system git
- Keep CLI language-agnostic (never read source code)
- All file operations should be relative to repo root

## Estimated Effort
2-3 days

## Developer Assignment
Backend/CLI Developer
