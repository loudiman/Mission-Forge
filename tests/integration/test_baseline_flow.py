"""Integration tests for baseline capture and commit flow."""

import json
import os
import stat
from pathlib import Path

import pytest

from missionforge.core.baseline_service import BaselineService
from missionforge.core.exceptions import (
    BaselineAlreadyExistsError,
    BaselineIncompleteError,
    BaselineNotCapturedError,
    BaselineValidationError,
)
from missionforge.core.workspace import Workspace


@pytest.fixture
def integration_workspace(tmp_path: Path) -> Workspace:
    """Create a complete workspace for integration testing."""
    # Create workspace structure
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()

    return Workspace(start_path=tmp_path)


@pytest.fixture
def mission_with_sub_mission(integration_workspace: Workspace) -> tuple[str, str]:
    """Create a mission with a sub-mission that has metrics."""
    mission_id = "MF-001"
    sub_mission_id = "MF-001-A"

    # Create mission directory
    mission_path = integration_workspace.mission_path(mission_id)
    mission_path.mkdir(parents=True, exist_ok=True)

    # Create mission.yaml
    mission_yaml = mission_path / "mission.yaml"
    mission_yaml.write_text(f"""id: {mission_id}
goal: Integration test mission
forbidden_paths:
  - "core/**"
aggregate_metrics:
  total_files_changed:
    max: 50
test_command: "pytest tests/"
sub_missions:
  - {sub_mission_id}
""")

    # Create plan.yaml
    plan_yaml = mission_path / "plan.yaml"
    plan_yaml.write_text("""execution_order:
  - MF-001-A
dependency_graph:
  MF-001-A: []
""")

    # Create sub-mission directory
    sub_mission_path = integration_workspace.sub_mission_path(mission_id, sub_mission_id)
    sub_mission_path.mkdir(parents=True, exist_ok=True)

    # Create sub-mission.yaml with metrics (all as floats since MetricDefinition.target is float)
    sub_mission_yaml = sub_mission_path / "sub-mission.yaml"
    sub_mission_yaml.write_text(f"""id: {sub_mission_id}
parent: {mission_id}
title: "Integration Test Sub-Mission"
goal: |
  Test the complete baseline workflow
depends_on: []
allowed_paths:
  - "src/api/**"
  - "tests/api/**"
metrics:
  rest_endpoint_exists:
    target: 0.0
  corba_references_count:
    target: 7.0
  test_coverage:
    target: 78.5
test_command: "pytest tests/api/"
""")

    return mission_id, sub_mission_id


class TestBaselineFlowHappyPath:
    """Test the complete happy path workflow."""

    def test_complete_baseline_workflow(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test complete workflow: capture → fill → commit."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Step 1: Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)

        # Verify baseline.todo.json was created
        assert todo_path.exists()
        assert todo_path.name == "baseline.todo.json"

        # Verify content structure
        with open(todo_path) as f:
            todo_data = json.load(f)

        assert todo_data["sub_mission_id"] == sub_mission_id
        assert todo_data["status"] == "captured"
        assert todo_data["timestamp"] is None
        assert len(todo_data["metrics"]) == 3

        # Verify all values are None (unfilled)
        for metric in todo_data["metrics"]:
            assert metric["value"] is None

        # Step 2: Simulate Bob filling the values (all as floats to match target types)
        todo_data["metrics"][0]["value"] = 0.0  # rest_endpoint_exists
        todo_data["metrics"][1]["value"] = 7.0  # corba_references_count
        todo_data["metrics"][2]["value"] = 78.5  # test_coverage

        with open(todo_path, "w") as f:
            json.dump(todo_data, f, indent=2)

        # Step 3: Commit baseline
        baseline_path = service.commit_baseline(sub_mission_id)

        # Verify baseline.json was created
        assert baseline_path.exists()
        assert baseline_path.name == "baseline.json"

        # Verify content
        with open(baseline_path) as f:
            baseline_data = json.load(f)

        assert baseline_data["sub_mission_id"] == sub_mission_id
        assert baseline_data["status"] == "committed"
        assert baseline_data["timestamp"] is not None
        assert len(baseline_data["metrics"]) == 3

        # Verify all values are filled
        metric_values = {m["metric_id"]: m["value"] for m in baseline_data["metrics"]}
        assert metric_values["rest_endpoint_exists"] == 0.0
        assert metric_values["corba_references_count"] == 7.0
        assert metric_values["test_coverage"] == 78.5

        # Step 4: Verify file is read-only
        file_stat = os.stat(baseline_path)
        mode = file_stat.st_mode
        assert not (mode & stat.S_IWUSR)
        assert not (mode & stat.S_IWGRP)
        assert not (mode & stat.S_IWOTH)

        # Step 5: Verify file is immutable (cannot write)
        with pytest.raises(PermissionError):
            with open(baseline_path, "w") as f:
                f.write("modified")


class TestBaselineFlowErrors:
    """Test error scenarios in the baseline flow."""

    def test_capture_when_baseline_exists(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that capturing when baseline.json exists raises error."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Create existing baseline.json
        baseline_path = integration_workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text('{"sub_mission_id": "MF-001-A"}')

        # Should raise error
        with pytest.raises(BaselineAlreadyExistsError) as exc_info:
            service.capture_baseline(sub_mission_id)

        assert sub_mission_id in str(exc_info.value)

    def test_commit_without_capture(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that committing without capture raises error."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Try to commit without capturing
        with pytest.raises(BaselineNotCapturedError) as exc_info:
            service.commit_baseline(sub_mission_id)

        assert sub_mission_id in str(exc_info.value)

    def test_commit_with_unfilled_values(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that committing with unfilled values raises error."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)

        # Fill only some values
        with open(todo_path) as f:
            todo_data = json.load(f)

        todo_data["metrics"][0]["value"] = 0.0  # Fill first metric
        # Leave other metrics as None

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        # Should raise error
        with pytest.raises(BaselineIncompleteError) as exc_info:
            service.commit_baseline(sub_mission_id)

        error_msg = str(exc_info.value)
        assert "corba_references_count" in error_msg
        assert "test_coverage" in error_msg

    def test_commit_with_wrong_types(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that committing with wrong types raises error."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)

        # Fill with wrong types (string instead of float)
        with open(todo_path) as f:
            todo_data = json.load(f)

        todo_data["metrics"][0]["value"] = "wrong"  # string instead of float
        todo_data["metrics"][1]["value"] = 7.0
        todo_data["metrics"][2]["value"] = 78.5

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        # Should raise validation error
        with pytest.raises(Exception) as exc_info:
            service.commit_baseline(sub_mission_id)

        # Could be ValidationError or BaselineValidationError
        assert "type" in str(exc_info.value).lower()


class TestBaselineFlowReset:
    """Test reset functionality."""

    def test_reset_removes_todo_file(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that reset removes baseline.todo.json."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)
        assert todo_path.exists()

        # Reset
        service.reset_baseline(sub_mission_id)

        # Verify file was removed
        assert not todo_path.exists()

    def test_reset_committed_requires_force(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that reset of committed baseline requires force flag."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture and commit baseline
        todo_path = service.capture_baseline(sub_mission_id)

        with open(todo_path) as f:
            todo_data = json.load(f)

        # Fill all values
        todo_data["metrics"][0]["value"] = 0.0
        todo_data["metrics"][1]["value"] = 7.0
        todo_data["metrics"][2]["value"] = 78.5

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        baseline_path = service.commit_baseline(sub_mission_id)
        assert baseline_path.exists()

        # Try to reset without force
        with pytest.raises(BaselineValidationError) as exc_info:
            service.reset_baseline(sub_mission_id)

        assert "force" in str(exc_info.value).lower()

        # Verify file still exists
        assert baseline_path.exists()

    def test_reset_with_force_removes_committed(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that reset with force removes committed baseline."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture and commit baseline
        todo_path = service.capture_baseline(sub_mission_id)

        with open(todo_path) as f:
            todo_data = json.load(f)

        # Fill all values
        todo_data["metrics"][0]["value"] = 0.0
        todo_data["metrics"][1]["value"] = 7.0
        todo_data["metrics"][2]["value"] = 78.5

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        baseline_path = service.commit_baseline(sub_mission_id)
        assert baseline_path.exists()

        # Reset with force
        service.reset_baseline(sub_mission_id, force=True)

        # Verify both files were removed
        assert not todo_path.exists()
        assert not baseline_path.exists()


class TestBaselineFlowFileStructure:
    """Test that files are created in correct locations."""

    def test_files_created_in_correct_locations(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that baseline files are created in correct directory structure."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)

        # Verify path structure (includes .missionforge)
        expected_dir = (
            integration_workspace.root
            / ".missionforge"
            / "missions"
            / mission_id
            / "sub-missions"
            / sub_mission_id
        )
        assert todo_path.parent == expected_dir
        assert todo_path.name == "baseline.todo.json"

        # Fill and commit
        with open(todo_path) as f:
            todo_data = json.load(f)

        todo_data["metrics"][0]["value"] = 0.0
        todo_data["metrics"][1]["value"] = 7.0
        todo_data["metrics"][2]["value"] = 78.5

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        baseline_path = service.commit_baseline(sub_mission_id)

        # Verify baseline.json is in same directory
        assert baseline_path.parent == expected_dir
        assert baseline_path.name == "baseline.json"


class TestBaselineFlowMetricValidation:
    """Test metric validation during the flow."""

    def test_all_metrics_from_sub_mission_are_captured(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that all metrics from sub-mission.yaml are captured."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)

        with open(todo_path) as f:
            todo_data = json.load(f)

        # Verify all expected metrics are present
        metric_ids = {m["metric_id"] for m in todo_data["metrics"]}
        expected_metrics = {
            "rest_endpoint_exists",
            "corba_references_count",
            "test_coverage",
        }
        assert metric_ids == expected_metrics

    def test_baseline_targets_match_sub_mission_targets(
        self, integration_workspace: Workspace, mission_with_sub_mission: tuple[str, str]
    ):
        """Test that baseline_target values match sub-mission targets."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = BaselineService(integration_workspace)

        # Capture baseline
        todo_path = service.capture_baseline(sub_mission_id)

        with open(todo_path) as f:
            todo_data = json.load(f)

        # Verify baseline_target values (all floats due to MetricDefinition)
        targets = {m["metric_id"]: m["baseline_target"] for m in todo_data["metrics"]}
        assert targets["rest_endpoint_exists"] == 0.0
        assert targets["corba_references_count"] == 7.0
        assert targets["test_coverage"] == 78.5


# Made with Bob
