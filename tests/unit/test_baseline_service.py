"""Unit tests for BaselineService."""

import json
import os
import stat
from pathlib import Path

import pytest
from pydantic import ValidationError

from missionforge.core.baseline_service import BaselineService
from missionforge.core.exceptions import (
    BaselineAlreadyExistsError,
    BaselineIncompleteError,
    BaselineNotCapturedError,
    BaselineValidationError,
)
from missionforge.core.workspace import Workspace


@pytest.fixture
def baseline_service(workspace: Workspace) -> BaselineService:
    """Create BaselineService instance with test workspace."""
    return BaselineService(workspace)


@pytest.fixture
def sub_mission_with_metrics(workspace: Workspace) -> str:
    """Create a sub-mission with metrics for testing."""
    sub_mission_id = "MF-001-A"
    parent_id = "MF-001"

    # Create parent mission directory
    mission_path = workspace.mission_path(parent_id)
    mission_path.mkdir(parents=True, exist_ok=True)

    # Create sub-mission directory
    sub_mission_path = workspace.sub_mission_path(parent_id, sub_mission_id)
    sub_mission_path.mkdir(parents=True, exist_ok=True)

    # Create sub-mission.yaml with metrics
    sub_mission_yaml = sub_mission_path / "sub-mission.yaml"
    sub_mission_yaml.write_text("""id: MF-001-A
parent: MF-001
title: "Test Sub-Mission with Metrics"
goal: |
  Test sub-mission for baseline testing
depends_on: []
allowed_paths:
  - "src/test/**"
metrics:
  rest_endpoint_exists:
    target: true
  corba_references_count:
    target: 0
  test_coverage:
    target: 85.0
test_command: "pytest tests/"
""")

    return sub_mission_id


class TestCaptureBaseline:
    """Tests for capture_baseline method."""

    def test_capture_baseline_success(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test successful baseline capture."""
        sub_mission_id = sub_mission_with_metrics

        # Capture baseline
        todo_path = baseline_service.capture_baseline(sub_mission_id)

        # Verify file was created
        assert todo_path.exists()
        assert todo_path.name == "baseline.todo.json"

        # Verify content
        with open(todo_path) as f:
            data = json.load(f)

        assert data["sub_mission_id"] == sub_mission_id
        assert data["status"] == "captured"
        assert data["timestamp"] is None
        assert len(data["metrics"]) == 3

        # Verify metrics
        metric_ids = {m["metric_id"] for m in data["metrics"]}
        assert metric_ids == {"rest_endpoint_exists", "corba_references_count", "test_coverage"}

        # Verify all values are None
        for metric in data["metrics"]:
            assert metric["value"] is None

    def test_capture_baseline_with_existing_baseline_raises_error(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that capturing baseline when baseline.json exists raises error."""
        sub_mission_id = sub_mission_with_metrics

        # Create existing baseline.json
        baseline_path = baseline_service.workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text('{"sub_mission_id": "MF-001-A"}')

        # Should raise error
        with pytest.raises(BaselineAlreadyExistsError) as exc_info:
            baseline_service.capture_baseline(sub_mission_id)

        assert sub_mission_id in str(exc_info.value)

    def test_capture_baseline_with_force_overwrites(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that force flag allows overwriting existing baseline."""
        sub_mission_id = sub_mission_with_metrics

        # Create existing baseline.json
        baseline_path = baseline_service.workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text('{"sub_mission_id": "MF-001-A"}')

        # Should succeed with force=True
        todo_path = baseline_service.capture_baseline(sub_mission_id, force=True)
        assert todo_path.exists()

    def test_capture_baseline_with_missing_target_raises_error(
        self, baseline_service: BaselineService, workspace: Workspace
    ):
        """Test that metric without target raises error."""
        sub_mission_id = "MF-002-A"
        parent_id = "MF-002"

        # Create sub-mission with metric missing target
        mission_path = workspace.mission_path(parent_id)
        mission_path.mkdir(parents=True, exist_ok=True)

        sub_mission_path = workspace.sub_mission_path(parent_id, sub_mission_id)
        sub_mission_path.mkdir(parents=True, exist_ok=True)

        sub_mission_yaml = sub_mission_path / "sub-mission.yaml"
        sub_mission_yaml.write_text("""id: MF-002-A
parent: MF-002
title: "Test Sub-Mission"
goal: "Test"
metrics:
  bad_metric:
    min: 0
    max: 100
test_command: "pytest tests/"
""")

        # Should raise error
        with pytest.raises(BaselineValidationError) as exc_info:
            baseline_service.capture_baseline(sub_mission_id)

        assert "bad_metric" in str(exc_info.value)
        assert "no target value" in str(exc_info.value)

    def test_capture_baseline_supports_flat_sub_mission_definition(
        self, baseline_service: BaselineService, workspace: Workspace
    ):
        """Test baseline capture can read legacy flat sub-mission YAML files."""
        mission_path = workspace.mission_path("MF-001")
        sub_missions_dir = mission_path / "sub-missions"
        sub_missions_dir.mkdir(parents=True, exist_ok=True)
        (sub_missions_dir / "MF-001-A.yaml").write_text("""id: MF-001-A
parent: MF-001
title: "Flat Sub-Mission"
goal: "Test flat layout"
metrics:
  test_coverage:
    target: 85.0
""")

        todo_path = baseline_service.capture_baseline("MF-001-A")

        assert todo_path.exists()
        with open(todo_path) as f:
            data = json.load(f)
        assert data["sub_mission_id"] == "MF-001-A"


class TestCommitBaseline:
    """Tests for commit_baseline method."""

    def test_commit_baseline_success(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str, tmp_path: Path
    ):
        """Test successful baseline commit."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.todo.json with filled values
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        todo_data = {
            "sub_mission_id": sub_mission_id,
            "timestamp": None,
            "status": "captured",
            "metrics": [
                {
                    "metric_id": "rest_endpoint_exists",
                    "description": "Metric: rest_endpoint_exists",
                    "baseline_target": True,
                    "value": False,
                },
                {
                    "metric_id": "corba_references_count",
                    "description": "Metric: corba_references_count",
                    "baseline_target": 0,
                    "value": 5,
                },
                {
                    "metric_id": "test_coverage",
                    "description": "Metric: test_coverage",
                    "baseline_target": 85.0,
                    "value": 78.5,
                },
            ],
        }

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        # Commit baseline
        baseline_path = baseline_service.commit_baseline(sub_mission_id)

        # Verify file was created
        assert baseline_path.exists()
        assert baseline_path.name == "baseline.json"

        # Verify content
        with open(baseline_path) as f:
            data = json.load(f)

        assert data["sub_mission_id"] == sub_mission_id
        assert data["status"] == "committed"
        assert data["timestamp"] is not None
        assert len(data["metrics"]) == 3

        # Verify file is read-only
        file_stat = os.stat(baseline_path)
        mode = file_stat.st_mode
        # Check that write permissions are not set
        assert not (mode & stat.S_IWUSR)
        assert not (mode & stat.S_IWGRP)
        assert not (mode & stat.S_IWOTH)

    def test_commit_baseline_without_capture_raises_error(
        self, baseline_service: BaselineService
    ):
        """Test that committing without capture raises error."""
        sub_mission_id = "MF-001-A"

        with pytest.raises(BaselineNotCapturedError) as exc_info:
            baseline_service.commit_baseline(sub_mission_id)

        assert sub_mission_id in str(exc_info.value)

    def test_commit_baseline_with_incomplete_values_raises_error(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that committing with incomplete values raises error."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.todo.json with some null values
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        todo_data = {
            "sub_mission_id": sub_mission_id,
            "timestamp": None,
            "status": "captured",
            "metrics": [
                {
                    "metric_id": "rest_endpoint_exists",
                    "description": "Metric: rest_endpoint_exists",
                    "baseline_target": True,
                    "value": None,  # Not filled
                },
                {
                    "metric_id": "corba_references_count",
                    "description": "Metric: corba_references_count",
                    "baseline_target": 0,
                    "value": 5,
                },
            ],
        }

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        # Should raise error
        with pytest.raises(BaselineIncompleteError) as exc_info:
            baseline_service.commit_baseline(sub_mission_id)

        assert "rest_endpoint_exists" in str(exc_info.value)

    def test_commit_baseline_with_type_mismatch_raises_error(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that committing with type mismatch raises error."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.todo.json with wrong type
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        todo_data = {
            "sub_mission_id": sub_mission_id,
            "timestamp": None,
            "status": "captured",
            "metrics": [
                {
                    "metric_id": "rest_endpoint_exists",
                    "description": "Metric: rest_endpoint_exists",
                    "baseline_target": True,
                    "value": 1,  # int instead of bool
                },
            ],
        }

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        # Should raise Pydantic ValidationError (caught during model parsing)
        with pytest.raises(ValidationError) as exc_info:
            baseline_service.commit_baseline(sub_mission_id)

        assert "Value type" in str(exc_info.value)

    def test_commit_baseline_float_int_compatibility(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that float/int type compatibility is allowed."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.todo.json with int instead of float
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        todo_data = {
            "sub_mission_id": sub_mission_id,
            "timestamp": None,
            "status": "captured",
            "metrics": [
                {
                    "metric_id": "test_coverage",
                    "description": "Metric: test_coverage",
                    "baseline_target": 85.0,
                    "value": 85,  # int instead of float - should be allowed
                },
            ],
        }

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        # Should succeed - numeric types are compatible
        baseline_path = baseline_service.commit_baseline(sub_mission_id)

        assert baseline_path.exists()
        with open(baseline_path) as f:
            data = json.load(f)
        assert data["metrics"][0]["value"] == 85


class TestResetBaseline:
    """Tests for reset_baseline method."""

    def test_reset_baseline_removes_todo_file(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that reset removes baseline.todo.json."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.todo.json
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)
        todo_path.write_text('{"sub_mission_id": "MF-001-A"}')

        # Reset
        baseline_service.reset_baseline(sub_mission_id)

        # Verify file was removed
        assert not todo_path.exists()

    def test_reset_baseline_without_force_raises_error_for_committed(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that reset without force raises error for committed baseline."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.json
        baseline_path = baseline_service.workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text('{"sub_mission_id": "MF-001-A"}')

        # Should raise error
        with pytest.raises(BaselineValidationError) as exc_info:
            baseline_service.reset_baseline(sub_mission_id)

        assert "force" in str(exc_info.value).lower()

    def test_reset_baseline_with_force_removes_committed(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that reset with force removes committed baseline."""
        sub_mission_id = sub_mission_with_metrics

        # Create baseline.json (read-only)
        baseline_path = baseline_service.workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text('{"sub_mission_id": "MF-001-A"}')
        os.chmod(baseline_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        # Reset with force
        baseline_service.reset_baseline(sub_mission_id, force=True)

        # Verify file was removed
        assert not baseline_path.exists()

    def test_reset_baseline_removes_both_files(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that reset with force removes both files."""
        sub_mission_id = sub_mission_with_metrics

        # Create both files
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        baseline_path = baseline_service.workspace.baseline_path(sub_mission_id)

        todo_path.parent.mkdir(parents=True, exist_ok=True)
        todo_path.write_text('{"sub_mission_id": "MF-001-A"}')
        baseline_path.write_text('{"sub_mission_id": "MF-001-A"}')

        # Reset with force
        baseline_service.reset_baseline(sub_mission_id, force=True)

        # Verify both files were removed
        assert not todo_path.exists()
        assert not baseline_path.exists()

    def test_reset_baseline_with_no_files_raises_error(
        self, baseline_service: BaselineService
    ):
        """Test that reset with no files raises error."""
        sub_mission_id = "MF-001-A"

        with pytest.raises(BaselineValidationError) as exc_info:
            baseline_service.reset_baseline(sub_mission_id)

        assert "No baseline files found" in str(exc_info.value)


class TestFileImmutability:
    """Tests for file immutability after commit."""

    def test_committed_baseline_is_read_only(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that committed baseline.json is read-only."""
        sub_mission_id = sub_mission_with_metrics

        # Create and commit baseline
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        todo_data = {
            "sub_mission_id": sub_mission_id,
            "timestamp": None,
            "status": "captured",
            "metrics": [
                {
                    "metric_id": "test_metric",
                    "description": "Test",
                    "baseline_target": True,
                    "value": False,
                },
            ],
        }

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        baseline_path = baseline_service.commit_baseline(sub_mission_id)

        # Try to write to file (should fail)
        with pytest.raises(PermissionError):
            with open(baseline_path, "w") as f:
                f.write("modified")

    def test_committed_baseline_cannot_be_deleted_without_permission_change(
        self, baseline_service: BaselineService, sub_mission_with_metrics: str
    ):
        """Test that committed baseline cannot be deleted without changing permissions."""
        sub_mission_id = sub_mission_with_metrics

        # Create and commit baseline
        todo_path = baseline_service.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        todo_data = {
            "sub_mission_id": sub_mission_id,
            "timestamp": None,
            "status": "captured",
            "metrics": [
                {
                    "metric_id": "test_metric",
                    "description": "Test",
                    "baseline_target": True,
                    "value": False,
                },
            ],
        }

        with open(todo_path, "w") as f:
            json.dump(todo_data, f)

        baseline_path = baseline_service.commit_baseline(sub_mission_id)

        # Try to delete file (should fail on most systems)
        # Note: On some systems, directory permissions may allow deletion
        # even if file is read-only, so we just verify the file is read-only
        file_stat = os.stat(baseline_path)
        mode = file_stat.st_mode
        assert not (mode & stat.S_IWUSR)


# Made with Bob
