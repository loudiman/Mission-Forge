"""Unit tests for ParentValidationService."""

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from missionforge.core.exceptions import (
    ParentValidationIncompleteError,
)
from missionforge.core.parent_validation_service import ParentValidationService
from missionforge.core.workspace import Workspace
from missionforge.models.schemas import (
    AggregateMetricResult,
    ForbiddenPathsCheck,
    ParentTestResult,
    SubMissionsAggregate,
    SubMissionSummary,
)


@pytest.fixture
def mock_workspace(tmp_path: Path) -> Workspace:
    """Create a mock workspace."""
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()
    return Workspace(start_path=tmp_path)


@pytest.fixture
def parent_mission_setup(mock_workspace: Workspace):
    """Setup parent mission with sub-missions."""
    mission_id = "MF-001"
    mission_path = mock_workspace.mission_path(mission_id)
    mission_path.mkdir(parents=True, exist_ok=True)

    # Create mission.yaml
    (mission_path / "mission.yaml").write_text(
        f"""id: {mission_id}
goal: Test parent mission
forbidden_paths:
  - "core/**"
sub_missions:
  - MF-001-A
  - MF-001-B
"""
    )

    # Create sub-mission directories and validation.json files
    for sub_id in ["MF-001-A", "MF-001-B"]:
        sub_path = mock_workspace.sub_mission_path(mission_id, sub_id)
        sub_path.mkdir(parents=True, exist_ok=True)

        validation_data = {
            "sub_mission_id": sub_id,
            "timestamp": "2026-05-16T17:00:00Z",
            "status": "PASSED",
            "deterministic_evidence": {
                "files_changed": ["src/api/test.py"],
                "scope_check": {
                    "allowed_paths_satisfied": True,
                    "forbidden_paths_violated": False,
                    "violations": [],
                },
                "test_results": None,
            },
            "metrics": [],
        }

        validation_path = mock_workspace.validation_path(sub_id)
        with open(validation_path, "w") as f:
            json.dump(validation_data, f)

    return mock_workspace, mission_id


class TestAggregateSubMissions:
    """Test sub-mission aggregation logic."""

    def test_aggregate_all_passed(self, parent_mission_setup):
        """Test aggregation when all sub-missions passed."""
        workspace, mission_id = parent_mission_setup
        service = ParentValidationService(workspace)

        result = service._aggregate_sub_missions(mission_id, ["MF-001-A", "MF-001-B"])

        assert result.total == 2
        assert result.passed == 2
        assert result.failed == 0
        assert result.blocked == 0
        assert len(result.details) == 2

    def test_aggregate_with_failures(self, parent_mission_setup):
        """Test aggregation with mixed statuses."""
        workspace, mission_id = parent_mission_setup
        service = ParentValidationService(workspace)

        # Modify one sub-mission to FAILED
        validation_path = workspace.validation_path("MF-001-B")
        with open(validation_path) as f:
            data = json.load(f)
        data["status"] = "FAILED"
        with open(validation_path, "w") as f:
            json.dump(data, f)

        result = service._aggregate_sub_missions(mission_id, ["MF-001-A", "MF-001-B"])

        assert result.total == 2
        assert result.passed == 1
        assert result.failed == 1
        assert result.blocked == 0

    def test_aggregate_missing_validation(self, parent_mission_setup):
        """Test error when validation.json missing."""
        workspace, mission_id = parent_mission_setup
        service = ParentValidationService(workspace)

        # Remove one validation.json
        validation_path = workspace.validation_path("MF-001-B")
        validation_path.unlink()

        with pytest.raises(ParentValidationIncompleteError) as exc_info:
            service._aggregate_sub_missions(mission_id, ["MF-001-A", "MF-001-B"])

        assert "MF-001-B" in str(exc_info.value)


class TestDetermineParentStatus:
    """Test status determination logic."""

    def test_status_passed_all_checks(self, mock_workspace):
        """Test status when all checks pass."""
        service = ParentValidationService(mock_workspace)

        sub_missions = SubMissionsAggregate(
            total=2,
            passed=2,
            failed=0,
            blocked=0,
            details=[
                SubMissionSummary(id="MF-001-A", status="PASSED", timestamp=None),
                SubMissionSummary(id="MF-001-B", status="PASSED", timestamp=None),
            ],
        )

        parent_test = ParentTestResult(
            command="pytest", exit_code=0, output="All tests passed", passed=True, duration=1.5
        )

        aggregate_metrics = [
            AggregateMetricResult(
                metric_id="test_metric",
                baseline_value=None,
                target_value=100,
                final_value=100,
                status="PASSED",
            )
        ]

        forbidden_check = ForbiddenPathsCheck(violated=False, violations=[])

        status = service._determine_parent_status(
            sub_missions, parent_test, aggregate_metrics, forbidden_check
        )

        assert status == "PASSED"

    def test_status_failed_sub_mission(self, mock_workspace):
        """Test status when sub-mission failed."""
        service = ParentValidationService(mock_workspace)

        sub_missions = SubMissionsAggregate(
            total=2,
            passed=1,
            failed=1,
            blocked=0,
            details=[
                SubMissionSummary(id="MF-001-A", status="PASSED", timestamp=None),
                SubMissionSummary(id="MF-001-B", status="FAILED", timestamp=None),
            ],
        )

        status = service._determine_parent_status(
            sub_missions, None, [], ForbiddenPathsCheck(violated=False, violations=[])
        )

        assert status == "FAILED"

    def test_status_failed_parent_test(self, mock_workspace):
        """Test status when parent test failed."""
        service = ParentValidationService(mock_workspace)

        sub_missions = SubMissionsAggregate(
            total=2,
            passed=2,
            failed=0,
            blocked=0,
            details=[
                SubMissionSummary(id="MF-001-A", status="PASSED", timestamp=None),
                SubMissionSummary(id="MF-001-B", status="PASSED", timestamp=None),
            ],
        )

        parent_test = ParentTestResult(
            command="pytest", exit_code=1, output="Tests failed", passed=False, duration=1.5
        )

        status = service._determine_parent_status(
            sub_missions, parent_test, [], ForbiddenPathsCheck(violated=False, violations=[])
        )

        assert status == "FAILED"

    def test_status_failed_aggregate_metric(self, mock_workspace):
        """Test status when aggregate metric failed."""
        service = ParentValidationService(mock_workspace)

        sub_missions = SubMissionsAggregate(
            total=2,
            passed=2,
            failed=0,
            blocked=0,
            details=[
                SubMissionSummary(id="MF-001-A", status="PASSED", timestamp=None),
                SubMissionSummary(id="MF-001-B", status="PASSED", timestamp=None),
            ],
        )

        aggregate_metrics = [
            AggregateMetricResult(
                metric_id="test_metric",
                baseline_value=None,
                target_value=100,
                final_value=50,
                status="FAILED",
            )
        ]

        status = service._determine_parent_status(
            sub_missions,
            None,
            aggregate_metrics,
            ForbiddenPathsCheck(violated=False, violations=[]),
        )

        assert status == "FAILED"

    def test_status_failed_forbidden_paths(self, mock_workspace):
        """Test status when forbidden paths violated."""
        service = ParentValidationService(mock_workspace)

        sub_missions = SubMissionsAggregate(
            total=2,
            passed=2,
            failed=0,
            blocked=0,
            details=[
                SubMissionSummary(id="MF-001-A", status="PASSED", timestamp=None),
                SubMissionSummary(id="MF-001-B", status="PASSED", timestamp=None),
            ],
        )

        forbidden_check = ForbiddenPathsCheck(violated=True, violations=["core/important.py"])

        status = service._determine_parent_status(sub_missions, None, [], forbidden_check)

        assert status == "FAILED"


class TestCheckForbiddenPaths:
    """Test forbidden paths checking."""

    def test_no_violations(self, parent_mission_setup):
        """Test forbidden paths check with no violations."""
        workspace, mission_id = parent_mission_setup
        service = ParentValidationService(workspace)

        result = service._check_forbidden_paths(mission_id, ["MF-001-A", "MF-001-B"], ["core/**"])

        assert not result.violated
        assert len(result.violations) == 0

    def test_with_violations(self, parent_mission_setup):
        """Test forbidden paths check with violations."""
        workspace, mission_id = parent_mission_setup
        service = ParentValidationService(workspace)

        # Modify sub-mission to have forbidden file
        validation_path = workspace.validation_path("MF-001-A")
        with open(validation_path) as f:
            data = json.load(f)
        data["deterministic_evidence"]["files_changed"] = ["core/important.py"]
        with open(validation_path, "w") as f:
            json.dump(data, f)

        result = service._check_forbidden_paths(mission_id, ["MF-001-A", "MF-001-B"], ["core/**"])

        assert result.violated
        assert "core/important.py" in result.violations

    def test_empty_forbidden_paths(self, parent_mission_setup):
        """Test with no forbidden paths defined."""
        workspace, mission_id = parent_mission_setup
        service = ParentValidationService(workspace)

        result = service._check_forbidden_paths(mission_id, ["MF-001-A", "MF-001-B"], [])

        assert not result.violated
        assert len(result.violations) == 0


class TestExecuteParentTest:
    """Test parent test execution."""

    def test_execute_test_success(self, mock_workspace: Workspace):
        """Test successful test execution."""
        service = ParentValidationService(mock_workspace)

        mock_result = Mock()
        mock_result.exit_code = 0
        mock_result.stdout = "All tests passed"
        mock_result.stderr = ""
        mock_result.success = True
        mock_result.duration = 1.5

        with patch(
            "missionforge.core.parent_validation_service.execute_test_command",
            return_value=mock_result,
        ):
            result = service._execute_parent_test("pytest", mock_workspace.root)

        assert result.passed
        assert result.exit_code == 0
        assert result.duration == 1.5

    def test_execute_test_failure(self, mock_workspace: Workspace):
        """Test failed test execution."""
        service = ParentValidationService(mock_workspace)

        mock_result = Mock()
        mock_result.exit_code = 1
        mock_result.stdout = ""
        mock_result.stderr = "Tests failed"
        mock_result.success = False
        mock_result.duration = 2.0

        with patch(
            "missionforge.core.parent_validation_service.execute_test_command",
            return_value=mock_result,
        ):
            result = service._execute_parent_test("pytest", mock_workspace.root)

        assert not result.passed
        assert result.exit_code == 1
        assert "Tests failed" in result.output


# Made with Bob
