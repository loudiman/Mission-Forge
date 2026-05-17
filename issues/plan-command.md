# MF-006: Plan Command and Dependency Graph Resolution

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-002 (Schemas) - needs plan schema
- MF-005 (Decompose Command) - needs sub-missions to exist

## Parallel Work
Cannot start until MF-005 completes

## Objective
Implement dependency graph validation and topological sort to determine execution order of sub-missions.

## Tasks
- [ ] Implement `missionforge plan <mission-id>` command
- [ ] Read all sub-mission YAML files from sub-missions/ directory
- [ ] Parse depends_on fields from each sub-mission
- [ ] Validate all dependency references exist
- [ ] Detect dependency cycles using graph algorithms
- [ ] Detect invalid parent references
- [ ] Check for overlapping allowed_paths between sub-missions
- [ ] Compute topological execution order
- [ ] Write resolved plan to plan.yaml with:
  - Parent mission ID
  - Sub-mission list
  - Dependency graph structure
  - Topological execution order
  - Decomposition rationale (if provided)
- [ ] Display ready and blocked sub-missions
- [ ] Show latent parallelism (sub-missions at same dependency level)
- [ ] Add unit tests for graph algorithms
- [ ] Add integration tests

## Acceptance Criteria
- [ ] Command validates all dependencies exist
- [ ] Detects and reports dependency cycles clearly
- [ ] Computes correct topological order
- [ ] plan.yaml contains complete dependency information
- [ ] Terminal output shows execution order clearly
- [ ] Shows which sub-missions could run in parallel (future Phase 3)
- [ ] Handles edge cases (no dependencies, linear chain, diamond pattern)
- [ ] Unit tests cover cycle detection and topological sort
- [ ] Integration tests cover various dependency patterns

## Technical Notes
- Use standard graph algorithms (DFS for cycle detection, Kahn's algorithm for topological sort)
- Dependency graph should be represented as adjacency list
- Consider using networkx library for graph operations (optional)
- plan.yaml format should be human-readable
- Show "latent parallelism" even though Phase 1 executes sequentially

## Example Dependency Patterns
```
Linear: A → B → C → D
Diamond: A → B → D
              ↘ C ↗
Parallel: A → B
          A → C
```

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-005)
