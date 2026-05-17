# MF-016: Mission Detail Panel

## Priority
**SHOULD FINISH** - Makes project easier to demo

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- MF-014 (Board Backend) - needs API endpoints
- MF-015 (Board Frontend) - needs base UI structure

## Parallel Work
Can work in parallel with MF-017 (Report Renderer) and MF-018 (Dependency Graph)

## Objective
Create detailed view panel that opens when a mission card is clicked, showing comprehensive mission information and evidence.

## Tasks

### Parent Mission Detail
- [ ] Create detail panel component (side panel or modal)
- [ ] Display mission goal (full text)
- [ ] Display decomposition summary
- [ ] Display dependency graph (reference MF-018)
- [ ] Display sub-missions list with expand/collapse
- [ ] Display aggregate metrics table:
  - Metric name
  - Baseline value
  - Target value
  - Current/final value
  - Status indicator
- [ ] Display parent validation status
- [ ] Display parent test results
- [ ] Display git diff summary (files changed)
- [ ] Display forbidden path violations (if any)
- [ ] Add tabs or sections for organization

### Sub-Mission Detail
- [ ] Display sub-mission goal
- [ ] Display allowed paths
- [ ] Display dependencies (what it depends on, what depends on it)
- [ ] Display metrics table (baseline → target → final)
- [ ] Display git diff (files changed by this sub-mission)
- [ ] Display test results
- [ ] Display validation status with details
- [ ] Link to Bob session (if available)

### UI/UX
- [ ] Smooth open/close animations
- [ ] Responsive layout
- [ ] Clear visual hierarchy
- [ ] Status indicators (colors, icons)
- [ ] Copy buttons for IDs and commands
- [ ] Close button and keyboard shortcuts (ESC)

## Acceptance Criteria
- [ ] Panel opens smoothly when mission card is clicked
- [ ] All mission information is displayed clearly
- [ ] Metrics tables are easy to read
- [ ] Status indicators are intuitive
- [ ] Panel works for both parent and sub-missions
- [ ] Responsive design works on different screen sizes
- [ ] Navigation between parent and sub-missions is smooth
- [ ] Panel can be closed easily

## Technical Notes
- Use slide-over panel pattern (recommended) or modal
- Consider using Headless UI or Radix UI for panel component
- Syntax highlighting for code/diff display
- Use color coding for status (green=pass, red=fail, yellow=in-progress)
- Lazy load content for performance

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Frontend Developer (depends on MF-014, MF-015)
