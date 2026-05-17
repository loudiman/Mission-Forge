# MF-014: Mission Board Backend Setup

## Priority
**SHOULD FINISH** - Makes project easier to demo

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- schemas-validators.md (locked schemas for parent mission, sub-mission, baseline, validation, plan)
- Sample `.missionforge/` fixtures (2-3 representative missions in varied states) — Dev B produces these as a side-output of schema work around hour ~6

The full CLI does NOT need to be functional. The backend is read-only over `.missionforge/` files, so it only needs the file layout and schemas frozen. Real CLI-produced data swaps in for fixtures once available.

## Parallel Work
Starts in parallel with the rest of Phase 1 once schemas + fixtures land (~hour 6). Independent from frontend (MF-015) — both build against the same API contract.

## Objective
Create a lightweight backend that reads MissionForge state from `.missionforge/` and exposes it to the web UI via REST API.

## Tasks
- [ ] Create backend project structure (FastAPI recommended)
- [ ] Implement repository root detection
- [ ] Create endpoint: GET /api/missions (list all parent missions)
- [ ] Create endpoint: GET /api/missions/{mission_id} (parent mission detail)
- [ ] Create endpoint: GET /api/missions/{mission_id}/sub-missions (list sub-missions)
- [ ] Create endpoint: GET /api/missions/{mission_id}/sub-missions/{sub_id} (sub-mission detail)
- [ ] Create endpoint: GET /api/missions/{mission_id}/report (get report.md)
- [ ] Read mission state from `.missionforge/` directory
- [ ] Parse YAML and JSON files
- [ ] Add error handling for missing or invalid state
- [ ] Add CORS configuration for local development
- [ ] Keep backend read-only initially
- [ ] Add health check endpoint
- [ ] Add API documentation (OpenAPI/Swagger)
- [ ] Add unit tests

## Acceptance Criteria
- [ ] Backend starts successfully and serves API
- [ ] All endpoints return correct data from `.missionforge/`
- [ ] Error handling works for missing missions
- [ ] CORS allows frontend to connect
- [ ] API documentation is accessible
- [ ] Response format is consistent and well-structured
- [ ] Unit tests cover all endpoints
- [ ] Backend can run standalone for testing

## API Response Examples

### GET /api/missions
```json
{
  "missions": [
    {
      "id": "MF-001",
      "goal": "Modernize matchmaking...",
      "status": "IN_PROGRESS",
      "sub_missions_count": 4,
      "sub_missions_complete": 2
    }
  ]
}
```

### GET /api/missions/MF-001
```json
{
  "id": "MF-001",
  "goal": "...",
  "forbidden_paths": [...],
  "aggregate_metrics": [...],
  "sub_missions": [...],
  "validation": {...}
}
```

## Technical Notes
- Use FastAPI for async support and automatic OpenAPI docs
- Read files directly from `.missionforge/` (no database needed)
- Cache parsed files to avoid repeated disk reads
- Invalidate cache when files change (watch for mtime)
- Use Pydantic models for response validation
- Port: 8000 (configurable via env var)

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend Developer (can work independently from frontend initially)
