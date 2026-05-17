"""Integration tests for validate command."""

import yaml
from typer.testing import CliRunner

from missionforge.cli.app import app

runner = CliRunner()


def test_validate_valid_mission(tmp_path, monkeypatch):
    """Test validate command succeeds for valid mission."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Validate
    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 0
    assert "valid" in result.stdout.lower()


def test_validate_valid_mission_with_issue_command_shape(tmp_path, monkeypatch):
    """Test issue-specified validate command succeeds for valid mission."""
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["init", "MF-001"])

    result = runner.invoke(app, ["mission", "MF-001", "--validate"])

    assert result.exit_code == 0
    assert "valid" in result.stdout.lower()


def test_validate_missing_mission(tmp_path, monkeypatch):
    """Test validate command fails for missing mission."""
    monkeypatch.chdir(tmp_path)

    # Create workspace but not mission
    (tmp_path / ".missionforge").mkdir()

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1
    assert "not found" in result.stdout.lower()


def test_validate_invalid_yaml(tmp_path, monkeypatch):
    """Test validate command fails for invalid YAML."""
    monkeypatch.chdir(tmp_path)

    # Create mission with invalid YAML
    mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
    mission_dir.mkdir(parents=True)
    mission_file = mission_dir / "mission.yaml"
    mission_file.write_text("invalid: yaml: syntax:")

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1
    assert "yaml" in result.stdout.lower()


def test_validate_missing_required_field(tmp_path, monkeypatch):
    """Test validate command fails for missing required field."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Modify mission.yaml to remove required field
    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    with open(mission_file) as f:
        data = yaml.safe_load(f)

    del data["goal"]

    with open(mission_file, "w") as f:
        yaml.dump(data, f)

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1
    assert "validation failed" in result.stdout.lower()


def test_validate_invalid_mission_id(tmp_path, monkeypatch):
    """Test validate command fails for invalid mission ID format."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Modify mission.yaml to have invalid ID
    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    with open(mission_file) as f:
        data = yaml.safe_load(f)

    data["id"] = "invalid-id"

    with open(mission_file, "w") as f:
        yaml.dump(data, f)

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1


def test_validate_mission_id_mismatch(tmp_path, monkeypatch):
    """Test validate command fails when mission ID doesn't match directory."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Modify mission.yaml to have different ID
    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    with open(mission_file) as f:
        data = yaml.safe_load(f)

    data["id"] = "MF-002"

    with open(mission_file, "w") as f:
        yaml.dump(data, f)

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1
    assert "does not match" in result.stdout.lower()


def test_validate_complex_glob_patterns(tmp_path, monkeypatch):
    """Test validate command succeeds with complex glob patterns."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Modify mission.yaml to have complex glob patterns
    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    with open(mission_file) as f:
        data = yaml.safe_load(f)

    data["forbidden_paths"] = ["src/**/*.py", "!src/tests/**"]

    with open(mission_file, "w") as f:
        yaml.dump(data, f)

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 0
    assert "valid" in result.stdout.lower()


def test_validate_invalid_glob_pattern(tmp_path, monkeypatch):
    """Test validate command fails for malformed glob patterns."""
    monkeypatch.chdir(tmp_path)

    runner.invoke(app, ["init", "MF-001"])

    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    with open(mission_file) as f:
        data = yaml.safe_load(f)

    data["forbidden_paths"] = ["src/[invalid"]

    with open(mission_file, "w") as f:
        yaml.dump(data, f)

    result = runner.invoke(app, ["mission", "MF-001", "--validate"])

    assert result.exit_code == 1
    assert "path pattern" in result.stdout.lower()


def test_validate_metric_without_constraint(tmp_path, monkeypatch):
    """Test validate command fails for metric without constraint."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Modify mission.yaml to have metric without constraint
    mission_file = tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
    with open(mission_file) as f:
        data = yaml.safe_load(f)

    data["aggregate_metrics"]["bad_metric"] = {"description": "No constraint"}

    with open(mission_file, "w") as f:
        yaml.dump(data, f)

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1
    assert "min, max" in result.stdout.lower()
    assert "target" in result.stdout.lower()


def test_validate_shows_next_steps(tmp_path, monkeypatch):
    """Test validate command shows next steps on success."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Validate
    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 0
    assert "Next steps:" in result.stdout
    assert "decompose" in result.stdout.lower()


def test_validate_shows_file_path_on_error(tmp_path, monkeypatch):
    """Test validate command shows file path when errors occur."""
    monkeypatch.chdir(tmp_path)

    # Create mission with invalid YAML
    mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
    mission_dir.mkdir(parents=True)
    mission_file = mission_dir / "mission.yaml"
    mission_file.write_text("invalid: yaml: syntax:")

    result = runner.invoke(app, ["mission", "validate", "MF-001"])

    assert result.exit_code == 1
    assert "mission.yaml" in result.stdout


def test_validate_with_flag_syntax(tmp_path, monkeypatch):
    """Test validate command works with --validate flag syntax."""
    monkeypatch.chdir(tmp_path)

    # Create mission
    runner.invoke(app, ["init", "MF-001"])

    # Validate using --validate flag (as specified in GitHub issue)
    result = runner.invoke(app, ["mission", "MF-001", "--validate"])

    assert result.exit_code == 0
    assert "valid" in result.stdout.lower()


def test_mission_no_args_shows_usage(tmp_path, monkeypatch):
    """Test mission command with no args exits with error and shows usage hint."""
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["mission"])

    assert result.exit_code == 1
    assert "no mission action specified" in result.stdout.lower()


# Made with Bob
