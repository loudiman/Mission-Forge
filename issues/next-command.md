# MF-007: Next Command for Sub-Mission Selection

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-006 (Plan Command) - needs dependency graph and execution order

## Parallel Work
Cannot start until MF-006 completes

## Objective
Implement command to identify which sub-mission(s) are ready to execute next based on dependency graph and validation status.

## Tasks
- [ ] Implement `missionforge next <mission-id>` command
- [ ] Read plan.yaml for dependency graph
- [ ] Read validation status of all sub-missions
- [ ] Determine which sub-missions have all dependencies satisfied
- [ ] For Phase 1, return one recommended next sub-mission
- [ ] Display all currently ready sub-missions (show latent parallelism)
- [ ] Mark blocked sub-missions with clear explanations
- [ ] Show why each blocked sub-mission is blocked
- [ ] Display progress summary (X of Y sub-missions complete)
- [ ] Handle edge cases (all complete, none ready, first sub-mission)
- [ ] Add unit and integration tests

## Acceptance Criteria
- [ ] Command correctly identifies ready sub-missions
- [ ] Returns one recommended sub-mission for Phase 1 execution
- [ ] Shows all ready sub-missions to demonstrate parallelism potential
- [ ] Clearly explains why blocked sub-missions are blocked
- [ ] Shows overall mission progress
- [ ] Handles case when all sub-missions are complete
- [ ] Handles case when no sub-missions are ready (dependency failure)
- [ ] Terminal output is clear and actionable
- [ ] Integration tests cover various dependency scenarios

## Example Output
```
Mission MF-001 Progress: 2/4 sub-missions complete

READY TO EXECUTE:
  → MF-001-C (recommended next)
    Dependencies satisfied: MF-001-A (PASSED)
  
  → MF-001-B
    Dependencies satisfied: MF-001-A (PASSED)
    
Note: MF-001-B and MF-001-C can run in parallel (Phase 3 feature)

BLOCKED:
  ⊗ MF-001-D
    Waiting for: MF-001-B, MF-001-C

COMPLETE:
  ✓ MF-001-A
```

## Technical Notes
- Read validation.json from each sub-mission to check status
- Use dependency graph from plan.yaml
- For Phase 1, recommend the first ready sub-mission in topological order
- Show all ready sub-missions to demonstrate future parallelism
- Clear status indicators (→ ready, ⊗ blocked, ✓ complete)

## Estimated Effort
**2-3 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-006)
