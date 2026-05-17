"""Unit tests for mission validation."""

import pytest
import yaml

from missionforge.core.mission_validator import MissionValidator


@pytest.fixture
def validator():
    """Create validator instance."""
    return MissionValidator()


@pytest.fixture
def valid_mission_data():
    """Create valid mission data."""
    return {
        "id": "MF-001",
        "goal": "Test mission goal that is long enough",
        "forbidden_paths": ["core/**", "config/**"],
        "aggregate_metrics": {"total_files_changed": {"max": 50}},
        "test_command": "pytest tests/",
        "sub_missions": [],
    }


def test_validate_valid_mission(validator, valid_mission_data, tmp_path):
    """Test validation of valid mission."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert is_valid
    assert len(errors) == 0


def test_validate_missing_required_field(validator, valid_mission_data, tmp_path):
    """Test validation fails for missing required field."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Remove required field
    del valid_mission_data["goal"]

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert len(errors) > 0


def test_validate_missing_test_command(validator, valid_mission_data, tmp_path):
    """Test validation fails when test_command is missing."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    del valid_mission_data["test_command"]

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("test_command" in err for err in errors)


def test_validate_whitespace_only_test_command(validator, valid_mission_data, tmp_path):
    """Test validation fails when test_command is whitespace-only.

    Pydantic accepts any non-None string for required fields, so a value like
    '   ' passes schema validation. MissionValidator must catch it explicitly.
    """
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    valid_mission_data["test_command"] = "   "

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("test_command" in err for err in errors)


def test_validate_invalid_mission_id_format(validator, valid_mission_data, tmp_path):
    """Test validation fails for invalid mission ID format."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Set invalid mission ID
    valid_mission_data["id"] = "invalid-id"

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert len(errors) > 0


def test_validate_empty_forbidden_paths(validator, valid_mission_data, tmp_path):
    """Test validation succeeds with empty forbidden_paths."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Empty forbidden_paths is valid
    valid_mission_data["forbidden_paths"] = []

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert is_valid
    assert len(errors) == 0


def test_validate_mission_id_mismatch(validator, valid_mission_data, tmp_path):
    """Test validation fails when mission ID doesn't match directory."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Set different mission ID
    valid_mission_data["id"] = "MF-002"

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("does not match directory" in err for err in errors)


def test_validate_metric_without_constraint(validator, valid_mission_data, tmp_path):
    """Test validation fails for metric without constraint."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Add metric without constraint
    valid_mission_data["aggregate_metrics"]["bad_metric"] = {"description": "No constraint"}

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("min, max, or target" in err.lower() for err in errors)


def test_validate_metric_not_object(validator, valid_mission_data, tmp_path):
    """Test validation fails for metric that is not an object."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Add metric that is not an object
    valid_mission_data["aggregate_metrics"]["bad_metric"] = "not an object"

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("valid dictionary" in err.lower() for err in errors)


def test_validate_missing_file(validator, tmp_path):
    """Test validation fails for missing file."""
    mission_file = tmp_path / "MF-001" / "mission.yaml"

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("not found" in err for err in errors)


def test_validate_invalid_yaml_syntax(validator, tmp_path):
    """Test validation fails for invalid YAML syntax."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Write invalid YAML
    mission_file.write_text("invalid: yaml: syntax:")

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("yaml" in err.lower() for err in errors)


def test_validate_empty_goal(validator, valid_mission_data, tmp_path):
    """Test validation fails for an empty goal."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    valid_mission_data["goal"] = "   "

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert len(errors) > 0


def test_validate_with_allowed_paths(validator, valid_mission_data, tmp_path):
    """Test validation succeeds with valid allowed_paths."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Add allowed_paths
    valid_mission_data["allowed_paths"] = ["src/**", "tests/**"]

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert is_valid
    assert len(errors) == 0


def test_validate_complex_glob_patterns(validator, valid_mission_data, tmp_path):
    """Test validation succeeds with complex glob patterns."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    # Add complex but valid glob patterns
    valid_mission_data["allowed_paths"] = ["src/**/*.py", "tests/**/test_*.py", "!**/__pycache__/**"]

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert is_valid
    assert len(errors) == 0


def test_validate_invalid_glob_pattern(validator, valid_mission_data, tmp_path):
    """Test validation fails for malformed glob patterns."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    mission_file = mission_dir / "mission.yaml"

    valid_mission_data["forbidden_paths"] = ["src/[invalid"]

    with open(mission_file, "w") as f:
        yaml.dump(valid_mission_data, f)

    is_valid, errors = validator.validate_file(mission_file)
    assert not is_valid
    assert any("path pattern" in err.lower() for err in errors)


# Made with Bob
