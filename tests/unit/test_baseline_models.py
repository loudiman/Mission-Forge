"""Unit tests for baseline Pydantic models."""

import pytest
from pydantic import ValidationError

from missionforge.models.schemas import SubMissionBaseline, SubMissionBaselineMetric


class TestSubMissionBaselineMetric:
    """Tests for SubMissionBaselineMetric model."""

    def test_valid_metric_with_bool_target(self):
        """Test creating metric with boolean target."""
        metric = SubMissionBaselineMetric(
            metric_id="rest_endpoint_exists",
            description="Check if REST endpoint exists",
            baseline_target=True,
            value=None,
        )
        assert metric.metric_id == "rest_endpoint_exists"
        assert metric.baseline_target is True
        assert metric.value is None

    def test_valid_metric_with_int_target(self):
        """Test creating metric with integer target."""
        metric = SubMissionBaselineMetric(
            metric_id="corba_references_count",
            description="Count CORBA references",
            baseline_target=0,
            value=None,
        )
        assert metric.metric_id == "corba_references_count"
        assert metric.baseline_target == 0
        assert metric.value is None

    def test_valid_metric_with_float_target(self):
        """Test creating metric with float target."""
        metric = SubMissionBaselineMetric(
            metric_id="test_coverage",
            description="Test coverage percentage",
            baseline_target=85.0,
            value=None,
        )
        assert metric.metric_id == "test_coverage"
        assert metric.baseline_target == 85.0
        assert metric.value is None

    def test_valid_metric_with_string_target(self):
        """Test creating metric with string target."""
        metric = SubMissionBaselineMetric(
            metric_id="api_version",
            description="API version",
            baseline_target="v1.0",
            value=None,
        )
        assert metric.metric_id == "api_version"
        assert metric.baseline_target == "v1.0"
        assert metric.value is None

    def test_metric_with_matching_value_type(self):
        """Test metric with value matching baseline_target type."""
        metric = SubMissionBaselineMetric(
            metric_id="test_coverage",
            description="Test coverage percentage",
            baseline_target=85.0,
            value=78.5,
        )
        assert metric.value == 78.5

    def test_metric_with_mismatched_value_type_bool_int(self):
        """Test metric with value type mismatch (bool vs int)."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaselineMetric(
                metric_id="rest_endpoint_exists",
                description="Check if REST endpoint exists",
                baseline_target=True,
                value=1,  # int instead of bool
            )
        assert "Value type" in str(exc_info.value)

    def test_metric_with_numeric_type_compatibility_int_float(self):
        """Test metric allows int/float interchangeability."""
        # int target, float value - should be allowed
        metric = SubMissionBaselineMetric(
            metric_id="corba_references_count",
            description="Count CORBA references",
            baseline_target=0,
            value=0.0,  # float instead of int - allowed for numeric types
        )
        assert metric.value == 0.0

    def test_metric_with_numeric_type_compatibility_float_int(self):
        """Test metric allows float/int interchangeability."""
        # float target, int value - should be allowed
        metric = SubMissionBaselineMetric(
            metric_id="test_coverage",
            description="Test coverage percentage",
            baseline_target=85.0,
            value=85,  # int instead of float - allowed for numeric types
        )
        assert metric.value == 85

    def test_empty_metric_id_raises_error(self):
        """Test that empty metric_id raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaselineMetric(
                metric_id="",
                description="Test metric",
                baseline_target=True,
                value=None,
            )
        assert "metric_id cannot be empty" in str(exc_info.value)

    def test_whitespace_metric_id_raises_error(self):
        """Test that whitespace-only metric_id raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaselineMetric(
                metric_id="   ",
                description="Test metric",
                baseline_target=True,
                value=None,
            )
        assert "metric_id cannot be empty" in str(exc_info.value)

    def test_empty_description_raises_error(self):
        """Test that empty description raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaselineMetric(
                metric_id="test_metric",
                description="",
                baseline_target=True,
                value=None,
            )
        assert "description cannot be empty" in str(exc_info.value)

    def test_whitespace_description_raises_error(self):
        """Test that whitespace-only description raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaselineMetric(
                metric_id="test_metric",
                description="   ",
                baseline_target=True,
                value=None,
            )
        assert "description cannot be empty" in str(exc_info.value)


class TestSubMissionBaseline:
    """Tests for SubMissionBaseline model."""

    def test_valid_baseline_captured_status(self):
        """Test creating baseline with captured status."""
        baseline = SubMissionBaseline(
            sub_mission_id="MF-001-A",
            timestamp=None,
            status="captured",
            metrics=[
                SubMissionBaselineMetric(
                    metric_id="test_metric",
                    description="Test metric",
                    baseline_target=True,
                    value=None,
                )
            ],
        )
        assert baseline.sub_mission_id == "MF-001-A"
        assert baseline.status == "captured"
        assert baseline.timestamp is None
        assert len(baseline.metrics) == 1

    def test_valid_baseline_committed_status(self):
        """Test creating baseline with committed status."""
        baseline = SubMissionBaseline(
            sub_mission_id="MF-001-A",
            timestamp="2026-05-17T06:00:00Z",
            status="committed",
            metrics=[
                SubMissionBaselineMetric(
                    metric_id="test_metric",
                    description="Test metric",
                    baseline_target=True,
                    value=False,
                )
            ],
        )
        assert baseline.sub_mission_id == "MF-001-A"
        assert baseline.status == "committed"
        assert baseline.timestamp == "2026-05-17T06:00:00Z"

    def test_valid_baseline_no_status(self):
        """Test creating baseline without status."""
        baseline = SubMissionBaseline(
            sub_mission_id="MF-001-A",
            metrics=[
                SubMissionBaselineMetric(
                    metric_id="test_metric",
                    description="Test metric",
                    baseline_target=True,
                    value=None,
                )
            ],
        )
        assert baseline.status is None

    def test_invalid_status_raises_error(self):
        """Test that invalid status raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaseline(
                sub_mission_id="MF-001-A",
                status="invalid",
                metrics=[
                    SubMissionBaselineMetric(
                        metric_id="test_metric",
                        description="Test metric",
                        baseline_target=True,
                        value=None,
                    )
                ],
            )
        assert "Invalid status" in str(exc_info.value)
        assert "captured" in str(exc_info.value)
        assert "committed" in str(exc_info.value)

    def test_invalid_sub_mission_id_format(self):
        """Test that invalid sub-mission ID format raises error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaseline(
                sub_mission_id="INVALID",
                metrics=[
                    SubMissionBaselineMetric(
                        metric_id="test_metric",
                        description="Test metric",
                        baseline_target=True,
                        value=None,
                    )
                ],
            )
        assert "Invalid sub-mission ID format" in str(exc_info.value)

    def test_valid_sub_mission_id_formats(self):
        """Test various valid sub-mission ID formats."""
        valid_ids = ["MF-001-A", "FG-042-Z", "ABCD-999-B"]
        for sub_mission_id in valid_ids:
            baseline = SubMissionBaseline(
                sub_mission_id=sub_mission_id,
                metrics=[
                    SubMissionBaselineMetric(
                        metric_id="test_metric",
                        description="Test metric",
                        baseline_target=True,
                        value=None,
                    )
                ],
            )
            assert baseline.sub_mission_id == sub_mission_id

    def test_invalid_sub_mission_id_formats(self):
        """Test various invalid sub-mission ID formats."""
        invalid_ids = [
            "MF-001",  # Missing suffix
            "MF-001-AB",  # Two-letter suffix
            "M-001-A",  # Single letter prefix
            "MF-1-A",  # Single digit
            "mf-001-a",  # Lowercase
            "MF-001-1",  # Numeric suffix
        ]
        for sub_mission_id in invalid_ids:
            with pytest.raises(ValidationError):
                SubMissionBaseline(
                    sub_mission_id=sub_mission_id,
                    metrics=[
                        SubMissionBaselineMetric(
                            metric_id="test_metric",
                            description="Test metric",
                            baseline_target=True,
                            value=None,
                        )
                    ],
                )

    def test_empty_metrics_list_raises_error(self):
        """Test that empty metrics list raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            SubMissionBaseline(
                sub_mission_id="MF-001-A",
                metrics=[],
            )
        assert "At least one metric must be defined" in str(exc_info.value)

    def test_multiple_metrics(self):
        """Test baseline with multiple metrics."""
        baseline = SubMissionBaseline(
            sub_mission_id="MF-001-A",
            metrics=[
                SubMissionBaselineMetric(
                    metric_id="metric1",
                    description="First metric",
                    baseline_target=True,
                    value=None,
                ),
                SubMissionBaselineMetric(
                    metric_id="metric2",
                    description="Second metric",
                    baseline_target=0,
                    value=None,
                ),
                SubMissionBaselineMetric(
                    metric_id="metric3",
                    description="Third metric",
                    baseline_target=85.0,
                    value=None,
                ),
            ],
        )
        assert len(baseline.metrics) == 3
        assert baseline.metrics[0].metric_id == "metric1"
        assert baseline.metrics[1].metric_id == "metric2"
        assert baseline.metrics[2].metric_id == "metric3"


# Made with Bob