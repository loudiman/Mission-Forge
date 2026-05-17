"""Integration tests for CLI commands."""

from pathlib import Path

from typer.testing import CliRunner

from missionforge.cli.app import app


def test_version_command(runner: CliRunner):
    """Test version command."""
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "MissionForge" in result.stdout
    assert "v0.1.0" in result.stdout


def test_workspace_init_command(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace init command."""
    # Change to temp directory
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["workspace", "init", "MF-001"])

    assert result.exit_code == 0
    assert "Initialized mission MF-001" in result.stdout

    # Verify directory structure
    workspace_dir = tmp_path / ".missionforge"
    assert workspace_dir.exists()
    assert (workspace_dir / "missions" / "MF-001").exists()
    assert (workspace_dir / "missions" / "MF-001" / "mission.yaml").exists()
    assert (workspace_dir / "missions" / "MF-001" / "plan.yaml").exists()
    assert (workspace_dir / "missions" / "MF-001" / "sub-missions").exists()


def test_workspace_init_invalid_mission_id(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace init with invalid mission ID."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["workspace", "init", "invalid-id"])

    assert result.exit_code == 1
    # Error is in stdout or exception message
    assert "Invalid mission ID" in (result.stdout + str(result.exception))


def test_workspace_init_existing_mission(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace init with existing mission."""
    monkeypatch.chdir(tmp_path)

    # Create mission first time
    result1 = runner.invoke(app, ["workspace", "init", "MF-001"])
    assert result1.exit_code == 0

    # Try to create again without force
    result2 = runner.invoke(app, ["workspace", "init", "MF-001"])
    assert result2.exit_code == 1
    assert "already exists" in result2.stdout


def test_workspace_init_with_force(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace init with force flag."""
    monkeypatch.chdir(tmp_path)

    # Create mission first time
    result1 = runner.invoke(app, ["workspace", "init", "MF-001"])
    assert result1.exit_code == 0

    # Create again with force
    result2 = runner.invoke(app, ["workspace", "init", "MF-001", "--force"])
    assert result2.exit_code == 0
    assert "Initialized mission MF-001" in result2.stdout


def test_workspace_status_no_workspace(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace status when no workspace exists."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["workspace", "status"])

    assert result.exit_code == 1
    assert "No workspace initialized" in result.stdout


def test_workspace_status_empty(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace status with no missions."""
    monkeypatch.chdir(tmp_path)

    # Create workspace structure
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    (workspace_dir / "missions").mkdir()

    result = runner.invoke(app, ["workspace", "status"])

    assert result.exit_code == 0
    assert "No missions found" in result.stdout


def test_workspace_status_with_missions(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test workspace status with missions."""
    monkeypatch.chdir(tmp_path)

    # Create missions
    runner.invoke(app, ["workspace", "init", "MF-001"])
    runner.invoke(app, ["workspace", "init", "MF-002"])

    result = runner.invoke(app, ["workspace", "status"])

    assert result.exit_code == 0
    assert "MF-001" in result.stdout
    assert "MF-002" in result.stdout
    assert "Missions" in result.stdout


def test_cli_verbose_flag(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test CLI with verbose flag."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["--verbose", "version"])

    assert result.exit_code == 0
    assert "MissionForge" in result.stdout


def test_cli_help(runner: CliRunner):
    """Test CLI help output."""
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "mission" in result.stdout.lower()  # Check for mission-related text
    assert "workspace" in result.stdout


def test_workspace_init_creates_valid_yaml(runner: CliRunner, tmp_path: Path, monkeypatch):
    """Test that workspace init creates valid YAML files."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["workspace", "init", "TEST-123"])
    assert result.exit_code == 0

    # Read and verify mission.yaml
    mission_yaml = tmp_path / ".missionforge" / "missions" / "TEST-123" / "mission.yaml"
    content = mission_yaml.read_text()

    assert "id: TEST-123" in content
    assert "goal:" in content
    assert "forbidden_paths:" in content
    assert "aggregate_metrics:" in content
    assert "test_command:" in content


def test_workspace_status_shows_sub_mission_count(
    runner: CliRunner, tmp_path: Path, monkeypatch
):
    """Test that workspace status shows sub-mission count."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["workspace", "init", "MF-001"])

    # Create sub-missions
    sub_missions_dir = (
        tmp_path / ".missionforge" / "missions" / "MF-001" / "sub-missions"
    )
    (sub_missions_dir / "MF-001-A.yaml").write_text("id: MF-001-A\n")
    (sub_missions_dir / "MF-001-B.yaml").write_text("id: MF-001-B\n")

    result = runner.invoke(app, ["workspace", "status"])

    assert result.exit_code == 0
    assert "MF-001" in result.stdout
    assert "2" in result.stdout  # Should show 2 sub-missions

# Made with Bob
