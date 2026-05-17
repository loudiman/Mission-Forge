# MF-015: Mission Board Frontend Setup

## Priority
**SHOULD FINISH** - Makes project easier to demo

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- API contract (OpenAPI/TypeScript types) agreed with Dev C at hour 0–2
- MF-014 (Board Backend) — only required for end-to-end integration, NOT for UI development

## Parallel Work
Starts at hour 0 against a **mock API** (MSW or a static JSON server) that returns fixtures matching the agreed contract. Swap mock → real backend at hour ~14 once MF-014 is live. UI components, layouts, and state management are all built and demo-ready before integration.

Mock-API mode is a first-class requirement: ship an `npm run dev:mock` script so demos work even if backend is down.

## Objective
Create the Mission Board frontend with Next.js, displaying parent missions in Kanban-style board with sub-mission visualization.

## Tasks

### Project Setup
- [ ] Set up Next.js 14 project with App Router
- [ ] Configure Tailwind CSS
- [ ] Set up TypeScript configuration
- [ ] Create base layout and navigation
- [ ] Set up API client for backend communication
- [ ] Configure environment variables for API URL

### Parent Mission Board
- [ ] Create Kanban board layout with columns:
  - Drafted, Approved, Decomposing, In Progress, Validating, Done, Blocked
- [ ] Create parent mission card component showing:
  - Mission ID and goal summary
  - Overall progress bar
  - Test status indicator
  - Forbidden path violation count
  - Expand/collapse control
- [ ] Implement drag-and-drop (stretch goal)
- [ ] Add loading states
- [ ] Add empty states
- [ ] Add error states

### Sub-Mission Visualization
- [ ] Create sub-mission card component showing:
  - Sub-mission ID and title
  - Status indicator
  - Dependencies
  - Test status
  - Metric progress
- [ ] Render sub-missions when parent is expanded
- [ ] Group sub-missions by dependency level
- [ ] Highlight ready vs blocked sub-missions
- [ ] Show latent parallelism indicator

### State Management
- [ ] Implement polling for state updates (every 3-5 seconds)
- [ ] Preserve selected mission during refresh
- [ ] Add subtle refresh indicator
- [ ] Handle concurrent updates gracefully

## Acceptance Criteria
- [ ] Board displays all parent missions correctly
- [ ] Kanban columns show missions in correct status
- [ ] Mission cards show accurate information
- [ ] Sub-missions expand/collapse smoothly
- [ ] Dependency relationships are clear
- [ ] Polling updates board without disrupting UX
- [ ] Loading and error states are user-friendly
- [ ] Responsive design works on different screen sizes
- [ ] UI is polished and demo-ready

## Technical Notes
- Use Next.js 14 App Router for routing
- Use Tailwind CSS for styling
- Consider `@hello-pangea/dnd` for drag-and-drop (optional)
- Use SWR or React Query for data fetching and caching
- Polling interval: 3-5 seconds (configurable)
- No WebSockets needed for MVP

## Estimated Effort
**4-5 hours** (hackathon pace)

## Developer Assignment
Frontend Developer (can work in parallel with backend after API contract is defined)
