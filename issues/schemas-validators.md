# Schema Definitions and Validators

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- cli-foundation.md - needs base CLI structure

## Parallel Work
Can work in parallel with git-test-utilities.md after cli-foundation completes

## Objective
Define and implement YAML/JSON schemas for parent missions, sub-missions, baselines, and validation files with comprehensive validation logic.

## Tasks
- [ ] Define parent mission YAML schema with fields:
  - `id`, `goal`, `forbidden_paths`, `aggregate_metrics`, `test_command`, `sub_missions`
- [ ] Define sub-mission YAML schema with fields:
  - `id`, `parent`, `title`, `goal`, `depends_on`, `allowed_paths`, `metrics`, `test_command`
- [ ] Define baseline JSON schema (baseline.todo.json and baseline.json)
- [ ] Define validation JSON schema (validation.todo.json and validation.json)
- [ ] Define plan YAML schema (dependency graph, execution order)
- [ ] Implement schema validators using jsonschema library
- [ ] Add validation for:
  - YAML/JSON syntax
  - Required fields presence
  - Mission ID format and consistency
  - Path/glob pattern format
  - Metric field structure
  - Dependency reference validity
- [ ] Create clear, actionable error messages for validation failures
- [ ] Add unit tests for all validators

## Acceptance Criteria
- [ ] All schema files are well-documented with examples
- [ ] Validators catch common errors with helpful messages
- [ ] Mission ID format is enforced (e.g., MF-001, MF-001-A)
- [ ] Path globs are validated for correct syntax
- [ ] Metric definitions are validated for required fields
- [ ] Dependency references are validated against existing sub-missions
- [ ] Unit test coverage > 80% for validation logic

## Technical Notes
- Use jsonschema for JSON validation
- Use PyYAML or ruamel.yaml for YAML parsing
- Keep schemas strict but extensible for future features
- Validation should happen early (fail fast)
- Consider using Pydantic models for type safety

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (can be same as cli-foundation or different)