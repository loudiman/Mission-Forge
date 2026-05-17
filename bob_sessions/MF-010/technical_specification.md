∑# MF-010: Parent Mission Validation - Technical Specification

## API Contracts

### 1. ParentValidationService API

```python
class ParentValidationService:
    """Service for parent mission validation."""
    
    def __init__(self, workspace: Workspace | None = None):
        """Initialize service with workspace."""
        self.workspace = workspace or Workspace()
    
    def validate_parent_mission(self, mission_id: str) -> Path:
        """Execute complete parent validation flow.
        
        Args:
            mission_id: Parent mission identifier (e.g., 'MF-001')
            
        Returns:
            Path to created validation.json
            
        Raises:
            ParentValidationIncompleteError: Not all sub-missions validated
            ParentValidationFailedError: Validation checks failed
            ParentTestFailedError: Parent test command failed
            AggregateMetricFailedError: Aggregate metric validation failed
            ForbiddenPathViolationError: Forbidden paths violated
        """
        pass
    
    def _load_parent_mission(self, mission_id: str) -> ParentMission:
        """Load and validate parent mission definition."""
        pass
    
    def _aggregate_sub_missions(
        self, 
        mission_id: str, 
        sub_mission_ids: list[str]
    ) -> SubMissionsAggregate:
        """Load and aggregate all sub-mission validation results."""
        pass
    
    def _execute_parent_test(
        self, 
        test_command: str, 
        cwd: Path
    ) -> ParentTestResult:
        """Execute parent-level test command."""
        pass
    
    def _validate_aggregate_metrics(
        self,
        mission_id: str,
        metrics_def: dict[str, MetricDefinition]
    ) -> list[AggregateMetricResult]:
        """Prompt Bob and validate aggregate metrics."""
        pass
    
    def _check_forbidden_paths(
        self,
        mission_id: str,
        sub_mission_ids: list[str],
        forbidden_paths: list[str]
    ) -> ForbiddenPathsCheck:
        """Check forbidden paths across all sub-missions."""
        pass
    
    def _determine_parent_status(
        self,
        sub_missions: SubMissionsAggregate,
        parent_test: ParentTestResult | None,
        aggregate_metrics: list[AggregateMetricResult],
        forbidden_check: ForbiddenPathsCheck
    ) -> str:
        """Determine overall parent mission status."""
        pass
```

### 2. CLI Command API

```python
@app.command("parent")
def validate_parent(
    mission_id: str = typer.Argument(
        ..., 
        help="Parent mission ID (e.g., MF-001)"
    ),
) -> None:
    """Validate parent mission after all sub-missions complete.
    
    This command:
    1. Verifies all sub-missions have validation.json files
    2. Checks all sub-missions have PASSED status
    3. Runs parent-level test_command if defined
    4. Prompts Bob to measure aggregate_metrics if defined
    5. Validates aggregate metrics against targets
    6. Checks forbidden_paths across all sub-mission changes
    7. Determines overall parent mission pass/fail status
    8. Writes immutable parent validation.json
    
    Examples:
        missionforge validate parent MF-001
    """
    pass
```

### 3. Workspace API Extensions

```python
class Workspace:
    """Existing workspace class with new methods."""
    
    def parent_validation_path(self, mission_id: str) -> Path:
        """Get path to parent validation.json.
        
        Args:
            mission_id: Parent mission identifier (e.g., 'MF-001')
            
        Returns:
            Path to .missionforge/missions/{mission_id}/validation.json
        """
        return self.mission_path(mission_id) / "validation.json"
```

## Data Models (Pydantic)

### Core Models

```python
class SubMissionSummary(BaseModel):
    """Summary of a single sub-mission's validation status."""
    
    id: str = Field(..., description="Sub-mission ID (e.g., MF-001-A)")
    status: str = Field(..., description="PASSED, FAILED, or BLOCKED")
    timestamp: str | None = Field(None, description="ISO 8601 timestamp")
    
    @field_validator("id")
    @classmethod
    def validate_sub_mission_id(cls, v: str) -> str:
        pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
        if not re.match(pattern, v):
            raise ValueError(f"Invalid sub-mission ID format: {v}")
        return v
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ("PASSED", "FAILED", "BLOCKED"):
            raise ValueError(f"Invalid status: {v}")
        return v


class SubMissionsAggregate(BaseModel):
    """Aggregate summary of all sub-missions."""
    
    total: int = Field(..., description="Total number of sub-missions")
    passed: int = Field(..., description="Number of PASSED sub-missions")
    failed: int = Field(..., description="Number of FAILED sub-missions")
    blocked: int = Field(..., description="Number of BLOCKED sub-missions")
    details: list[SubMissionSummary] = Field(
        default_factory=list,
        description="Detailed status of each sub-mission"
    )
    
    @field_validator("total", "passed", "failed", "blocked")
    @classmethod
    def validate_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Count cannot be negative")
        return v
    
    @model_validator(mode="after")
    def validate_counts(self) -> "SubMissionsAggregate":
        """Ensure counts add up correctly."""
        if self.passed + self.failed + self.blocked != self.total:
            raise ValueError("Sub-mission counts do not match total")
        if len(self.details) != self.total:
            raise ValueError("Details count does not match total")
        return self


class AggregateMetricResult(BaseModel):
    """Result of an aggregate metric validation."""
    
    metric_id: str = Field(..., description="Unique metric identifier")
    baseline_value: bool | int | float | str | None = Field(
        None, 
        description="Baseline value if available"
    )
    target_value: bool | int | float | str = Field(
        ..., 
        description="Target value from mission definition"
    )
    final_value: bool | int | float | str | None = Field(
        None, 
        description="Final measured value (filled by Bob)"
    )
    status: str = Field(..., description="PASSED or FAILED")
    
    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("metric_id cannot be empty")
        return v
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ("PASSED", "FAILED"):
            raise ValueError(f"Invalid status: {v}")
        return v


class ParentTestResult(BaseModel):
    """Parent-level test execution result."""
    
    command: str = Field(..., description="Test command executed")
    exit_code: int = Field(..., description="Process exit code")
    output: str = Field(..., description="Combined stdout/stderr")
    passed: bool = Field(..., description="Whether tests passed")
    duration: float = Field(..., description="Execution time in seconds")
    
    @field_validator("duration")
    @classmethod
    def validate_duration(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Duration cannot be negative")
        return v


class ForbiddenPathsCheck(BaseModel):
    """Cross-sub-mission forbidden paths validation."""
    
    violated: bool = Field(..., description="Whether any paths violated")
    violations: list[str] = Field(
        default_factory=list,
        description="List of violating file paths"
    )


class ParentMissionValidation(BaseModel):
    """Complete parent mission validation state."""
    
    mission_id: str = Field(..., description="Parent mission ID")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    status: str = Field(..., description="PASSED, FAILED, or INCOMPLETE")
    sub_missions: SubMissionsAggregate = Field(
        ..., 
        description="Aggregate sub-mission status"
    )
    aggregate_metrics: list[AggregateMetricResult] = Field(
        default_factory=list,
        description="Aggregate metric validation results"
    )
    parent_test: ParentTestResult | None = Field(
        None,
        description="Parent test execution result"
    )
    forbidden_paths_check: ForbiddenPathsCheck = Field(
        ...,
        description="Forbidden paths validation result"
    )
    
    @field_validator("mission_id")
    @classmethod
    def validate_mission_id(cls, v: str) -> str:
        pattern = r"^[A-Z]{2,4}-\d{3}[A-Z]?$"
        if not re.match(pattern, v):
            raise ValueError(f"Invalid mission ID format: {v}")
        return v
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in ("PASSED", "FAILED", "INCOMPLETE"):
            raise ValueError(f"Invalid status: {v}")
        return v
```

## Exception Hierarchy

```python
class ParentValidationError(MissionForgeError):
    """Base exception for parent validation errors."""
    pass


class ParentValidationIncompleteError(ParentValidationError):
    """Raised when not all sub-missions have validation.json."""
    
    def __init__(self, mission_id: str, missing_subs: list[str]):
        missing_list = "\n  • ".join(missing_subs)
        super().__init__(
            f"Parent mission {mission_id} cannot be validated - "
            f"missing validation.json for:\n  • {missing_list}",
            "Run 'missionforge validate capture <id>' and commit for each sub-mission"
        )


class ParentValidationFailedError(ParentValidationError):
    """Raised when parent validation fails."""
    
    def __init__(self, mission_id: str, reason: str):
        super().__init__(
            f"Parent mission {mission_id} validation failed: {reason}",
            "Review and fix the issues before re-validating"
        )


class ParentTestFailedError(ParentValidationError):
    """Raised when parent test command fails."""
    
    def __init__(self, mission_id: str, exit_code: int, output: str):
        super().__init__(
            f"Parent test for {mission_id} failed (exit code: {exit_code})\n"
            f"Output:\n{output[:500]}",
            "Fix test failures before proceeding with validation"
        )


class AggregateMetricFailedError(ParentValidationError):
    """Raised when aggregate metric validation fails."""
    
    def __init__(self, mission_id: str, failed_metrics: list[str]):
        metrics_list = "\n  • ".join(failed_metrics)
        super().__init__(
            f"Aggregate metrics failed for {mission_id}:\n  • {metrics_list}",
            "Review sub-mission implementations to meet aggregate targets"
        )


class ForbiddenPathViolationError(ParentValidationError):
    """Raised when forbidden paths are violated across sub-missions."""
    
    def __init__(self, mission_id: str, violations: list[str]):
        violations_list = "\n  • ".join(violations)
        super().__init__(
            f"Forbidden path violations detected for {mission_id}:\n  • {violations_list}",
            "Ensure no sub-mission modifies forbidden paths"
        )
```

## Implementation Details

### 1. Sub-Mission Aggregation

```python
def _aggregate_sub_missions(
    self, 
    mission_id: str, 
    sub_mission_ids: list[str]
) -> SubMissionsAggregate:
    """Load and aggregate all sub-mission validation results."""
    
    details: list[SubMissionSummary] = []
    passed = failed = blocked = 0
    missing: list[str] = []
    
    for sub_id in sub_mission_ids:
        validation_path = self.workspace.validation_path(sub_id)
        
        if not validation_path.exists():
            missing.append(sub_id)
            continue
        
        with open(validation_path) as f:
            data = json.load(f)
        
        validation = SubMissionValidation(**data)
        status = validation.status
        
        if status == "PASSED":
            passed += 1
        elif status == "FAILED":
            failed += 1
        elif status == "BLOCKED":
            blocked += 1
        
        details.append(SubMissionSummary(
            id=sub_id,
            status=status,
            timestamp=validation.timestamp
        ))
    
    if missing:
        raise ParentValidationIncompleteError(mission_id, missing)
    
    return SubMissionsAggregate(
        total=len(sub_mission_ids),
        passed=passed,
        failed=failed,
        blocked=blocked,
        details=details
    )
```

### 2. Parent Test Execution

```python
def _execute_parent_test(
    self, 
    test_command: str, 
    cwd: Path
) -> ParentTestResult:
    """Execute parent-level test command."""
    
    cmd = shlex.split(test_command)
    result = execute_test_command(cmd, cwd=cwd)
    
    combined_output = (result.stdout + "\n" + result.stderr).strip()
    
    return ParentTestResult(
        command=test_command,
        exit_code=result.exit_code,
        output=combined_output,
        passed=result.success,
        duration=round(result.duration, 2)
    )
```

### 3. Aggregate Metrics Validation

```python
def _validate_aggregate_metrics(
    self,
    mission_id: str,
    metrics_def: dict[str, MetricDefinition]
) -> list[AggregateMetricResult]:
    """Prompt Bob and validate aggregate metrics."""
    
    results: list[AggregateMetricResult] = []
    
    # Create todo structure for Bob
    todo_metrics = []
    for metric_id, metric_def in metrics_def.items():
        todo_metrics.append({
            "metric_id": metric_id,
            "target_value": metric_def.target,
            "final_value": None,  # Bob fills this
            "description": f"Aggregate metric: {metric_id}"
        })
    
    # TODO: Implement Bob prompting mechanism
    # For now, assume Bob has filled values
    
    for metric_data in todo_metrics:
        if metric_data["final_value"] is None:
            raise ValidationIncompleteError(
                mission_id, 
                [metric_data["metric_id"]]
            )
        
        # Use same validation logic as sub-mission metrics
        status = self._determine_metric_status(
            final_value=metric_data["final_value"],
            target_value=metric_data["target_value"],
            baseline_value=None
        )
        
        results.append(AggregateMetricResult(
            metric_id=metric_data["metric_id"],
            baseline_value=None,
            target_value=metric_data["target_value"],
            final_value=metric_data["final_value"],
            status=status
        ))
    
    return results
```

### 4. Forbidden Paths Check

```python
def _check_forbidden_paths(
    self,
    mission_id: str,
    sub_mission_ids: list[str],
    forbidden_paths: list[str]
) -> ForbiddenPathsCheck:
    """Check forbidden paths across all sub-missions."""
    
    all_changed_files: list[str] = []
    
    # Collect all changed files from all sub-missions
    for sub_id in sub_mission_ids:
        validation_path = self.workspace.validation_path(sub_id)
        
        with open(validation_path) as f:
            data = json.load(f)
        
        validation = SubMissionValidation(**data)
        all_changed_files.extend(
            validation.deterministic_evidence.files_changed
        )
    
    # Remove duplicates
    all_changed_files = list(set(all_changed_files))
    
    # Check against forbidden paths
    from ..utils.path_matching import validate_paths_against_scope
    
    result = validate_paths_against_scope(
        changed_files=[Path(f) for f in all_changed_files],
        allowed_patterns=[],  # Not checking allowed for parent
        forbidden_patterns=forbidden_paths
    )
    
    violations = result["forbidden_files"]
    
    return ForbiddenPathsCheck(
        violated=len(violations) > 0,
        violations=violations
    )
```

### 5. Status Determination

```python
def _determine_parent_status(
    self,
    sub_missions: SubMissionsAggregate,
    parent_test: ParentTestResult | None,
    aggregate_metrics: list[AggregateMetricResult],
    forbidden_check: ForbiddenPathsCheck
) -> str:
    """Determine overall parent mission status."""
    
    # INCOMPLETE: Not all sub-missions validated
    # (Already checked in _aggregate_sub_missions)
    
    # FAILED: Any sub-mission not PASSED
    if sub_missions.failed > 0 or sub_missions.blocked > 0:
        return "FAILED"
    
    # FAILED: Parent test failed
    if parent_test is not None and not parent_test.passed:
        return "FAILED"
    
    # FAILED: Any aggregate metric failed
    if any(m.status == "FAILED" for m in aggregate_metrics):
        return "FAILED"
    
    # FAILED: Forbidden paths violated
    if forbidden_check.violated:
        return "FAILED"
    
    # PASSED: All checks passed
    return "PASSED"
```

## CLI Output Format

### Success Case

```
$ missionforge validate parent MF-001

✓ Loading parent mission MF-001...

✓ Checking sub-missions (4 total)...
  ✓ MF-001-A: PASSED (2026-05-16T17:00:00Z)
  ✓ MF-001-B: PASSED (2026-05-16T17:15:00Z)
  ✓ MF-001-C: PASSED (2026-05-16T17:30:00Z)
  ✓ MF-001-D: PASSED (2026-05-16T17:45:00Z)

✓ Running parent tests...
  Command: ./gradlew integrationTest && pytest tests/integration
  Duration: 45.2s
  Status: PASSED

⚠ Measuring aggregate metrics (2 metrics)...
  Please analyze implementation and fill final_value in validation.todo.json
  
[After Bob fills metrics]

✓ Validating aggregate metrics...
  ┌─────────────────────────┬──────────┬────────┬───────┬────────┐
  │ Metric                  │ Baseline │ Target │ Final │ Status │
  ├─────────────────────────┼──────────┼────────┼───────┼────────┤
  │ total_corba_references  │ 7        │ 0      │ 0     │ PASSED │
  │ integration_coverage    │ 45.0     │ 80.0   │ 85.0  │ PASSED │
  └─────────────────────────┴──────────┴────────┴───────┴────────┘

✓ Checking forbidden paths...
  No violations detected

✓ Parent Mission Validation: PASSED
  Committed: .missionforge/missions/MF-001/validation.json
  
⚠️  validation.json is now immutable
```

### Failure Cases

#### Sub-Mission Not Validated
```
$ missionforge validate parent MF-001

✓ Loading parent mission MF-001...

✗ Checking sub-missions...
  Error: Missing validation.json for:
    • MF-001-B
    • MF-001-D
  
💡 Suggestion: Run 'missionforge validate capture <id>' and commit for each sub-mission
```

#### Sub-Mission Failed
```
$ missionforge validate parent MF-001

✓ Loading parent mission MF-001...

✗ Checking sub-missions (4 total)...
  ✓ MF-001-A: PASSED
  ✗ MF-001-B: FAILED
  ✓ MF-001-C: PASSED
  ✗ MF-001-D: BLOCKED

Error: Cannot validate parent - 1 sub-mission(s) FAILED, 1 BLOCKED
💡 Suggestion: Fix issues in failed sub-missions and re-validate before parent validation
```

#### Parent Test Failed
```
$ missionforge validate parent MF-001

✓ Loading parent mission MF-001...
✓ Checking sub-missions (4 total)... All PASSED

✗ Running parent tests...
  Command: ./gradlew integrationTest
  Duration: 12.3s
  Exit Code: 1
  
  Output:
  > Task :integrationTest FAILED
  
  IntegrationTest > testCrossModuleInteraction FAILED
      Expected: 0 CORBA references
      Actual: 3 CORBA references found
  
Error: Parent test command failed (exit code: 1)
💡 Suggestion: Fix integration test failures before proceeding with validation
```

## Testing Strategy

### Unit Tests

```python
# tests/unit/test_parent_validation_service.py

def test_aggregate_sub_missions_all_passed():
    """Test aggregation when all sub-missions passed."""
    # Setup: Create mock sub-mission validation.json files
    # Execute: Call _aggregate_sub_missions
    # Assert: total=4, passed=4, failed=0, blocked=0

def test_aggregate_sub_missions_with_failures():
    """Test aggregation with mixed statuses."""
    # Setup: Create sub-missions with PASSED, FAILED, BLOCKED
    # Execute: Call _aggregate_sub_missions
    # Assert: Correct counts for each status

def test_aggregate_sub_missions_missing_validation():
    """Test error when validation.json missing."""
    # Setup: Create sub-missions without validation.json
    # Execute: Call _aggregate_sub_missions
    # Assert: Raises ParentValidationIncompleteError

def test_determine_parent_status_all_passed():
    """Test status determination when all checks pass."""
    # Setup: Create passing sub-missions, test, metrics, paths
    # Execute: Call _determine_parent_status
    # Assert: Returns "PASSED"

def test_determine_parent_status_sub_failed():
    """Test status when sub-mission failed."""
    # Setup: Create sub-missions with one FAILED
    # Execute: Call _determine_parent_status
    # Assert: Returns "FAILED"

def test_check_forbidden_paths_no_violations():
    """Test forbidden paths check with no violations."""
    # Setup: Create sub-missions with allowed file changes
    # Execute: Call _check_forbidden_paths
    # Assert: violated=False, violations=[]

def test_check_forbidden_paths_with_violations():
    """Test forbidden paths check with violations."""
    # Setup: Create sub-missions with forbidden file changes
    # Execute: Call _check_forbidden_paths
    # Assert: violated=True, violations contains files
```

### Integration Tests

```python
# tests/integration/test_parent_validation_flow.py

def test_parent_validation_happy_path():
    """Test complete parent validation flow - all passing."""
    # Setup: Create parent mission with 4 sub-missions, all PASSED
    # Execute: validate_parent_mission("MF-001")
    # Assert: validation.json created, status=PASSED

def test_parent_validation_with_test_command():
    """Test parent validation with test execution."""
    # Setup: Parent mission with test_command
    # Execute: validate_parent_mission
    # Assert: Test executed, results captured

def test_parent_validation_aggregate_metrics():
    """Test parent validation with aggregate metrics."""
    # Setup: Parent mission with aggregate_metrics
    # Execute: validate_parent_mission (with Bob filling metrics)
    # Assert: Metrics validated, results captured

def test_parent_validation_immutable_file():
    """Test validation.json is immutable."""
    # Setup: Complete parent validation
    # Execute: Try to modify validation.json
    # Assert: PermissionError raised

def test_parent_validation_missing_sub_mission():
    """Test error when sub-mission not validated."""
    # Setup: Parent with 4 subs, only 3 have validation.json
    # Execute: validate_parent_mission
    # Assert: ParentValidationIncompleteError raised
```

## Performance Benchmarks

| Operation | Target Time | Max Time | Notes |
|-----------|-------------|----------|-------|
| Load parent mission | < 10ms | 50ms | YAML parsing |
| Aggregate 10 sub-missions | < 100ms | 500ms | JSON loading |
| Execute parent tests | Variable | N/A | Depends on test suite |
| Validate 5 metrics | < 50ms | 200ms | Computation only |
| Check 100 paths | < 100ms | 500ms | Pattern matching |
| Write validation.json | < 50ms | 200ms | File I/O |
| **Total (excluding tests)** | < 500ms | 2s | End-to-end |

## Migration Path

Since this is a new feature, no migration is needed. However:

1. Existing missions without parent validation.json continue to work
2. Parent validation is optional until explicitly run
3. No breaking changes to existing APIs
4. Backward compatible with existing validation.json format

## Future Enhancements

1. **Parallel Sub-Mission Loading**: Load validation.json files in parallel
2. **Incremental Validation**: Only re-validate changed sub-missions
3. **Validation Caching**: Cache validation results for performance
4. **Custom Validators**: Plugin system for domain-specific validation
5. **Validation Reports**: Generate HTML/PDF reports from validation.json
6. **Notification System**: Webhooks for validation completion
7. **Validation History**: Track validation history over time
8. **Rollback Support**: Rollback to previous validation state