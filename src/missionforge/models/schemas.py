"""Pydantic models for mission schemas."""


from pydantic import BaseModel, Field, field_validator, model_validator


class MetricDefinition(BaseModel):
    """Definition of a metric with constraints."""

    min: float | None = Field(None, description="Minimum allowed value")
    max: float | None = Field(None, description="Maximum allowed value")
    target: float | None = Field(None, description="Target value")

    @model_validator(mode="after")
    def validate_constraints(self) -> "MetricDefinition":
        """Ensure at least one constraint is defined."""
        if self.min is None and self.max is None and self.target is None:
            raise ValueError("At least one of min, max, or target must be specified")
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError(f"min ({self.min}) cannot be greater than max ({self.max})")
        return self


class ParentMission(BaseModel):
    """Parent mission schema."""

    id: str = Field(..., description="Mission identifier (e.g., MF-001)")
    goal: str = Field(..., description="High-level mission goal")
    forbidden_paths: list[str] = Field(
        default_factory=list, description="Path patterns that sub-missions cannot modify"
    )
    aggregate_metrics: dict[str, MetricDefinition] = Field(
        default_factory=dict, description="Aggregate metrics across all sub-missions"
    )
    test_command: str | None = Field(
        None, description="Command to run tests for mission validation"
    )
    sub_missions: list[str] = Field(
        default_factory=list, description="List of sub-mission IDs"
    )

    @field_validator("id")
    @classmethod
    def validate_mission_id(cls, v: str) -> str:
        """Validate mission ID format."""
        import re

        pattern = r"^[A-Z]{2,4}-\d{3}[A-Z]?$"
        if not re.match(pattern, v):
            raise ValueError(
                f"Invalid mission ID format: {v}. "
                "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001, FG-042A)"
            )
        return v

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        """Ensure goal is not empty."""
        if not v.strip():
            raise ValueError("Mission goal cannot be empty")
        return v

    @field_validator("forbidden_paths")
    @classmethod
    def validate_forbidden_paths(cls, v: list[str]) -> list[str]:
        """Validate path glob patterns."""
        import pathspec

        for pattern in v:
            try:
                pathspec.PathSpec.from_lines("gitwildmatch", [pattern])
            except Exception as e:
                raise ValueError(f"Invalid path pattern '{pattern}': {e}") from e
        return v


class SubMission(BaseModel):
    """Sub-mission schema."""

    id: str = Field(..., description="Sub-mission identifier (e.g., MF-001-A)")
    parent: str = Field(..., description="Parent mission ID")
    title: str = Field(..., description="Short descriptive title")
    goal: str = Field(..., description="Specific goal for this sub-mission")
    depends_on: list[str] = Field(
        default_factory=list, description="List of sub-mission IDs this depends on"
    )
    allowed_paths: list[str] = Field(
        default_factory=list, description="Path patterns this sub-mission can modify"
    )
    metrics: dict[str, MetricDefinition] = Field(
        default_factory=dict, description="Metrics for this sub-mission"
    )
    test_command: str | None = Field(
        None, description="Command to run tests for this sub-mission"
    )

    @field_validator("id")
    @classmethod
    def validate_sub_mission_id(cls, v: str) -> str:
        """Validate sub-mission ID format."""
        import re

        pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
        if not re.match(pattern, v):
            raise ValueError(
                f"Invalid sub-mission ID format: {v}. "
                "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}-[A-Z] (e.g., MF-001-A)"
            )
        return v

    @field_validator("parent")
    @classmethod
    def validate_parent_id(cls, v: str) -> str:
        """Validate parent mission ID format."""
        import re

        pattern = r"^[A-Z]{2,4}-\d{3}[A-Z]?$"
        if not re.match(pattern, v):
            raise ValueError(
                f"Invalid parent mission ID format: {v}. "
                "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001)"
            )
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Ensure title is not empty."""
        if not v.strip():
            raise ValueError("Sub-mission title cannot be empty")
        return v

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        """Ensure goal is not empty."""
        if not v.strip():
            raise ValueError("Sub-mission goal cannot be empty")
        return v

    @field_validator("allowed_paths")
    @classmethod
    def validate_allowed_paths(cls, v: list[str]) -> list[str]:
        """Validate path glob patterns."""
        import pathspec

        for pattern in v:
            try:
                pathspec.PathSpec.from_lines("gitwildmatch", [pattern])
            except Exception as e:
                raise ValueError(f"Invalid path pattern '{pattern}': {e}") from e
        return v

    @model_validator(mode="after")
    def validate_parent_child_relationship(self) -> "SubMission":
        """Ensure sub-mission ID matches parent ID."""
        # Extract parent prefix from sub-mission ID
        parts = self.id.rsplit("-", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid sub-mission ID format: {self.id}")

        expected_parent = parts[0]
        if self.parent != expected_parent:
            raise ValueError(
                f"Sub-mission ID '{self.id}' does not match parent ID '{self.parent}'. "
                f"Expected parent: '{expected_parent}'"
            )
        return self


class BaselineMetrics(BaseModel):
    """Baseline metrics captured before mission starts."""

    files_changed: int = Field(..., description="Number of files changed")
    lines_added: int = Field(..., description="Number of lines added")
    lines_removed: int = Field(..., description="Number of lines removed")
    test_coverage: float | None = Field(None, description="Test coverage percentage")
    custom_metrics: dict[str, float] = Field(
        default_factory=dict, description="Custom metrics defined by mission"
    )

    @field_validator("files_changed", "lines_added", "lines_removed")
    @classmethod
    def validate_non_negative(cls, v: int) -> int:
        """Ensure counts are non-negative."""
        if v < 0:
            raise ValueError("Metric values cannot be negative")
        return v

    @field_validator("test_coverage")
    @classmethod
    def validate_coverage(cls, v: float | None) -> float | None:
        """Ensure coverage is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Test coverage must be between 0 and 100")
        return v


class Baseline(BaseModel):
    """Baseline state for a mission or sub-mission."""

    mission_id: str = Field(..., description="Mission or sub-mission ID")
    timestamp: str = Field(..., description="ISO 8601 timestamp of baseline capture")
    git_commit: str = Field(..., description="Git commit hash at baseline")
    metrics: BaselineMetrics = Field(..., description="Captured metrics")

    @field_validator("git_commit")
    @classmethod
    def validate_git_commit(cls, v: str) -> str:
        """Validate git commit hash format."""
        import re

        if not re.match(r"^[0-9a-f]{7,40}$", v):
            raise ValueError(f"Invalid git commit hash: {v}")
        return v


class ValidationMetrics(BaseModel):
    """Validation metrics captured after mission completion."""

    files_changed: int = Field(..., description="Number of files changed")
    lines_added: int = Field(..., description="Number of lines added")
    lines_removed: int = Field(..., description="Number of lines removed")
    test_coverage: float | None = Field(None, description="Test coverage percentage")
    tests_passed: bool = Field(..., description="Whether all tests passed")
    custom_metrics: dict[str, float] = Field(
        default_factory=dict, description="Custom metrics defined by mission"
    )

    @field_validator("files_changed", "lines_added", "lines_removed")
    @classmethod
    def validate_non_negative(cls, v: int) -> int:
        """Ensure counts are non-negative."""
        if v < 0:
            raise ValueError("Metric values cannot be negative")
        return v

    @field_validator("test_coverage")
    @classmethod
    def validate_coverage(cls, v: float | None) -> float | None:
        """Ensure coverage is between 0 and 100."""
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Test coverage must be between 0 and 100")
        return v


class Validation(BaseModel):
    """Validation state for a mission or sub-mission."""

    mission_id: str = Field(..., description="Mission or sub-mission ID")
    timestamp: str = Field(..., description="ISO 8601 timestamp of validation")
    git_commit: str = Field(..., description="Git commit hash at validation")
    metrics: ValidationMetrics = Field(..., description="Captured metrics")
    passed: bool = Field(..., description="Whether validation passed all checks")
    errors: list[str] = Field(default_factory=list, description="Validation errors if any")

    @field_validator("git_commit")
    @classmethod
    def validate_git_commit(cls, v: str) -> str:
        """Validate git commit hash format."""
        import re

        if not re.match(r"^[0-9a-f]{7,40}$", v):
            raise ValueError(f"Invalid git commit hash: {v}")
        return v


class ExecutionPlan(BaseModel):
    """Execution plan with dependency graph."""

    execution_order: list[str] = Field(
        default_factory=list, description="Ordered list of sub-mission IDs to execute"
    )
    dependency_graph: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Map of sub-mission ID to list of dependencies",
    )

    @model_validator(mode="after")
    def validate_dependencies(self) -> "ExecutionPlan":
        """Validate dependency graph consistency."""
        # Check all dependencies exist in execution order
        all_missions = set(self.execution_order)
        for mission_id, deps in self.dependency_graph.items():
            if mission_id not in all_missions:
                raise ValueError(
                    f"Mission '{mission_id}' in dependency graph "
                    f"not found in execution order"
                )
            for dep in deps:
                if dep not in all_missions:
                    raise ValueError(
                        f"Dependency '{dep}' for mission '{mission_id}' "
                        f"not found in execution order"
                    )

        # Check for circular dependencies
        visited = set()
        rec_stack = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.dependency_graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for mission_id in self.dependency_graph:
            if mission_id not in visited:
                if has_cycle(mission_id):
                    raise ValueError("Circular dependency detected in execution plan")

        return self

class SubMissionBaselineMetric(BaseModel):
    """A single metric in a sub-mission baseline."""

    metric_id: str = Field(..., description="Unique identifier for the metric")
    description: str = Field(..., description="Human-readable description of what is measured")
    baseline_target: bool | int | float | str = Field(
        ..., description="Expected baseline value before implementation"
    )
    value: bool | int | float | str | None = Field(
        None, description="Actual measured value (null until filled by Bob)"
    )

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, v: str) -> str:
        """Ensure metric_id is not empty."""
        if not v.strip():
            raise ValueError("metric_id cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Ensure description is not empty."""
        if not v.strip():
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_value_type(self) -> "SubMissionBaselineMetric":
        """Ensure value type matches baseline_target type when value is not None."""
        if self.value is not None:
            target_type = type(self.baseline_target)
            value_type = type(self.value)
            if target_type != value_type:
                raise ValueError(
                    f"Value type ({value_type.__name__}) does not match "
                    f"baseline_target type ({target_type.__name__})"
                )
        return self


class SubMissionBaseline(BaseModel):
    """Baseline for sub-mission custom metrics."""

    sub_mission_id: str = Field(..., description="Sub-mission identifier (e.g., MF-001-A)")
    timestamp: str | None = Field(
        None, description="ISO 8601 timestamp when baseline was committed"
    )
    status: str | None = Field(
        None, description="Baseline status: 'captured' or 'committed'"
    )
    metrics: list[SubMissionBaselineMetric] = Field(
        ..., description="List of baseline metrics"
    )

    @field_validator("sub_mission_id")
    @classmethod
    def validate_sub_mission_id(cls, v: str) -> str:
        """Validate sub-mission ID format."""
        import re

        pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
        if not re.match(pattern, v):
            raise ValueError(
                f"Invalid sub-mission ID format: {v}. "
                "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}-[A-Z] (e.g., MF-001-A)"
            )
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Validate status is one of allowed values."""
        if v is not None and v not in ("captured", "committed"):
            raise ValueError(f"Invalid status: {v}. Must be 'captured' or 'committed'")
        return v

    @field_validator("metrics")
    @classmethod
    def validate_metrics_not_empty(cls, v: list[SubMissionBaselineMetric]) -> list[SubMissionBaselineMetric]:
        """Ensure at least one metric is defined."""
        if not v:
            raise ValueError("At least one metric must be defined")
        return v



# Made with Bob
