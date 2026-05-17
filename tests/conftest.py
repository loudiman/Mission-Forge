"""Shared pytest fixtures and configuration."""

import subprocess
from collections.abc import Generator
from pathlib import Path

import pytest
from typer.testing import CliRunner

from missionforge.cli.app import app
from missionforge.core.workspace import Workspace


@pytest.fixture
def runner() -> CliRunner:
    """Provide Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary workspace directory."""
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()
    yield tmp_path


@pytest.fixture
def workspace(temp_workspace: Path) -> Workspace:
    """Create a Workspace instance in temporary directory."""
    return Workspace(start_path=temp_workspace)


@pytest.fixture
def sample_mission(workspace: Workspace) -> str:
    """Create a sample mission in workspace."""
    mission_id = "MF-001"
    mission_path = workspace.mission_path(mission_id)
    mission_path.mkdir(parents=True, exist_ok=True)
    (mission_path / "sub-missions").mkdir(exist_ok=True)

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

    plan_yaml = mission_path / "plan.yaml"
    plan_yaml.write_text(
        """execution_order: []
dependency_graph: {}
"""
    )

    return mission_id


@pytest.fixture
def cli_app():
    """Provide CLI app for testing."""
    return app


@pytest.fixture(autouse=True)
def reset_workspace_cache():
    """Reset workspace cache between tests."""
    from missionforge.cli import app as cli_app_module

    cli_app_module._workspace = None
    cli_app_module._config = None
    yield
    cli_app_module._workspace = None
    cli_app_module._config = None


@pytest.fixture
def git_repo(tmp_path: Path) -> Path:
    """Create a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_path,
        check=True,
        capture_output=True,
    )

    return repo_path


@pytest.fixture
def git_repo_with_commit(git_repo: Path) -> Path:
    """Create a git repository with an initial commit."""
    test_file = git_repo / "initial.txt"
    test_file.write_text("initial content")

    subprocess.run(["git", "add", "initial.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )

    return git_repo


# Made with Bob
