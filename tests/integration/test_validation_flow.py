"""Integration tests for sub-mission validation capture and commit flow."""

import json
import os
import stat
from pathlib import Path
from unittest.mock import patch

import pytest

from missionforge.core.exceptions import (
    ValidationAlreadyExistsError,
    ValidationIncompleteError,
    ValidationNotCapturedError,
)
from missionforge.core.validation_service import ValidationService
from missionforge.core.workspace import Workspace


@pytest.fixture
def integration_workspace(tmp_path: Path) -> Workspace:
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()
    return Workspace(start_path=tmp_path)


@pytest.fixture
def mission_with_sub_mission(integration_workspace: Workspace) -> tuple[str, str]:
    mission_id = "MF-001"
    sub_mission_id = "MF-001-A"

    mission_path = integration_workspace.mission_path(mission_id)
    mission_path.mkdir(parents=True, exist_ok=True)

    (mission_path / "mission.yaml").write_text(
        f"""id: {mission_id}
goal: Integration test mission
forbidden_paths:
  - "core/**"
aggregate_metrics:
  total_files_changed:
    max: 50
sub_missions:
  - {sub_mission_id}
"""
    )

    (mission_path / "plan.yaml").write_text(
        """execution_order:
  - MF-001-A
dependency_graph:
  MF-001-A: []
"""
    )

    sub_mission_path = integration_workspace.sub_mission_path(mission_id, sub_mission_id)
    sub_mission_path.mkdir(parents=True, exist_ok=True)

    (sub_mission_path / "sub-mission.yaml").write_text(
        f"""id: {sub_mission_id}
parent: {mission_id}
title: "Integration Test Sub-Mission"
goal: Test validation workflow
depends_on: []
allowed_paths:
  - "src/api/**"
metrics:
  endpoint_exists:
    target: 1.0
  test_coverage:
    target: 80.0
"""
    )

    return mission_id, sub_mission_id


@pytest.fixture
def mission_with_baseline(
    integration_workspace: Workspace,
    mission_with_sub_mission: tuple[str, str],
) -> tuple[str, str]:
    """Create a mission with baseline.json already committed."""
    mission_id, sub_mission_id = mission_with_sub_mission
    baseline_path = integration_workspace.baseline_path(sub_mission_id)
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    baseline_data = {
        "sub_mission_id": sub_mission_id,
        "timestamp": "2026-05-01T00:00:00+00:00",
        "status": "committed",
        "metrics": [
            {"metric_id": "endpoint_exists", "description": "...", "baseline_target": 0.0, "value": 0.0},
            {"metric_id": "test_coverage", "description": "...", "baseline_target": 50.0, "value": 50.0},
        ],
    }
    with open(baseline_path, "w") as f:
        json.dump(baseline_data, f)
    return mission_id, sub_mission_id


def _no_git_changes(cwd=None):
    """Helper to patch git calls to return no changes."""

    from missionforge.git.operations import GitStatus
    return GitStatus(staged=[], unstaged=[], untracked=[], deleted=[], renamed={})


class TestValidationCaptureHappyPath:
    def test_capture_creates_todo_json(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        assert todo_path.exists()
        assert todo_path.name == "validation.todo.json"

    def test_capture_content_structure(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        assert data["sub_mission_id"] == sub_mission_id
        assert data["status"] == "captured"
        assert data["timestamp"] is None
        assert "deterministic_evidence" in data
        assert "metrics" in data
        assert len(data["metrics"]) == 2

    def test_capture_metrics_have_none_final_value(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        for metric in data["metrics"]:
            assert metric["final_value"] is None
            assert metric["status"] is None

    def test_capture_includes_baseline_values(
        self,
        integration_workspace: Workspace,
        mission_with_baseline: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_baseline
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        by_id = {m["metric_id"]: m for m in data["metrics"]}
        assert by_id["endpoint_exists"]["baseline_value"] == 0.0
        assert by_id["test_coverage"]["baseline_value"] == 50.0

    def test_capture_scope_check_populated(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        scope = data["deterministic_evidence"]["scope_check"]
        assert "allowed_paths_satisfied" in scope
        assert "forbidden_paths_violated" in scope
        assert "violations" in scope


class TestValidationCaptureErrors:
    def test_capture_fails_if_validation_exists(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        validation_path = integration_workspace.validation_path(sub_mission_id)
        validation_path.parent.mkdir(parents=True, exist_ok=True)
        validation_path.write_text("{}")

        with pytest.raises(ValidationAlreadyExistsError):
            service.capture_validation(sub_mission_id)

    def test_capture_force_overwrites(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        validation_path = integration_workspace.validation_path(sub_mission_id)
        validation_path.parent.mkdir(parents=True, exist_ok=True)
        validation_path.write_text("{}")

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id, force=True)

        assert todo_path.exists()


class TestValidationCommitHappyPath:
    def _capture_and_fill(
        self,
        service: ValidationService,
        workspace: Workspace,
        sub_mission_id: str,
        final_values: dict[str, object],
    ) -> Path:
        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        for metric in data["metrics"]:
            if metric["metric_id"] in final_values:
                metric["final_value"] = final_values[metric["metric_id"]]

        with open(todo_path, "w") as f:
            json.dump(data, f)

        return todo_path

    def test_commit_creates_validation_json(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        self._capture_and_fill(
            service, integration_workspace, sub_mission_id,
            {"endpoint_exists": 1.0, "test_coverage": 85.0},
        )
        out_path = service.commit_validation(sub_mission_id)

        assert out_path.exists()
        assert out_path.name == "validation.json"

    def test_commit_status_passed(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        self._capture_and_fill(
            service, integration_workspace, sub_mission_id,
            {"endpoint_exists": 1.0, "test_coverage": 85.0},
        )
        out_path = service.commit_validation(sub_mission_id)

        with open(out_path) as f:
            data = json.load(f)

        assert data["status"] == "PASSED"
        assert data["timestamp"] is not None

    def test_commit_status_failed_when_metric_misses(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        # endpoint_exists target is 1.0, provide 0.0 → FAILED
        self._capture_and_fill(
            service, integration_workspace, sub_mission_id,
            {"endpoint_exists": 0.0, "test_coverage": 85.0},
        )
        out_path = service.commit_validation(sub_mission_id)

        with open(out_path) as f:
            data = json.load(f)

        assert data["status"] == "FAILED"
        by_id = {m["metric_id"]: m for m in data["metrics"]}
        assert by_id["endpoint_exists"]["status"] == "FAILED"
        assert by_id["test_coverage"]["status"] == "PASSED"

    def test_commit_file_is_immutable(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        self._capture_and_fill(
            service, integration_workspace, sub_mission_id,
            {"endpoint_exists": 1.0, "test_coverage": 85.0},
        )
        out_path = service.commit_validation(sub_mission_id)

        mode = os.stat(out_path).st_mode
        assert not (mode & stat.S_IWUSR)
        assert not (mode & stat.S_IWGRP)
        assert not (mode & stat.S_IWOTH)

        with pytest.raises(PermissionError):
            with open(out_path, "w") as f:
                f.write("tampered")

    def test_commit_contains_timestamp(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        self._capture_and_fill(
            service, integration_workspace, sub_mission_id,
            {"endpoint_exists": 1.0, "test_coverage": 80.0},
        )
        out_path = service.commit_validation(sub_mission_id)

        with open(out_path) as f:
            data = json.load(f)

        assert data["timestamp"] is not None
        assert "2026" in data["timestamp"] or "T" in data["timestamp"]


class TestValidationCommitErrors:
    def test_commit_without_capture_raises(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with pytest.raises(ValidationNotCapturedError):
            service.commit_validation(sub_mission_id)

    def test_commit_with_unfilled_metrics_raises(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                service.capture_validation(sub_mission_id)

        with pytest.raises(ValidationIncompleteError) as exc_info:
            service.commit_validation(sub_mission_id)

        assert sub_mission_id in str(exc_info.value)


class TestValidationScopeAndBlocked:
    def _patch_git_with_files(self, files: list[Path]):
        """Return context managers patching git to return specific staged files."""
        from pathlib import Path as _Path

        from missionforge.git.operations import GitStatus
        git_status = GitStatus(staged=files, unstaged=[], untracked=[], deleted=[], renamed={})
        return (
            patch("missionforge.core.validation_service.get_repo_root", return_value=_Path(".")),
            patch("missionforge.core.validation_service.get_status", return_value=git_status),
            patch("missionforge.core.validation_service.get_changed_files", return_value=[]),
        )

    def test_blocked_when_forbidden_file_changed(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        """Files matching forbidden_paths trigger BLOCKED status."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        p1, p2, p3 = self._patch_git_with_files([Path("core/important.py")])
        with p1, p2, p3:
            todo_path = service.capture_validation(sub_mission_id)

        # Fill metrics
        with open(todo_path) as f:
            data = json.load(f)
        for m in data["metrics"]:
            m["final_value"] = 1.0
        with open(todo_path, "w") as f:
            json.dump(data, f)

        out_path = service.commit_validation(sub_mission_id)

        with open(out_path) as f:
            committed = json.load(f)

        assert committed["status"] == "BLOCKED"

    def test_violations_captured_in_scope_check(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        """Scope violations are recorded in deterministic evidence."""
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        p1, p2, p3 = self._patch_git_with_files([Path("core/important.py")])
        with p1, p2, p3:
            todo_path = service.capture_validation(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        scope = data["deterministic_evidence"]["scope_check"]
        assert scope["violations"]


class TestValidationFileLocations:
    def test_files_in_correct_directory(
        self,
        integration_workspace: Workspace,
        mission_with_sub_mission: tuple[str, str],
    ):
        mission_id, sub_mission_id = mission_with_sub_mission
        service = ValidationService(integration_workspace)

        with patch("missionforge.core.validation_service.get_status", return_value=_no_git_changes()):
            with patch("missionforge.core.validation_service.get_changed_files", return_value=[]):
                todo_path = service.capture_validation(sub_mission_id)

        expected_dir = (
            integration_workspace.root
            / ".missionforge"
            / "missions"
            / mission_id
            / "sub-missions"
            / sub_mission_id
        )
        assert todo_path.parent == expected_dir
        assert todo_path.name == "validation.todo.json"


# Made with Bob
