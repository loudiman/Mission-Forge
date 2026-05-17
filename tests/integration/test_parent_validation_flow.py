"""Integration tests for parent mission validation flow."""

import json
import os
import stat
from pathlib import Path

import pytest

from missionforge.core.exceptions import (
    ParentValidationFailedError,
    ParentValidationIncompleteError,
)
from missionforge.core.parent_validation_service import ParentValidationService
from missionforge.core.workspace import Workspace


@pytest.fixture
def integration_workspace(tmp_path: Path) -> Workspace:
    """Create integration test workspace."""
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()
    return Workspace(start_path=tmp_path)


@pytest.fixture
def complete_parent_mission(integration_workspace: Workspace):
    """Setup complete parent mission with all sub-missions validated."""
    mission_id = "MF-001"
    mission_path = integration_workspace.mission_path(mission_id)
    mission_path.mkdir(parents=True, exist_ok=True)

    # Create mission.yaml
    (mission_path / "mission.yaml").write_text(
        f"""id: {mission_id}
goal: Integration test parent mission
forbidden_paths:
  - "core/**"
sub_missions:
  - MF-001-A
  - MF-001-B
  - MF-001-C
"""
    )

    # Create sub-missions with validation.json
    for sub_id in ["MF-001-A", "MF-001-B", "MF-001-C"]:
        sub_path = integration_workspace.sub_mission_path(mission_id, sub_id)
        sub_path.mkdir(parents=True, exist_ok=True)

        # Create sub-mission.yaml
        (sub_path / "sub-mission.yaml").write_text(
            f"""id: {sub_id}
parent: {mission_id}
title: "Test Sub-Mission"
goal: Test validation workflow
depends_on: []
allowed_paths:
  - "src/api/**"
metrics:
  test_metric:
    target: 100.0
"""
        )

        # Create validation.json
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
                "test_results": {
                    "command": "pytest",
                    "exit_code": 0,
                    "output": "All tests passed",
                    "passed": True,
                    "duration": 1.5,
                },
            },
            "metrics": [
                {
                    "metric_id": "test_metric",
                    "baseline_value": 50.0,
                    "target_value": 100.0,
                    "final_value": 100.0,
                    "status": "PASSED",
                }
            ],
        }

        validation_path = integration_workspace.validation_path(sub_id)
        with open(validation_path, "w") as f:
            json.dump(validation_data, f)

    return integration_workspace, mission_id


class TestParentValidationHappyPath:
    """Test successful parent validation flow."""

    def test_validate_parent_all_passed(self, complete_parent_mission):
        """Test parent validation when all sub-missions passed."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        validation_path = service.validate_parent_mission(mission_id)

        assert validation_path.exists()
        assert validation_path.name == "validation.json"

        with open(validation_path) as f:
            data = json.load(f)

        assert data["mission_id"] == mission_id
        assert data["status"] == "PASSED"
        assert data["sub_missions"]["total"] == 3
        assert data["sub_missions"]["passed"] == 3
        assert data["sub_missions"]["failed"] == 0
        assert data["sub_missions"]["blocked"] == 0

    def test_validation_file_is_immutable(self, complete_parent_mission):
        """Test that validation.json is read-only."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        validation_path = service.validate_parent_mission(mission_id)

        mode = os.stat(validation_path).st_mode
        assert not (mode & stat.S_IWUSR)
        assert not (mode & stat.S_IWGRP)
        assert not (mode & stat.S_IWOTH)

        with pytest.raises(PermissionError):
            with open(validation_path, "w") as f:
                f.write("tampered")

    def test_validation_contains_timestamp(self, complete_parent_mission):
        """Test that validation contains timestamp."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        validation_path = service.validate_parent_mission(mission_id)

        with open(validation_path) as f:
            data = json.load(f)

        assert data["timestamp"] is not None
        assert "2026" in data["timestamp"] or "T" in data["timestamp"]

    def test_validation_includes_sub_mission_details(self, complete_parent_mission):
        """Test that validation includes all sub-mission details."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        validation_path = service.validate_parent_mission(mission_id)

        with open(validation_path) as f:
            data = json.load(f)

        details = data["sub_missions"]["details"]
        assert len(details) == 3

        sub_ids = {d["id"] for d in details}
        assert sub_ids == {"MF-001-A", "MF-001-B", "MF-001-C"}

        for detail in details:
            assert detail["status"] == "PASSED"
            assert detail["timestamp"] is not None


class TestParentValidationErrors:
    """Test error cases in parent validation."""

    def test_missing_sub_mission_validation(self, complete_parent_mission):
        """Test error when sub-mission validation.json missing."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        # Remove one validation.json
        validation_path = workspace.validation_path("MF-001-B")
        validation_path.unlink()

        with pytest.raises(ParentValidationIncompleteError) as exc_info:
            service.validate_parent_mission(mission_id)

        assert "MF-001-B" in str(exc_info.value)

    def test_sub_mission_failed(self, complete_parent_mission):
        """Test error when sub-mission has FAILED status."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        # Modify one sub-mission to FAILED
        validation_path = workspace.validation_path("MF-001-B")
        with open(validation_path) as f:
            data = json.load(f)
        data["status"] = "FAILED"
        with open(validation_path, "w") as f:
            json.dump(data, f)

        with pytest.raises(ParentValidationFailedError) as exc_info:
            service.validate_parent_mission(mission_id)

        assert "FAILED" in str(exc_info.value)

    def test_sub_mission_blocked(self, complete_parent_mission):
        """Test error when sub-mission has BLOCKED status."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        # Modify one sub-mission to BLOCKED
        validation_path = workspace.validation_path("MF-001-C")
        with open(validation_path) as f:
            data = json.load(f)
        data["status"] = "BLOCKED"
        with open(validation_path, "w") as f:
            json.dump(data, f)

        with pytest.raises(ParentValidationFailedError) as exc_info:
            service.validate_parent_mission(mission_id)

        assert "BLOCKED" in str(exc_info.value)


class TestForbiddenPathsValidation:
    """Test forbidden paths checking across sub-missions."""

    def test_forbidden_paths_violation(self, complete_parent_mission):
        """Test error when forbidden paths violated."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        # Modify one sub-mission to have forbidden file
        validation_path = workspace.validation_path("MF-001-A")
        with open(validation_path) as f:
            data = json.load(f)
        data["deterministic_evidence"]["files_changed"] = ["core/important.py"]
        with open(validation_path, "w") as f:
            json.dump(data, f)

        with pytest.raises(ParentValidationFailedError) as exc_info:
            service.validate_parent_mission(mission_id)

        assert "Forbidden paths" in str(exc_info.value)

    def test_no_forbidden_paths_defined(self, complete_parent_mission):
        """Test validation succeeds when no forbidden paths defined."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        # Modify mission to have no forbidden paths
        mission_path = workspace.mission_path(mission_id)
        (mission_path / "mission.yaml").write_text(
            f"""id: {mission_id}
goal: Integration test parent mission
sub_missions:
  - MF-001-A
  - MF-001-B
  - MF-001-C
"""
        )

        validation_path = service.validate_parent_mission(mission_id)

        with open(validation_path) as f:
            data = json.load(f)

        assert not data["forbidden_paths_check"]["violated"]
        assert len(data["forbidden_paths_check"]["violations"]) == 0


class TestParentTestExecution:
    """Test parent test command execution."""

    def test_parent_test_not_defined(self, complete_parent_mission):
        """Test validation succeeds when no parent test defined."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        validation_path = service.validate_parent_mission(mission_id)

        with open(validation_path) as f:
            data = json.load(f)

        assert data["parent_test"] is None
        assert data["status"] == "PASSED"


class TestValidationFileLocation:
    """Test validation file is created in correct location."""

    def test_validation_in_mission_directory(self, complete_parent_mission):
        """Test validation.json is in mission directory."""
        workspace, mission_id = complete_parent_mission
        service = ParentValidationService(workspace)

        validation_path = service.validate_parent_mission(mission_id)

        expected_dir = workspace.mission_path(mission_id)
        assert validation_path.parent == expected_dir
        assert validation_path.name == "validation.json"


# Made with Bob
