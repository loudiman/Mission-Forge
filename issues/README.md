# MissionForge Development Issues

## Overview
This directory contains GitHub issue drafts for the MissionForge hackathon project. Issues are organized into two phases with realistic time estimates for a 24-hour hackathon.

## Issue Organization

### Phase 1: Core CLI Harness (Must Finish)
**Critical Path - 16-20 hours total**

1. **cli-foundation.md** (4-6h) - No dependencies, start immediately
2. **schemas-validators.md** (3-4h) - Depends on cli-foundation
3. **git-test-utilities.md** (2-3h) - Depends on cli-foundation, parallel with schemas
4. **workspace-commands.md** (2-3h) - Depends on cli-foundation + schemas
5. **decompose-command.md** (3-4h) - Depends on workspace-commands
6. **plan-command.md** (3-4h) - Depends on decompose-command
7. **next-command.md** (2h) - Depends on plan-command
8. **baseline-flow.md** (3-4h) - Depends on schemas, parallel with plan/next
9. **sub-mission-validation.md** (4-5h) - Depends on baseline + git-test-utilities
10. **parent-validation.md** (3h) - Depends on sub-mission-validation
11. **report-generation.md** (3h) - Depends on parent-validation
12. **bob-skill-slash-commands.md** (2-3h) - Depends on all CLI commands
13. **demo-mission-prep.md** (4-5h) - Depends on all CLI, can overlap with Phase 2

### Phase 2: Mission Board (Should Finish)
**Enhancement Path - 12-16 hours total**

14. **board-backend.md** (3-4h) - Depends on Phase 1 CLI
15. **board-frontend.md** (4-5h) - Depends on board-backend
16. **mission-detail-panel.md** (3h) - Depends on board-frontend
17. **report-renderer.md** (2h) - Depends on board-frontend, parallel with detail-panel
18. **dependency-graph-view.md** (3-4h) - Nice to have, parallel with other UI
19. **cli-wrapper-endpoints.md** (2h) - Nice to have, depends on board-backend
20. **watsonx-mission-chat.md** (3-4h) - Nice to have, depends on board-backend + detail-panel
21. **stakeholder-translation.md** (3h) - Nice to have, parallel with mission-chat
22. **demo-polish-submission.md** (5-7h) - Final integration, depends on completed features

## Parallel Work Streams (4 Developers)

| Window | Dev A — CLI Core | Dev B — CLI Validation | Dev C — Board Backend | Dev D — Board Frontend |
|---|---|---|---|---|
| **0–6h** | cli-foundation | schemas-validators (in parallel; finalize after A's foundation lands) + git-test-utilities + author 2-3 `.missionforge/` sample fixtures | Co-design API contract with Dev D; scaffold FastAPI project | Co-design API contract; Next.js scaffold + mock API server (MSW) + wireframes |
| **6–14h** | workspace-commands → decompose-command | baseline-flow (no longer waits for decompose) → start sub-mission-validation | board-backend against fixtures | board-frontend against mock API |
| **14–22h** | plan-command → next-command | sub-mission-validation → parent-validation → report-generation | cli-wrapper-endpoints, watsonx-mission-chat (if time) | mission-detail-panel + report-renderer; swap mock → real API |
| **22–24h** | demo-mission-prep | bob-skill-slash-commands | integration + endpoint hardening | demo-polish-submission |

**Dropped from critical plan (nice-to-haves, do only if ahead of schedule):**
- dependency-graph-view (use ASCII fallback)
- stakeholder-translation

### Cross-stream sync points
1. **Hour 0–2**: All 4 devs agree on API contract + schemas (blocking everyone).
2. **Hour ~6**: Dev B publishes `.missionforge/` sample fixtures → unblocks Dev C and Dev D's mock swap.
3. **Hour ~14**: Dev C's backend goes live → Dev D swaps mock → real.
4. **Hour ~22**: Feature freeze; full team on demo-prep + polish.

## Time Budget (24 hours)

### Must Complete (16-20 hours)
- Phase 1 CLI: All 13 issues
- Minimum viable product for terminal-only demo

### Should Complete (8-12 hours)
- Phase 2 Board: Issues 14-17 (backend + basic frontend)
- Visual demo enhancement

### Nice to Have (4-8 hours)
- Issues 18-21 (advanced UI + watsonx)
- Polish and wow factors

### Cut if Needed
1. dependency-graph-view (use ASCII diagram instead)
2. stakeholder-translation (focus on mission-chat only)
3. cli-wrapper-endpoints (Board read-only is fine)
4. watsonx-mission-chat (terminal-only demo still works)

## Critical Path
```
cli-foundation (4-6h)
  ↓
schemas-validators (3-4h) + git-test-utilities (2-3h)
  ↓
workspace-commands (2-3h)
  ↓
decompose-command (3-4h)
  ↓
plan-command (3-4h) + baseline-flow (3-4h)
  ↓
next-command (2h) + sub-mission-validation (4-5h)
  ↓
parent-validation (3h)
  ↓
report-generation (3h)
  ↓
bob-skill-slash-commands (2-3h)
  ↓
demo-mission-prep (4-5h)
```

**Total Critical Path: ~40 hours of sequential work**
**With 2 parallel developers: ~20-24 hours**
**With 4 parallel developers (this plan): ~22 hours wall-clock**, assuming the hour-0 API-contract sync and hour-6 fixture handoff happen on time. Slack in Dev C/D streams absorbs CLI critical-path slippage.

## Success Criteria

### Minimum Viable (Must Have)
- ✅ CLI can initialize missions
- ✅ CLI can validate parent missions
- ✅ CLI can decompose into sub-missions
- ✅ CLI can plan dependency graph
- ✅ CLI can track baseline and validation
- ✅ CLI can generate evidence reports
- ✅ Bob Skill and slash commands work
- ✅ Terminal-only demo is recordable

### Enhanced (Should Have)
- ✅ Mission Board displays mission state
- ✅ Board shows Kanban-style progress
- ✅ Board renders evidence reports
- ✅ Visual demo is compelling

### Polish (Nice to Have)
- ✅ Dependency graph visualization
- ✅ Watsonx.ai integration
- ✅ Stakeholder translation
- ✅ Board can trigger CLI commands

## Notes
- All time estimates assume experienced developers working at hackathon pace
- Estimates include implementation, testing, and basic documentation
- Does not include breaks, meals, or context switching overhead
- Parallel work requires clear API contracts and minimal conflicts
