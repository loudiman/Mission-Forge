# MF-008: Baseline Capture and Commit Flow

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-002 (Schemas) - needs baseline + sub-mission schemas

NOT a hard dependency: decompose-command. Baseline operates on any `sub-mission.yaml` that conforms to the schema — for development and tests, hand-authored sub-mission YAML fixtures are sufficient. Decompose is just one producer of those files.

## Parallel Work
Runs in parallel with workspace-commands, decompose-command, plan-command, and next-command once schemas land. Only sub-mission-validation downstream of this is blocked on a real baseline.json.

## Objective
Implement baseline measurement workflow for sub-missions: capture baseline.todo.json and commit to immutable baseline.json.

## Tasks
- [ ] Implement `missionforge baseline <sub-mission-id> --capture` command
- [ ] Read sub-mission metrics from sub-mission.yaml
- [ ] Generate baseline.todo.json with:
  - metric_id
  - description
  - baseline_target
  - value (empty for Bob to fill)
- [ ] Prevent capture if baseline.json already exists (unless --force)
- [ ] Implement `missionforge baseline <sub-mission-id> --commit` command
- [ ] Validate all baseline fields are filled
- [ ] Validate field types match metric definitions
- [ ] Check values are reasonable (not obviously wrong)
- [ ] Write immutable baseline.json with timestamp
- [ ] Prevent modification after commit
- [ ] Add --reset flag to allow re-capture if needed
- [ ] Display baseline summary in terminal
- [ ] Add unit and integration tests

## Acceptance Criteria
- [ ] `--capture` generates correct baseline.todo.json structure
- [ ] baseline.todo.json is easy for Bob to fill
- [ ] Cannot capture if baseline already committed (without --force)
- [ ] `--commit` validates all fields are filled
- [ ] Type validation catches incorrect value types
- [ ] baseline.json is immutable after commit
- [ ] Timestamp is recorded in baseline.json
- [ ] Terminal output shows clear summary
- [ ] Integration tests cover capture → fill → commit flow

## Example baseline.todo.json
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "A REST endpoint exists at /api/matchmaking",
      "baseline_target": false,
      "value": null
    }
  ]
}
```

## Example baseline.json
```json
{
  "sub_mission_id": "MF-001-A",
  "timestamp": "2026-05-16T16:30:00Z",
  "status": "committed",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "A REST endpoint exists at /api/matchmaking",
      "baseline_target": false,
      "value": false
    }
  ]
}
```

## Technical Notes
- baseline.json should be immutable (add file permissions check)
- Validate metric values match expected types (bool, int, string)
- Add metadata: timestamp, status, sub_mission_id
- Clear error messages for validation failures

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (can work in parallel with MF-006/MF-007)
