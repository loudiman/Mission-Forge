"""Tests for schema models."""

import pytest
from pydantic import ValidationError

from missionforge.models.schemas import (
    Baseline,
    BaselineMetrics,
    ExecutionPlan,
    MetricDefinition,
    ParentMission,
    SubMission,
    Validation,
    ValidationMetrics,
)


class TestMetricDefinition:
    """Tests for MetricDefinition model."""

    def test_valid_metric_with_min_max(self):
        """Test valid metric with min and max."""
        metric = MetricDefinition(min=0, max=100)
        assert metric.min == 0
        assert metric.max == 100
        assert metric.target is None

    def test_valid_metric_with_target(self):
        """Test valid metric with target only."""
        metric = MetricDefinition(target=50)
        assert metric.target == 50
        assert metric.min is None
        assert metric.max is None

    def test_invalid_metric_no_constraints(self):
        """Test that at least one constraint is required."""
        with pytest.raises(ValidationError) as exc_info:
            MetricDefinition()
        assert "at least one" in str(exc_info.value).lower()

    def test_invalid_metric_min_greater_than_max(self):
        """Test that min cannot be greater than max."""
        with pytest.raises(ValidationError) as exc_info:
            MetricDefinition(min=100, max=50)
        assert "cannot be greater than" in str(exc_info.value).lower()


class TestParentMission:
    """Tests for ParentMission model."""

    def test_valid_parent_mission(self):
        """Test valid parent mission."""
        mission = ParentMission(
            id="MF-001",
            goal="Test mission goal",
            forbidden_paths=["core/**"],
            aggregate_metrics={"total_files": MetricDefinition(max=50)},
            test_command="pytest",
            sub_missions=["MF-001-A"],
        )
        assert mission.id == "MF-001"
        assert mission.goal == "Test mission goal"
        assert len(mission.forbidden_paths) == 1
        assert len(mission.sub_missions) == 1

    def test_valid_mission_id_formats(self):
        """Test various valid mission ID formats."""
        valid_ids = ["MF-001", "AB-999", "PROJ-123", "TEST-001A"]
        for mission_id in valid_ids:
            mission = ParentMission(id=mission_id, goal="Test")
            assert mission.id == mission_id

    def test_invalid_mission_id_formats(self):
        """Test invalid mission ID formats."""
        invalid_ids = [
            "MF001",  # Missing hyphen
            "MF-1",  # Too few digits
            "MF-1234",  # Too many digits
            "mf-001",  # Lowercase
            "M-001",  # Too few letters
            "TOOLONG-001",  # Too many letters
        ]
        for mission_id in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                ParentMission(id=mission_id, goal="Test")
            assert "Invalid mission ID format" in str(exc_info.value)

    def test_empty_goal_rejected(self):
        """Test that empty goal is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            ParentMission(id="MF-001", goal="   ")
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_minimal_parent_mission(self):
        """Test minimal valid parent mission."""
        mission = ParentMission(id="MF-001", goal="Test goal")
        assert mission.id == "MF-001"
        assert mission.goal == "Test goal"
        assert mission.forbidden_paths == []
        assert mission.aggregate_metrics == {}
        assert mission.test_command is None
        assert mission.sub_missions == []


class TestSubMission:
    """Tests for SubMission model."""

    def test_valid_sub_mission(self):
        """Test valid sub-mission."""
        sub = SubMission(
            id="MF-001-A",
            parent="MF-001",
            title="Test sub-mission",
            goal="Test goal",
            depends_on=["MF-001-B"],
            allowed_paths=["src/**"],
            metrics={"files_changed": MetricDefinition(max=10)},
            test_command="pytest tests/",
        )
        assert sub.id == "MF-001-A"
        assert sub.parent == "MF-001"
        assert sub.title == "Test sub-mission"

    def test_valid_sub_mission_id_formats(self):
        """Test various valid sub-mission ID formats."""
        valid_ids = ["MF-001-A", "AB-999-Z", "PROJ-123-B"]
        for sub_id in valid_ids:
            parent_id = sub_id.rsplit("-", 1)[0]
            sub = SubMission(
                id=sub_id, parent=parent_id, title="Test", goal="Test"
            )
            assert sub.id == sub_id

    def test_invalid_sub_mission_id_formats(self):
        """Test invalid sub-mission ID formats."""
        invalid_ids = [
            "MF-001",  # Missing sub-mission letter
            "MF-001-AB",  # Too many letters
            "MF-001-1",  # Number instead of letter
            "mf-001-a",  # Lowercase
        ]
        for sub_id in invalid_ids:
            with pytest.raises(ValidationError) as exc_info:
                SubMission(
                    id=sub_id, parent="MF-001", title="Test", goal="Test"
                )
            assert "Invalid sub-mission ID format" in str(exc_info.value)

    def test_parent_child_mismatch(self):
        """Test that parent-child ID mismatch is detected."""
        with pytest.raises(ValidationError) as exc_info:
            SubMission(
                id="MF-001-A",
                parent="MF-002",  # Wrong parent
                title="Test",
                goal="Test",
            )
        assert "does not match parent" in str(exc_info.value).lower()

    def test_empty_title_rejected(self):
        """Test that empty title is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SubMission(
                id="MF-001-A", parent="MF-001", title="  ", goal="Test"
            )
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_empty_goal_rejected(self):
        """Test that empty goal is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            SubMission(
                id="MF-001-A", parent="MF-001", title="Test", goal="  "
            )
        assert "cannot be empty" in str(exc_info.value).lower()

    def test_minimal_sub_mission(self):
        """Test minimal valid sub-mission."""
        sub = SubMission(
            id="MF-001-A", parent="MF-001", title="Test", goal="Test goal"
        )
        assert sub.id == "MF-001-A"
        assert sub.parent == "MF-001"
        assert sub.depends_on == []
        assert sub.allowed_paths == []
        assert sub.metrics == {}
        assert sub.test_command is None


class TestBaselineMetrics:
    """Tests for BaselineMetrics model."""

    def test_valid_baseline_metrics(self):
        """Test valid baseline metrics."""
        metrics = BaselineMetrics(
            files_changed=5,
            lines_added=100,
            lines_removed=50,
            test_coverage=85.5,
            custom_metrics={"complexity": 42.0},
        )
        assert metrics.files_changed == 5
        assert metrics.lines_added == 100
        assert metrics.lines_removed == 50
        assert metrics.test_coverage == 85.5
        assert metrics.custom_metrics["complexity"] == 42.0

    def test_negative_values_rejected(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError):
            BaselineMetrics(files_changed=-1, lines_added=0, lines_removed=0)

        with pytest.raises(ValidationError):
            BaselineMetrics(files_changed=0, lines_added=-1, lines_removed=0)

        with pytest.raises(ValidationError):
            BaselineMetrics(files_changed=0, lines_added=0, lines_removed=-1)

    def test_invalid_coverage_range(self):
        """Test that coverage must be 0-100."""
        with pytest.raises(ValidationError):
            BaselineMetrics(
                files_changed=0,
                lines_added=0,
                lines_removed=0,
                test_coverage=-1,
            )

        with pytest.raises(ValidationError):
            BaselineMetrics(
                files_changed=0,
                lines_added=0,
                lines_removed=0,
                test_coverage=101,
            )


class TestBaseline:
    """Tests for Baseline model."""

    def test_valid_baseline(self):
        """Test valid baseline."""
        baseline = Baseline(
            mission_id="MF-001",
            timestamp="2024-01-01T00:00:00Z",
            git_commit="abc123def456",
            metrics=BaselineMetrics(
                files_changed=0, lines_added=0, lines_removed=0
            ),
        )
        assert baseline.mission_id == "MF-001"
        assert baseline.git_commit == "abc123def456"

    def test_invalid_git_commit(self):
        """Test that invalid git commit is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Baseline(
                mission_id="MF-001",
                timestamp="2024-01-01T00:00:00Z",
                git_commit="invalid!@#",
                metrics=BaselineMetrics(
                    files_changed=0, lines_added=0, lines_removed=0
                ),
            )
        assert "Invalid git commit hash" in str(exc_info.value)


class TestValidationMetrics:
    """Tests for ValidationMetrics model."""

    def test_valid_validation_metrics(self):
        """Test valid validation metrics."""
        metrics = ValidationMetrics(
            files_changed=5,
            lines_added=100,
            lines_removed=50,
            test_coverage=90.0,
            tests_passed=True,
            custom_metrics={"complexity": 40.0},
        )
        assert metrics.files_changed == 5
        assert metrics.tests_passed is True


class TestValidation:
    """Tests for Validation model."""

    def test_valid_validation(self):
        """Test valid validation."""
        validation = Validation(
            mission_id="MF-001",
            timestamp="2024-01-01T00:00:00Z",
            git_commit="abc123def456",
            metrics=ValidationMetrics(
                files_changed=5,
                lines_added=100,
                lines_removed=50,
                tests_passed=True,
            ),
            passed=True,
            errors=[],
        )
        assert validation.mission_id == "MF-001"
        assert validation.passed is True
        assert len(validation.errors) == 0

    def test_validation_with_errors(self):
        """Test validation with errors."""
        validation = Validation(
            mission_id="MF-001",
            timestamp="2024-01-01T00:00:00Z",
            git_commit="abc123def456",
            metrics=ValidationMetrics(
                files_changed=5,
                lines_added=100,
                lines_removed=50,
                tests_passed=False,
            ),
            passed=False,
            errors=["Test failed", "Coverage too low"],
        )
        assert validation.passed is False
        assert len(validation.errors) == 2


class TestExecutionPlan:
    """Tests for ExecutionPlan model."""

    def test_valid_execution_plan(self):
        """Test valid execution plan."""
        plan = ExecutionPlan(
            execution_order=["MF-001-A", "MF-001-B", "MF-001-C"],
            dependency_graph={
                "MF-001-A": [],
                "MF-001-B": ["MF-001-A"],
                "MF-001-C": ["MF-001-B"],
            },
        )
        assert len(plan.execution_order) == 3
        assert len(plan.dependency_graph) == 3

    def test_empty_execution_plan(self):
        """Test empty execution plan."""
        plan = ExecutionPlan()
        assert plan.execution_order == []
        assert plan.dependency_graph == {}

    def test_missing_dependency_in_execution_order(self):
        """Test that dependencies must be in execution order."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutionPlan(
                execution_order=["MF-001-A"],
                dependency_graph={"MF-001-A": ["MF-001-B"]},  # B not in order
            )
        assert "not found in execution order" in str(exc_info.value).lower()

    def test_mission_in_graph_not_in_order(self):
        """Test that all missions in graph must be in execution order."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutionPlan(
                execution_order=["MF-001-A"],
                dependency_graph={
                    "MF-001-A": [],
                    "MF-001-B": [],  # B not in execution order
                },
            )
        assert "not found in execution order" in str(exc_info.value).lower()

    def test_circular_dependency_detected(self):
        """Test that circular dependencies are detected."""
        with pytest.raises(ValidationError) as exc_info:
            ExecutionPlan(
                execution_order=["MF-001-A", "MF-001-B"],
                dependency_graph={
                    "MF-001-A": ["MF-001-B"],
                    "MF-001-B": ["MF-001-A"],  # Circular!
                },
            )
        assert "circular dependency" in str(exc_info.value).lower()

    def test_complex_dependency_graph(self):
        """Test complex but valid dependency graph."""
        plan = ExecutionPlan(
            execution_order=["MF-001-A", "MF-001-B", "MF-001-C", "MF-001-D"],
            dependency_graph={
                "MF-001-A": [],
                "MF-001-B": ["MF-001-A"],
                "MF-001-C": ["MF-001-A"],
                "MF-001-D": ["MF-001-B", "MF-001-C"],
            },
        )
        assert len(plan.execution_order) == 4
        assert len(plan.dependency_graph["MF-001-D"]) == 2


# Made with Bob