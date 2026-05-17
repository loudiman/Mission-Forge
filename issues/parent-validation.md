# MF-010: Parent Mission Validation

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-002 (Schemas) - needs validation schema
- MF-003 (Git/Test Utilities) - needs test execution
- MF-009 (Sub-Mission Validation) - needs all sub-missions validated

## Parallel Work
Cannot start until MF-009 completes

## Objective
Implement parent-level validation that aggregates all sub-mission results and validates parent-level metrics and tests.

## Tasks
- [ ] Implement `missionforge validate <mission-id>` command (parent level)
- [ ] Verify all sub-missions have validation.json files
- [ ] Check all sub-missions have PASSED status
- [ ] Run parent-level test_command
- [ ] Capture parent test output and exit code
- [ ] Re-check git diff against parent forbidden_paths across all sub-missions
- [ ] Prompt Bob to measure parent aggregate_metrics if needed
- [ ] Compare aggregate metrics against targets
- [ ] Determine overall parent mission pass/fail status
- [ ] Write parent validation.json
- [ ] Display comprehensive validation summary
- [ ] Handle failure cases (sub-mission failed, aggregate metric failed, test failed)
- [ ] Add unit and integration tests

## Acceptance Criteria
- [ ] Command validates all sub-missions passed before proceeding
- [ ] Parent test command executes correctly
- [ ] Aggregate metrics are validated against targets
- [ ] Forbidden paths check covers all sub-mission changes
- [ ] Parent validation.json contains complete evidence
- [ ] Clear pass/fail status with detailed reasons
- [ ] Terminal output shows comprehensive summary
- [ ] Handles edge cases (no sub-missions, partial completion)
- [ ] Integration tests cover various scenarios

## Example parent validation.json
```json
{
  "mission_id": "MF-001",
  "timestamp": "2026-05-16T18:00:00Z",
  "status": "PASSED",
  "sub_missions": {
    "total": 4,
    "passed": 4,
    "failed": 0,
    "details": [
      {"id": "MF-001-A", "status": "PASSED"},
      {"id": "MF-001-B", "status": "PASSED"},
      {"id": "MF-001-C", "status": "PASSED"},
      {"id": "MF-001-D", "status": "PASSED"}
    ]
  },
  "aggregate_metrics": [
    {
      "metric_id": "corba_refs_in_matchmaking",
      "baseline_value": 7,
      "target_value": 0,
      "final_value": 0,
      "status": "PASSED"
    }
  ],
  "parent_test": {
    "command": "./gradlew integrationTest && pytest tests/integration",
    "exit_code": 0,
    "passed": true
  },
  "forbidden_paths_check": {
    "violated": false,
    "violations": []
  }
}
```

## Technical Notes
- Two-level validation: sub-missions must pass AND parent must pass
- Aggregate metrics catch integration issues individual sub-missions miss
- Parent test command is the final integration check
- Status: PASSED, FAILED, INCOMPLETE

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-009)
