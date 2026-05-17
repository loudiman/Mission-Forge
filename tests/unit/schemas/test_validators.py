"""Tests for schema validators."""

import json

import pytest
import yaml

from missionforge.core.exceptions import ValidationError as MFValidationError
from missionforge.models.schemas import (
    Baseline,
    ExecutionPlan,
    ParentMission,
    SubMission,
    Validation,
)
from missionforge.schemas.validators import SchemaValidator


@pytest.fixture
def tmp_mission_dir(tmp_path):
    """Create temporary mission directory structure."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()
    (mission_dir / "sub-missions").mkdir()
    return mission_dir


@pytest.fixture
def valid_parent_mission_data():
    """Valid parent mission data."""
    return {
        "id": "MF-001",
        "goal": "Test mission goal",
        "forbidden_paths": ["core/**"],
        "aggregate_metrics": {"total_files": {"max": 50}},
        "test_command": "pytest",
        "sub_missions": ["MF-001-A"],
    }


@pytest.fixture
def valid_sub_mission_data():
    """Valid sub-mission data."""
    return {
        "id": "MF-001-A",
        "parent": "MF-001",
        "title": "Test sub-mission",
        "goal": "Test goal",
        "depends_on": [],
        "allowed_paths": ["src/**"],
        "metrics": {"files_changed": {"max": 10}},
        "test_command": "pytest tests/",
    }


@pytest.fixture
def valid_baseline_data():
    """Valid baseline data."""
    return {
        "mission_id": "MF-001",
        "timestamp": "2024-01-01T00:00:00Z",
        "git_commit": "abc123def456",
        "metrics": {
            "files_changed": 0,
            "lines_added": 0,
            "lines_removed": 0,
            "test_coverage": 85.0,
            "custom_metrics": {},
        },
    }


@pytest.fixture
def valid_validation_data():
    """Valid validation data."""
    return {
        "mission_id": "MF-001",
        "timestamp": "2024-01-01T00:00:00Z",
        "git_commit": "abc123def456",
        "metrics": {
            "files_changed": 5,
            "lines_added": 100,
            "lines_removed": 50,
            "test_coverage": 90.0,
            "tests_passed": True,
            "custom_metrics": {},
        },
        "passed": True,
        "errors": [],
    }


@pytest.fixture
def valid_plan_data():
    """Valid execution plan data."""
    return {
        "execution_order": ["MF-001-A", "MF-001-B"],
        "dependency_graph": {"MF-001-A": [], "MF-001-B": ["MF-001-A"]},
    }


class TestValidateParentMissionFile:
    """Tests for validate_parent_mission_file."""

    def test_valid_mission_file(self, tmp_path, valid_parent_mission_data):
        """Test validating valid mission file."""
        mission_file = tmp_path / "mission.yaml"
        with open(mission_file, "w") as f:
            yaml.dump(valid_parent_mission_data, f)

        mission = SchemaValidator.validate_parent_mission_file(mission_file)
        assert isinstance(mission, ParentMission)
        assert mission.id == "MF-001"
        assert mission.goal == "Test mission goal"

    def test_missing_file(self, tmp_path):
        """Test error when file doesn't exist."""
        mission_file = tmp_path / "missing.yaml"
        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_parent_mission_file(mission_file)
        assert "not found" in str(exc_info.value).lower()

    def test_empty_file(self, tmp_path):
        """Test error with empty file."""
        mission_file = tmp_path / "mission.yaml"
        mission_file.write_text("")

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_parent_mission_file(mission_file)
        assert "empty" in str(exc_info.value).lower()

    def test_invalid_yaml_syntax(self, tmp_path):
        """Test error with invalid YAML syntax."""
        mission_file = tmp_path / "mission.yaml"
        mission_file.write_text("invalid: yaml: syntax:")

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_parent_mission_file(mission_file)
        assert "yaml syntax" in str(exc_info.value).lower()

    def test_invalid_mission_id(self, tmp_path, valid_parent_mission_data):
        """Test error with invalid mission ID."""
        valid_parent_mission_data["id"] = "invalid-id"
        mission_file = tmp_path / "mission.yaml"
        with open(mission_file, "w") as f:
            yaml.dump(valid_parent_mission_data, f)

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_parent_mission_file(mission_file)
        assert "validation failed" in str(exc_info.value).lower()

    def test_missing_required_field(self, tmp_path, valid_parent_mission_data):
        """Test error with missing required field."""
        del valid_parent_mission_data["goal"]
        mission_file = tmp_path / "mission.yaml"
        with open(mission_file, "w") as f:
            yaml.dump(valid_parent_mission_data, f)

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_parent_mission_file(mission_file)
        assert "validation failed" in str(exc_info.value).lower()


class TestValidateSubMissionFile:
    """Tests for validate_sub_mission_file."""

    def test_valid_sub_mission_file(self, tmp_path, valid_sub_mission_data):
        """Test validating valid sub-mission file."""
        sub_file = tmp_path / "MF-001-A.yaml"
        with open(sub_file, "w") as f:
            yaml.dump(valid_sub_mission_data, f)

        sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
        assert isinstance(sub_mission, SubMission)
        assert sub_mission.id == "MF-001-A"
        assert sub_mission.parent == "MF-001"

    def test_missing_file(self, tmp_path):
        """Test error when file doesn't exist."""
        sub_file = tmp_path / "missing.yaml"
        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_sub_mission_file(sub_file)
        assert "not found" in str(exc_info.value).lower()

    def test_parent_mismatch(self, tmp_path, valid_sub_mission_data):
        """Test error with parent-child ID mismatch."""
        valid_sub_mission_data["parent"] = "MF-002"  # Wrong parent
        sub_file = tmp_path / "MF-001-A.yaml"
        with open(sub_file, "w") as f:
            yaml.dump(valid_sub_mission_data, f)

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_sub_mission_file(sub_file)
        assert "validation failed" in str(exc_info.value).lower()


class TestValidateBaselineFile:
    """Tests for validate_baseline_file."""

    def test_valid_baseline_file(self, tmp_path, valid_baseline_data):
        """Test validating valid baseline file."""
        baseline_file = tmp_path / "baseline.json"
        with open(baseline_file, "w") as f:
            json.dump(valid_baseline_data, f)

        baseline = SchemaValidator.validate_baseline_file(baseline_file)
        assert isinstance(baseline, Baseline)
        assert baseline.mission_id == "MF-001"

    def test_missing_file(self, tmp_path):
        """Test error when file doesn't exist."""
        baseline_file = tmp_path / "missing.json"
        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_baseline_file(baseline_file)
        assert "not found" in str(exc_info.value).lower()

    def test_invalid_json_syntax(self, tmp_path):
        """Test error with invalid JSON syntax."""
        baseline_file = tmp_path / "baseline.json"
        baseline_file.write_text("{invalid json")

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_baseline_file(baseline_file)
        assert "json syntax" in str(exc_info.value).lower()


class TestValidateValidationFile:
    """Tests for validate_validation_file."""

    def test_valid_validation_file(self, tmp_path, valid_validation_data):
        """Test validating valid validation file."""
        validation_file = tmp_path / "validation.json"
        with open(validation_file, "w") as f:
            json.dump(valid_validation_data, f)

        validation = SchemaValidator.validate_validation_file(validation_file)
        assert isinstance(validation, Validation)
        assert validation.mission_id == "MF-001"
        assert validation.passed is True

    def test_missing_file(self, tmp_path):
        """Test error when file doesn't exist."""
        validation_file = tmp_path / "missing.json"
        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_validation_file(validation_file)
        assert "not found" in str(exc_info.value).lower()


class TestValidatePlanFile:
    """Tests for validate_plan_file."""

    def test_valid_plan_file(self, tmp_path, valid_plan_data):
        """Test validating valid plan file."""
        plan_file = tmp_path / "plan.yaml"
        with open(plan_file, "w") as f:
            yaml.dump(valid_plan_data, f)

        plan = SchemaValidator.validate_plan_file(plan_file)
        assert isinstance(plan, ExecutionPlan)
        assert len(plan.execution_order) == 2

    def test_missing_file(self, tmp_path):
        """Test error when file doesn't exist."""
        plan_file = tmp_path / "missing.yaml"
        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_plan_file(plan_file)
        assert "not found" in str(exc_info.value).lower()

    def test_circular_dependency(self, tmp_path):
        """Test error with circular dependency."""
        plan_data = {
            "execution_order": ["MF-001-A", "MF-001-B"],
            "dependency_graph": {
                "MF-001-A": ["MF-001-B"],
                "MF-001-B": ["MF-001-A"],
            },
        }
        plan_file = tmp_path / "plan.yaml"
        with open(plan_file, "w") as f:
            yaml.dump(plan_data, f)

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_plan_file(plan_file)
        assert "circular dependency" in str(exc_info.value).lower()


class TestValidateSubMissionDependencies:
    """Tests for validate_sub_mission_dependencies."""

    def test_valid_dependencies(self):
        """Test with valid dependencies."""
        sub_mission = SubMission(
            id="MF-001-B",
            parent="MF-001",
            title="Test",
            goal="Test",
            depends_on=["MF-001-A"],
        )
        available = ["MF-001-A", "MF-001-B"]

        # Should not raise
        SchemaValidator.validate_sub_mission_dependencies(sub_mission, available)

    def test_missing_dependency(self):
        """Test with missing dependency."""
        sub_mission = SubMission(
            id="MF-001-B",
            parent="MF-001",
            title="Test",
            goal="Test",
            depends_on=["MF-001-A", "MF-001-C"],  # C doesn't exist
        )
        available = ["MF-001-A", "MF-001-B"]

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_sub_mission_dependencies(sub_mission, available)
        assert "missing dependencies" in str(exc_info.value).lower()
        assert "MF-001-C" in str(exc_info.value)

    def test_no_dependencies(self):
        """Test with no dependencies."""
        sub_mission = SubMission(
            id="MF-001-A", parent="MF-001", title="Test", goal="Test"
        )
        available = ["MF-001-A"]

        # Should not raise
        SchemaValidator.validate_sub_mission_dependencies(sub_mission, available)


class TestValidateForbiddenPaths:
    """Tests for validate_forbidden_paths."""

    def test_no_conflicts(self):
        """Test with no path conflicts."""
        parent = ParentMission(
            id="MF-001", goal="Test", forbidden_paths=["core/**"]
        )
        sub = SubMission(
            id="MF-001-A",
            parent="MF-001",
            title="Test",
            goal="Test",
            allowed_paths=["src/**"],
        )

        # Should not raise
        SchemaValidator.validate_forbidden_paths(parent, sub)

    def test_path_conflict(self):
        """Test with path conflict."""
        parent = ParentMission(
            id="MF-001", goal="Test", forbidden_paths=["core/**"]
        )
        sub = SubMission(
            id="MF-001-A",
            parent="MF-001",
            title="Test",
            goal="Test",
            allowed_paths=["core/config.py"],  # Conflicts!
        )

        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_forbidden_paths(parent, sub)
        assert "conflict" in str(exc_info.value).lower()
        assert "core/config.py" in str(exc_info.value)

    def test_no_forbidden_paths(self):
        """Test with no forbidden paths."""
        parent = ParentMission(id="MF-001", goal="Test")
        sub = SubMission(
            id="MF-001-A",
            parent="MF-001",
            title="Test",
            goal="Test",
            allowed_paths=["anything/**"],
        )

        # Should not raise
        SchemaValidator.validate_forbidden_paths(parent, sub)


class TestValidateMissionStructure:
    """Tests for validate_mission_structure."""

    def test_valid_mission_structure(
        self, tmp_mission_dir, valid_parent_mission_data, valid_sub_mission_data
    ):
        """Test validating complete mission structure."""
        # Create mission.yaml
        mission_file = tmp_mission_dir / "mission.yaml"
        with open(mission_file, "w") as f:
            yaml.dump(valid_parent_mission_data, f)

        # Create plan.yaml
        plan_file = tmp_mission_dir / "plan.yaml"
        plan_data = {
            "execution_order": ["MF-001-A"],
            "dependency_graph": {"MF-001-A": []},
        }
        with open(plan_file, "w") as f:
            yaml.dump(plan_data, f)

        # Create sub-mission
        sub_file = tmp_mission_dir / "sub-missions" / "MF-001-A.yaml"
        with open(sub_file, "w") as f:
            yaml.dump(valid_sub_mission_data, f)

        results = SchemaValidator.validate_mission_structure(tmp_mission_dir)
        assert results["mission_file"] is True
        assert results["plan_file"] is True
        assert "MF-001-A" in results["sub_missions"]
        assert len(results["errors"]) == 0

    def test_missing_mission_file(self, tmp_mission_dir):
        """Test error when mission.yaml is missing."""
        with pytest.raises(MFValidationError) as exc_info:
            SchemaValidator.validate_mission_structure(tmp_mission_dir)
        assert "not found" in str(exc_info.value).lower()

    def test_sub_mission_parent_mismatch(
        self, tmp_mission_dir, valid_parent_mission_data, valid_sub_mission_data
    ):
        """Test detection of parent-child mismatch."""
        # Create mission.yaml
        mission_file = tmp_mission_dir / "mission.yaml"
        with open(mission_file, "w") as f:
            yaml.dump(valid_parent_mission_data, f)

        # Create sub-mission with wrong parent
        valid_sub_mission_data["parent"] = "MF-002"
        sub_file = tmp_mission_dir / "sub-missions" / "MF-001-A.yaml"
        with open(sub_file, "w") as f:
            yaml.dump(valid_sub_mission_data, f)

        results = SchemaValidator.validate_mission_structure(tmp_mission_dir)
        assert len(results["errors"]) > 0
        # Check for either "parent mismatch" or "does not match parent" in errors
        assert any(
            "parent mismatch" in err.lower() or "does not match parent" in err.lower()
            for err in results["errors"]
        )


# Made with Bob
