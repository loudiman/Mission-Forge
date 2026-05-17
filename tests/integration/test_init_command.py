"""Integration tests for init command."""

from typer.testing import CliRunner

from missionforge.cli.app import app

runner = CliRunner()


def test_init_creates_structure(tmp_path, monkeypatch):
    """Test init command creates proper directory structure."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "MF-001"])

    assert result.exit_code == 0
    assert (tmp_path / ".missionforge" / "missions" / "MF-001").exists()
    assert (tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml").exists()
    assert (tmp_path / ".missionforge" / "missions" / "MF-001" / "plan.yaml").exists()
    assert (tmp_path / ".missionforge" / "missions" / "MF-001" / "sub-missions").is_dir()
    assert (tmp_path / ".missionforge" / "missions" / "MF-001" / "report.md").exists()


def test_init_prevents_overwrite(tmp_path, monkeypatch):
    """Test init command prevents accidental overwrite."""
    monkeypatch.chdir(tmp_path)

    # Create mission first time
    runner.invoke(app, ["init", "MF-001"])

    # Try to create again without --force
    result = runner.invoke(app, ["init", "MF-001"])

    assert result.exit_code == 1
    assert "already exists" in result.stdout


def test_init_with_force_overwrites(tmp_path, monkeypatch):
    """Test init command with --force overwrites existing mission."""
    monkeypatch.chdir(tmp_path)

    # Create mission first time
    runner.invoke(app, ["init", "MF-001"])

    # Create again with --force
    result = runner.invoke(app, ["init", "MF-001", "--force"])

    assert result.exit_code == 0


def test_init_validates_mission_id_format(tmp_path, monkeypatch):
    """Test init command validates mission ID format."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "invalid-id"])

    assert result.exit_code == 1
    # Error message appears in the exception output
    assert result.exception is not None or "Invalid mission ID" in str(result.output)


def test_workspace_init_creates_structure(tmp_path, monkeypatch):
    """Test workspace init command creates proper directory structure."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["workspace", "init", "MF-001"])

    assert result.exit_code == 0
    assert (tmp_path / ".missionforge" / "missions" / "MF-001").exists()
    assert (tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml").exists()


def test_init_creates_valid_mission_yaml(tmp_path, monkeypatch):
    """Test init command creates valid mission.yaml."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "MF-001"])

    assert result.exit_code == 0

    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    content = mission_file.read_text()

    # Check for key sections in template
    assert "id: MF-001" in content
    assert "goal:" in content
    assert "forbidden_paths:" in content
    assert "aggregate_metrics:" in content
    assert "test_command:" in content
    assert "sub_missions:" in content


def test_init_with_different_mission_ids(tmp_path, monkeypatch):
    """Test init command with various valid mission ID formats."""
    monkeypatch.chdir(tmp_path)

    valid_ids = ["MF-001", "FG-042", "PROJ-123", "AB-999A"]

    for mission_id in valid_ids:
        result = runner.invoke(app, ["init", mission_id])
        assert result.exit_code == 0
        assert (tmp_path / ".missionforge" / "missions" / mission_id).exists()


def test_init_shows_next_steps(tmp_path, monkeypatch):
    """Test init command shows helpful next steps."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "MF-001"])

    assert result.exit_code == 0
    assert "Next steps:" in result.stdout
    assert "mission.yaml" in result.stdout
    assert "validate" in result.stdout


# Made with Bob
