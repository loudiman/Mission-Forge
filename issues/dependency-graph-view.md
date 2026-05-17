# MF-018: Dependency Graph Visualization

## Priority
**NICE TO HAVE** - Increases polish and judging impact

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- MF-014 (Board Backend) - needs plan.yaml data
- MF-015 (Board Frontend) - needs base UI structure

## Parallel Work
Can work in parallel with MF-016, MF-017, MF-019

## Objective
Render the sub-mission dependency structure in a clear visual format showing execution order and relationships.

## Tasks
- [ ] Read dependency data from plan.yaml via backend API
- [ ] Choose visualization library (reactflow, vis.js, or custom SVG)
- [ ] Create dependency graph component
- [ ] Render nodes for each sub-mission
- [ ] Render edges/arrows showing dependencies
- [ ] Highlight node states:
  - Completed (green)
  - Ready (blue)
  - Blocked (gray)
  - Failed (red)
  - In Progress (yellow)
- [ ] Add node click to open sub-mission detail
- [ ] Keep graph readable for demo mission (4-6 nodes)
- [ ] Add zoom and pan controls (optional)
- [ ] Support different layout algorithms (hierarchical, force-directed)

## Acceptance Criteria
- [ ] Graph clearly shows dependency relationships
- [ ] Node colors indicate status at a glance
- [ ] Arrows show dependency direction clearly
- [ ] Graph is readable for demo mission
- [ ] Clicking nodes opens detail panel
- [ ] Graph updates when mission state changes
- [ ] Works well in demo recording
- [ ] Handles various dependency patterns (linear, diamond, parallel)

## Example Patterns to Support
```
Linear: A → B → C → D

Diamond: 
    A
   ↙ ↘
  B   C
   ↘ ↙
    D

Parallel:
    A
   ↙ ↘
  B   C
```

## Technical Notes
- Consider reactflow for interactive graphs
- Use hierarchical layout for clear top-to-bottom flow
- Keep it simple - clarity over complexity
- Ensure graph is visible in screen recordings
- Add legend for status colors

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Frontend Developer (can work in parallel with other Phase 2 UI tasks)
