# MF-005: Decompose Command and Sub-Mission Creation

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-002 (Schemas) - needs sub-mission schema
- MF-004 (Workspace Commands) - needs parent mission to exist

## Parallel Work
Cannot start until dependencies complete, but can work independently once started

## Objective
Implement the decompose command that guides Bob through creating sub-mission files and the plan.yaml.

## Tasks
- [ ] Implement `missionforge decompose <mission-id>` command
- [ ] Display clear instructions for Bob on what to do
- [ ] Validate parent mission exists and is valid
- [ ] Create sub-missions/ directory if not exists
- [ ] Provide template/guidance for sub-mission YAML structure
- [ ] Validate each sub-mission file as it's created
- [ ] Ensure sub-mission IDs follow pattern (e.g., MF-001-A, MF-001-B)
- [ ] Validate parent reference in each sub-mission
- [ ] Check that sub-mission allowed_paths don't conflict
- [ ] Provide guidance for creating plan.yaml
- [ ] Display summary of created sub-missions
- [ ] Add integration tests

## Acceptance Criteria
- [ ] Command displays clear instructions for Bob
- [ ] Sub-mission files are validated as they're created
- [ ] Sub-mission ID format is enforced (parent-id + letter suffix)
- [ ] Parent reference is validated
- [ ] Conflicting allowed_paths are detected and warned
- [ ] Terminal output shows progress and next steps
- [ ] Bob can follow the workflow without confusion
- [ ] Integration tests cover the full decomposition flow

## Bob Workflow
1. User runs `missionforge decompose MF-001`
2. CLI displays instructions and sub-mission template
3. Bob reads codebase and creates sub-mission files
4. Bob writes plan.yaml with dependency graph
5. CLI validates structure and reports status

## Technical Notes
- Sub-mission ID pattern: `^[A-Z]{2,4}-\d{3}-[A-Z]$`
- Validate parent mission exists before allowing decomposition
- Check for overlapping allowed_paths between sub-missions
- plan.yaml should include: parent_id, sub_missions list, dependency graph, rationale
- Provide helpful error messages for common mistakes

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-001, MF-002, MF-004)
