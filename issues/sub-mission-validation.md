# MF-009: Sub-Mission Validation Capture and Commit

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-002 (Schemas) - needs validation schema
- MF-003 (Git/Test Utilities) - needs git diff and test execution
- MF-008 (Baseline Flow) - needs baseline.json to compare against

## Parallel Work
Cannot start until all dependencies complete

## Objective
Implement validation workflow for sub-missions: capture deterministic evidence and Bob-filled metrics, then commit final validation results.

## Tasks
- [ ] Implement `missionforge validate <sub-mission-id> --capture` command
- [ ] Run git diff to identify changed files
- [ ] Compare changed files against sub-mission allowed_paths
- [ ] Compare changed files against parent forbidden_paths
- [ ] Run sub-mission test_command and capture output
- [ ] Record test exit code
- [ ] Generate validation.todo.json with:
  - Deterministic evidence (files changed, scope check, test results)
  - Empty metric value fields for Bob to fill
- [ ] Implement `missionforge validate <sub-mission-id> --commit` command
- [ ] Validate Bob-filled metric values are complete
- [ ] Compare final values against baseline values
- [ ] Compare final values against target values
- [ ] Determine pass/fail status for each metric
- [ ] Determine overall sub-mission pass/fail status
- [ ] Write validation.json with complete results
- [ ] Display clear validation summary
- [ ] Block dependent sub-missions if validation fails
- [ ] Add unit and integration tests

## Acceptance Criteria
- [ ] `--capture` correctly identifies changed files via git diff
- [ ] Scope validation works (allowed paths, forbidden paths)
- [ ] Test command executes and output is captured
- [ ] validation.todo.json contains all deterministic evidence
- [ ] `--commit` validates all metric fields are filled
- [ ] Baseline vs final comparison is accurate
- [ ] Target vs final comparison is accurate
- [ ] Pass/fail logic is correct
- [ ] validation.json contains complete evidence
- [ ] Terminal output clearly shows pass/fail status
- [ ] Integration tests cover various scenarios (pass, fail, scope violation)

## Example validation.todo.json
```json
{
  "sub_mission_id": "MF-001-A",
  "deterministic_evidence": {
    "files_changed": ["server/src/rest/MatchmakingEndpoint.java"],
    "scope_check": {
      "allowed_paths_satisfied": true,
      "forbidden_paths_violated": false,
      "violations": []
    },
    "test_results": {
      "command": "./gradlew test --tests '*MatchmakingEndpointTest*'",
      "exit_code": 0,
      "output": "...",
      "passed": true
    }
  },
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "baseline_value": false,
      "target_value": true,
      "final_value": null
    }
  ]
}
```

## Example validation.json
```json
{
  "sub_mission_id": "MF-001-A",
  "timestamp": "2026-05-16T17:00:00Z",
  "status": "PASSED",
  "deterministic_evidence": { ... },
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "baseline_value": false,
      "target_value": true,
      "final_value": true,
      "status": "PASSED"
    }
  ]
}
```

## Technical Notes
- Use git diff utilities from MF-003
- Scope check must validate against both allowed and forbidden paths
- Test execution should have timeout
- validation.json status: PASSED, FAILED, BLOCKED
- Clear distinction between deterministic evidence (CLI) and semantic metrics (Bob)

## Estimated Effort
**4-5 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-001, MF-002, MF-003, MF-008)
