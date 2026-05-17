"""Pytest configuration and fixtures."""

from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from missionforge.cli.app import app
from missionforge.core.workspace import Workspace


@pytest.fixture
def runner() -> CliRunner:
    """Provide Typer CLI test runner.

    Returns:
        CliRunner instance for testing CLI commands.
    """
    return CliRunner()


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary workspace directory.

    Args:
        tmp_path: Pytest temporary directory fixture.

    Yields:
        Path to temporary workspace root.
    """
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()
    yield tmp_path


@pytest.fixture
def workspace(temp_workspace: Path) -> Workspace:
    """Create a Workspace instance in temporary directory.

    Args:
        temp_workspace: Temporary workspace fixture.

    Returns:
        Workspace instance.
    """
    return Workspace(start_path=temp_workspace)


@pytest.fixture
def sample_mission(workspace: Workspace) -> str:
    """Create a sample mission in workspace.

    Args:
        workspace: Workspace fixture.

    Returns:
        Mission ID of created mission.
    """
    mission_id = "MF-001"
    mission_path = workspace.mission_path(mission_id)
    mission_path.mkdir(parents=True, exist_ok=True)
    (mission_path / "sub-missions").mkdir(exist_ok=True)

    # Create mission.yaml
    mission_yaml = mission_path / "mission.yaml"
    mission_yaml.write_text(
        f"""id: {mission_id}
goal: Test mission
forbidden_paths:
  - "core/**"
aggregate_metrics:
  total_files_changed:
    max: 50
test_command: "pytest tests/"
sub_missions: []
"""
    )

    # Create plan.yaml
    plan_yaml = mission_path / "plan.yaml"
    plan_yaml.write_text(
        """execution_order: []
dependency_graph: {}
"""
    )

    return mission_id


@pytest.fixture
def cli_app():
    """Provide CLI app for testing.

    Returns:
        Typer app instance.
    """
    return app


@pytest.fixture(autouse=True)
def reset_workspace_cache():
    """Reset workspace cache between tests."""
    # Import here to avoid circular imports
    from missionforge.cli import app as cli_app_module

    cli_app_module._workspace = None
    cli_app_module._config = None
    yield
    cli_app_module._workspace = None
    cli_app_module._config = None

# Made with Bob
