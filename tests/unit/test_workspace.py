"""Unit tests for workspace module."""

from pathlib import Path

import pytest

from missionforge.core.exceptions import WorkspaceNotFoundError
from missionforge.core.workspace import Workspace


def test_workspace_finds_root(temp_workspace: Path):
    """Test workspace root discovery from subdirectory."""
    # Create nested subdirectory
    subdir = temp_workspace / "src" / "app"
    subdir.mkdir(parents=True)

    # Should find workspace from subdirectory
    ws = Workspace(start_path=subdir)
    assert ws.root == temp_workspace
    assert ws.workspace_dir == temp_workspace / ".missionforge"
    assert ws.missions_dir == temp_workspace / ".missionforge" / "missions"


def test_workspace_not_found_raises_error(tmp_path: Path):
    """Test error when workspace not found."""
    with pytest.raises(WorkspaceNotFoundError) as exc_info:
        Workspace(start_path=tmp_path)

    assert "No .missionforge workspace found" in str(exc_info.value)
    assert "missionforge workspace init" in exc_info.value.suggestion


def test_workspace_exists(workspace: Workspace):
    """Test workspace existence check."""
    assert workspace.exists()


def test_workspace_not_exists(tmp_path: Path):
    """Test workspace existence check when not initialized."""
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    # Create workspace but delete it
    ws = Workspace(start_path=tmp_path)
    workspace_dir.rmdir()

    assert not ws.exists()


def test_mission_path(workspace: Workspace):
    """Test mission path resolution."""
    mission_id = "MF-001"
    expected = workspace.missions_dir / mission_id

    assert workspace.mission_path(mission_id) == expected


def test_sub_mission_path(workspace: Workspace):
    """Test sub-mission path resolution."""
    mission_id = "MF-001"
    sub_mission_id = "MF-001-A"
    expected = workspace.missions_dir / mission_id / "sub-missions" / sub_mission_id

    assert workspace.sub_mission_path(mission_id, sub_mission_id) == expected


def test_initialize_workspace(tmp_path: Path):
    """Test workspace initialization."""
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()

    ws = Workspace(start_path=tmp_path)
    ws.initialize()

    assert ws.missions_dir.exists()
    assert ws.missions_dir.is_dir()


def test_list_missions_empty(workspace: Workspace):
    """Test listing missions when none exist."""
    missions = workspace.list_missions()
    assert missions == []


def test_list_missions(workspace: Workspace, sample_mission: str):
    """Test listing missions."""
    missions = workspace.list_missions()
    assert sample_mission in missions
    assert len(missions) == 1


def test_list_missions_multiple(workspace: Workspace):
    """Test listing multiple missions."""
    # Create multiple missions
    for i in range(1, 4):
        mission_id = f"MF-00{i}"
        mission_path = workspace.mission_path(mission_id)
        mission_path.mkdir(parents=True)
        (mission_path / "mission.yaml").write_text(f"id: {mission_id}\n")

    missions = workspace.list_missions()
    assert len(missions) == 3
    assert "MF-001" in missions
    assert "MF-002" in missions
    assert "MF-003" in missions
    # Should be sorted
    assert missions == ["MF-001", "MF-002", "MF-003"]


def test_list_missions_ignores_directories_without_yaml(workspace: Workspace):
    """Test that directories without mission.yaml are ignored."""
    # Create directory without mission.yaml
    invalid_mission = workspace.mission_path("INVALID-001")
    invalid_mission.mkdir(parents=True)

    missions = workspace.list_missions()
    assert "INVALID-001" not in missions

# Made with Bob
