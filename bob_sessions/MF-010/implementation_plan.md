# MF-010: Parent Mission Validation - Implementation Plan

## Overview
Implement parent-level validation that aggregates all sub-mission results and validates parent-level metrics and tests. This is a **MUST FINISH** feature required for project viability.

## Dependencies
- ✅ MF-001 (CLI Foundation) - Complete
- ✅ MF-002 (Schemas) - Complete  
- ✅ MF-003 (Git/Test Utilities) - Complete
- ⚠️ MF-009 (Sub-Mission Validation) - **Required** (currently implemented)

## Architecture Overview

### Two-Level Validation System
```
Parent Mission Validation
├── Sub-Mission Aggregation (all must PASS)
├── Parent Test Execution (must pass)
├── Aggregate Metrics Validation (must meet targets)
└── Cross-Sub-Mission Forbidden Paths Check
```

### Key Architectural Principles
1. **Two-level validation**: Sub-missions must pass AND parent must pass
2. **Aggregate metrics catch integration issues** that individual sub-missions miss
3. **Parent test command** is the final integration check
4. **Immutable validation.json** for audit trail

## Data Models

### ParentMissionValidation Schema
```python
class SubMissionSummary(BaseModel):
    """Summary of a single sub-mission's validation status."""
    id: str
    status: str  # PASSED, FAILED, BLOCKED
    timestamp: str | None

class SubMissionsAggregate(BaseModel):
    """Aggregate summary of all sub-missions."""
    total: int
    passed: int
    failed: int
    blocked: int
    details: list[SubMissionSummary]

class AggregateMetricResult(BaseModel):
    """Result of an aggregate metric validation."""
    metric_id: str
    baseline_value: bool | int | float | str | None
    target_value: bool | int | float | str
    final_value: bool | int | float | str | None
    status: str  # PASSED, FAILED

class ParentTestResult(BaseModel):
    """Parent-level test execution result."""
    command: str
    exit_code: int
    output: str
    passed: bool
    duration: float

class ForbiddenPathsCheck(BaseModel):
    """Cross-sub-mission forbidden paths validation."""
    violated: bool
    violations: list[str]  # List of violating file paths

class ParentMissionValidation(BaseModel):
    """Complete parent mission validation state."""
    mission_id: str
    timestamp: str
    status: str  # PASSED, FAILED, INCOMPLETE
    sub_missions: SubMissionsAggregate
    aggregate_metrics: list[AggregateMetricResult]
    parent_test: ParentTestResult | None
    forbidden_paths_check: ForbiddenPathsCheck
```

## Implementation Flow

### Phase 1: Schema & Models (1 hour)
1. Add parent validation models to [`schemas.py`](../../src/missionforge/models/schemas.py)
2. Add validation for parent mission ID format
3. Add parent validation exceptions to [`exceptions.py`](../../src/missionforge/core/exceptions.py)

### Phase 2: Workspace & Service (1.5 hours)
1. Add parent validation path methods to [`Workspace`](../../src/missionforge/core/workspace.py):
   - `parent_validation_path(mission_id: str) -> Path`
   - Returns: `.missionforge/missions/{mission_id}/validation.json`

2. Create `ParentValidationService` class:
   ```python
   class ParentValidationService:
       def validate_parent_mission(self, mission_id: str) -> Path:
           """Execute parent validation and write validation.json."""
           # 1. Load parent mission definition
           # 2. Verify all sub-missions have validation.json
           # 3. Check all sub-missions PASSED
           # 4. Execute parent test command
           # 5. Prompt Bob for aggregate metrics
           # 6. Validate aggregate metrics
           # 7. Check forbidden paths across all sub-missions
           # 8. Determine overall status
           # 9. Write immutable validation.json
   ```

### Phase 3: CLI Command (0.5 hours)
Add parent validation command to [`validate.py`](../../src/missionforge/cli/commands/validate.py):
```python
@app.command("parent")
def validate_parent(
    mission_id: str = typer.Argument(..., help="Parent mission ID (e.g., MF-001)"),
) -> None:
    """Validate parent mission after all sub-missions complete."""
```

### Phase 4: Testing (1 hour)
1. Unit tests for `ParentValidationService`
2. Integration tests for parent validation flow
3. CLI command tests

## Validation Logic Details

### 1. Sub-Mission Aggregation
```python
def _aggregate_sub_missions(self, mission_id: str) -> SubMissionsAggregate:
    """Load and aggregate all sub-mission validation results."""
    # Load parent mission to get sub_missions list
    # For each sub-mission:
    #   - Check validation.json exists
    #   - Load status
    #   - Count PASSED/FAILED/BLOCKED
    # Return aggregate summary
```

**Failure Conditions:**
- Any sub-mission missing `validation.json` → INCOMPLETE
- Any sub-mission status is FAILED → Parent FAILED
- Any sub-mission status is BLOCKED → Parent FAILED

### 2. Parent Test Execution
```python
def _execute_parent_test(self, test_command: str) -> ParentTestResult:
    """Execute parent-level test command."""
    # Use existing execute_test_command from testing.executor
    # Capture exit code, output, duration
    # Return structured result
```

**Failure Conditions:**
- Test command exit code != 0 → Parent FAILED

### 3. Aggregate Metrics Validation
```python
def _validate_aggregate_metrics(
    self, 
    metrics_def: dict[str, MetricDefinition],
    mission_id: str
) -> list[AggregateMetricResult]:
    """Prompt Bob to measure and validate aggregate metrics."""
    # For each aggregate metric:
    #   - Create todo structure with metric_id, description, target
    #   - Prompt Bob to fill final_value
    #   - Compare against target using same logic as sub-mission
    #   - Determine PASSED/FAILED status
```

**Failure Conditions:**
- Any aggregate metric FAILED → Parent FAILED

### 4. Forbidden Paths Check
```python
def _check_forbidden_paths_across_subs(
    self,
    mission_id: str,
    forbidden_paths: list[str]
) -> ForbiddenPathsCheck:
    """Check forbidden paths across all sub-mission changes."""
    # Collect all files_changed from all sub-mission validation.json
    # Run path matching against parent forbidden_paths
    # Return violations if any
```

**Failure Conditions:**
- Any file violates forbidden paths → Parent FAILED

### 5. Overall Status Determination
```python
def _determine_parent_status(
    self,
    sub_missions: SubMissionsAggregate,
    parent_test: ParentTestResult | None,
    aggregate_metrics: list[AggregateMetricResult],
    forbidden_check: ForbiddenPathsCheck
) -> str:
    """Determine overall parent mission status."""
    # INCOMPLETE: Not all sub-missions have validation.json
    # FAILED: Any of the following:
    #   - Any sub-mission FAILED or BLOCKED
    #   - Parent test failed
    #   - Any aggregate metric FAILED
    #   - Forbidden paths violated
    # PASSED: All checks passed
```

## File Structure

```
.missionforge/
└── missions/
    └── MF-001/
        ├── mission.yaml              # Parent mission definition
        ├── plan.yaml                 # Execution plan
        ├── validation.json           # NEW: Parent validation result
        └── sub-missions/
            ├── MF-001-A/
            │   └── validation.json   # Sub-mission validation
            ├── MF-001-B/
            │   └── validation.json
            └── ...
```

## Example Parent validation.json

```json
{
  "mission_id": "MF-001",
  "timestamp": "2026-05-16T18:00:00Z",
  "status": "PASSED",
  "sub_missions": {
    "total": 4,
    "passed": 4,
    "failed": 0,
    "blocked": 0,
    "details": [
      {"id": "MF-001-A", "status": "PASSED", "timestamp": "2026-05-16T17:00:00Z"},
      {"id": "MF-001-B", "status": "PASSED", "timestamp": "2026-05-16T17:15:00Z"},
      {"id": "MF-001-C", "status": "PASSED", "timestamp": "2026-05-16T17:30:00Z"},
      {"id": "MF-001-D", "status": "PASSED", "timestamp": "2026-05-16T17:45:00Z"}
    ]
  },
  "aggregate_metrics": [
    {
      "metric_id": "total_corba_references",
      "baseline_value": 7,
      "target_value": 0,
      "final_value": 0,
      "status": "PASSED"
    },
    {
      "metric_id": "integration_test_coverage",
      "baseline_value": 45.0,
      "target_value": 80.0,
      "final_value": 85.0,
      "status": "PASSED"
    }
  ],
  "parent_test": {
    "command": "./gradlew integrationTest && pytest tests/integration",
    "exit_code": 0,
    "output": "All tests passed...",
    "passed": true,
    "duration": 45.2
  },
  "forbidden_paths_check": {
    "violated": false,
    "violations": []
  }
}
```

## CLI Usage

```bash
# After all sub-missions validated
missionforge validate parent MF-001

# Output:
# ✓ Checking sub-missions...
#   - MF-001-A: PASSED
#   - MF-001-B: PASSED
#   - MF-001-C: PASSED
#   - MF-001-D: PASSED
# 
# ✓ Running parent tests...
#   Command: ./gradlew integrationTest
#   Duration: 45.2s
#   Status: PASSED
#
# ⚠ Measuring aggregate metrics...
#   Please fill final_value in validation.todo.json
#
# [After Bob fills metrics]
#
# ✓ Validating aggregate metrics...
#   - total_corba_references: 0 (target: 0) ✓
#   - integration_test_coverage: 85.0 (target: 80.0) ✓
#
# ✓ Checking forbidden paths...
#   No violations detected
#
# ✓ Parent Mission Validation: PASSED
#   Committed: .missionforge/missions/MF-001/validation.json
```

## Error Handling

### Missing Sub-Mission Validation
```
Error: Sub-mission MF-001-B has no validation.json
Suggestion: Run 'missionforge validate capture MF-001-B' and commit
```

### Sub-Mission Failed
```
Error: Cannot validate parent - sub-mission MF-001-C status is FAILED
Suggestion: Fix issues in MF-001-C and re-validate before parent validation
```

### Parent Test Failed
```
Error: Parent test command failed (exit code: 1)
Output: [test output]
Suggestion: Fix integration test failures before proceeding
```

### Aggregate Metric Failed
```
Error: Aggregate metric 'total_corba_references' failed
  Expected: 0, Got: 3
Suggestion: Review sub-mission implementations to meet aggregate target
```

## Testing Strategy

### Unit Tests
- `test_parent_validation_service.py`
  - Test sub-mission aggregation logic
  - Test status determination logic
  - Test metric validation logic
  - Test forbidden paths checking

### Integration Tests
- `test_parent_validation_flow.py`
  - Test complete parent validation flow
  - Test with all sub-missions PASSED
  - Test with one sub-mission FAILED
  - Test with missing sub-mission validation
  - Test parent test execution
  - Test aggregate metrics validation
  - Test forbidden paths violations

### CLI Tests
- `test_parent_validate_command.py`
  - Test command invocation
  - Test output formatting
  - Test error messages
  - Test file creation

## Edge Cases

1. **No sub-missions defined**: Return INCOMPLETE with clear message
2. **Partial sub-mission completion**: Return INCOMPLETE, list missing validations
3. **Parent has no test_command**: Skip test execution, continue validation
4. **Parent has no aggregate_metrics**: Skip aggregate validation, continue
5. **Sub-mission validation.json corrupted**: Fail with clear error message
6. **Concurrent validation attempts**: File locking or clear error message

## Performance Considerations

- Load sub-mission validations lazily (only when needed)
- Cache parent mission definition to avoid repeated file reads
- Stream test output for long-running parent tests
- Limit aggregate metric prompts to avoid overwhelming Bob

## Security Considerations

- Parent validation.json is immutable (read-only permissions)
- Validate all file paths to prevent directory traversal
- Sanitize test command output before displaying
- Validate metric values to prevent injection attacks

## Rollout Plan

1. **Hour 0-1**: Implement schemas and models
2. **Hour 1-2.5**: Implement service layer
3. **Hour 2.5-3**: Implement CLI command
4. **Hour 3-4**: Write and run tests
5. **Hour 4**: Integration testing and bug fixes

## Success Criteria

- ✅ Command validates all sub-missions passed before proceeding
- ✅ Parent test command executes correctly
- ✅ Aggregate metrics are validated against targets
- ✅ Forbidden paths check covers all sub-mission changes
- ✅ Parent validation.json contains complete evidence
- ✅ Clear pass/fail status with detailed reasons
- ✅ Terminal output shows comprehensive summary
- ✅ Handles edge cases (no sub-missions, partial completion)
- ✅ Integration tests cover various scenarios

## Related Files

### Files to Modify
- [`src/missionforge/models/schemas.py`](../../src/missionforge/models/schemas.py) - Add parent validation models
- [`src/missionforge/core/workspace.py`](../../src/missionforge/core/workspace.py) - Add parent validation paths
- [`src/missionforge/core/exceptions.py`](../../src/missionforge/core/exceptions.py) - Add parent validation exceptions
- [`src/missionforge/cli/commands/validate.py`](../../src/missionforge/cli/commands/validate.py) - Add parent command

### Files to Create
- `src/missionforge/core/parent_validation_service.py` - Parent validation service
- `tests/unit/test_parent_validation_service.py` - Unit tests
- `tests/integration/test_parent_validation_flow.py` - Integration tests
- `tests/integration/test_parent_validate_command.py` - CLI tests

### Files to Reference
- [`src/missionforge/core/validation_service.py`](../../src/missionforge/core/validation_service.py) - Sub-mission validation logic
- [`src/missionforge/testing/executor.py`](../../src/missionforge/testing/executor.py) - Test execution
- [`src/missionforge/utils/path_matching.py`](../../src/missionforge/utils/path_matching.py) - Path validation

## Notes

- This is a **MUST FINISH** feature for project viability
- Estimated effort: 3-4 hours at hackathon pace
- Depends on MF-009 (Sub-Mission Validation) being complete
- Two-level validation is architectural - parent can fail even if all subs pass
- Aggregate metrics catch integration issues individual sub-missions miss