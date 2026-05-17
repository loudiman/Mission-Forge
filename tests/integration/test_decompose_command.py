"""Integration tests for decompose command."""

import pytest
from typer.testing import CliRunner

from missionforge.cli.app import app

runner = CliRunner()


@pytest.fixture
def test_mission(tmp_path):
    """Create a test mission structure."""
    workspace_dir = tmp_path / ".missionforge"
    missions_dir = workspace_dir / "missions"
    mission_dir = missions_dir / "MF-001"
    mission_dir.mkdir(parents=True)

    # Create valid mission.yaml
    mission_yaml = mission_dir / "mission.yaml"
    mission_yaml.write_text("""id: MF-001
goal: "Test mission for decomposition"
test_command: "pytest tests/"
forbidden_paths:
  - ".git/**"
  - "*.pyc"
""")

    return tmp_path


@pytest.fixture
def test_mission_with_sub_missions(test_mission):
    """Create a test mission with sub-missions."""
    mission_dir = test_mission / ".missionforge" / "missions" / "MF-001"
    sub_missions_dir = mission_dir / "sub-missions"
    sub_missions_dir.mkdir()

    # Create sub-mission A
    sub_a = sub_missions_dir / "MF-001-A.yaml"
    sub_a.write_text("""id: MF-001-A
parent: MF-001
title: "Sub-mission A"
goal: "First sub-mission"
allowed_paths:
  - "src/module_a/**"
""")

    # Create sub-mission B
    sub_b = sub_missions_dir / "MF-001-B.yaml"
    sub_b.write_text("""id: MF-001-B
parent: MF-001
title: "Sub-mission B"
goal: "Second sub-mission"
depends_on:
  - MF-001-A
allowed_paths:
  - "src/module_b/**"
""")

    return test_mission


class TestDecomposeCommand:
    """Test decompose command functionality."""

    def test_decompose_creates_sub_missions_directory(self, test_mission, monkeypatch):
        """Test that decompose creates sub-missions directory on first run."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        sub_missions_dir = test_mission / ".missionforge" / "missions" / "MF-001" / "sub-missions"
        assert sub_missions_dir.exists()
        assert sub_missions_dir.is_dir()
        assert "Created:" in result.stdout
        assert "Already exists:" not in result.stdout

    def test_decompose_reports_existing_directory_on_second_run(self, test_mission, monkeypatch):
        """Test that a second decompose run reports the directory already exists."""
        monkeypatch.chdir(test_mission)

        # First run creates the directory
        runner.invoke(app, ["decompose", "MF-001"])

        # Second run should acknowledge it already exists
        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Already exists:" in result.stdout
        assert "Created:" not in result.stdout

    def test_decompose_validates_parent_mission(self, test_mission, monkeypatch):
        """Test that decompose validates parent mission first."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Validating parent mission" in result.stdout
        assert "Parent mission is valid" in result.stdout

    def test_decompose_displays_instructions(self, test_mission, monkeypatch):
        """Test that decompose displays clear instructions."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Instructions for Bob" in result.stdout
        assert "Read the codebase" in result.stdout
        assert "Break down into logical sub-missions" in result.stdout

    def test_decompose_displays_template(self, test_mission, monkeypatch):
        """Test that decompose displays sub-mission template."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Sub-mission template" in result.stdout
        assert "id: MF-001-A" in result.stdout
        assert "parent: MF-001" in result.stdout
        assert "allowed_paths:" in result.stdout

    def test_decompose_displays_plan_guidance(self, test_mission, monkeypatch):
        """Test that decompose displays plan.yaml guidance."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Execution Plan" in result.stdout
        assert "execution_order:" in result.stdout
        assert "dependency_graph:" in result.stdout

    def test_decompose_shows_current_status(self, test_mission_with_sub_missions, monkeypatch):
        """Test that decompose shows current status of sub-missions."""
        monkeypatch.chdir(test_mission_with_sub_missions)

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Current Status" in result.stdout
        assert "MF-001-A.yaml" in result.stdout
        assert "MF-001-B.yaml" in result.stdout

    def test_decompose_fails_for_nonexistent_mission(self, test_mission, monkeypatch):
        """Test that decompose fails for non-existent mission."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["decompose", "MF-999"])

        assert result.exit_code == 1
        assert "Mission MF-999 not found" in result.stdout

    def test_decompose_fails_for_invalid_mission(self, test_mission, monkeypatch):
        """Test that decompose fails for invalid mission."""
        monkeypatch.chdir(test_mission)

        # Create invalid mission
        mission_dir = test_mission / ".missionforge" / "missions" / "MF-002"
        mission_dir.mkdir()
        mission_yaml = mission_dir / "mission.yaml"
        mission_yaml.write_text("""id: MF-002
goal: ""
""")  # Empty goal is invalid

        result = runner.invoke(app, ["decompose", "MF-002"])

        assert result.exit_code == 1
        assert "validation failed" in result.stdout.lower()


class TestValidateSubmissionCommand:
    """Test validate-submission command functionality."""

    def test_validate_submission_validates_valid_sub_mission(
        self, test_mission_with_sub_missions, monkeypatch
    ):
        """Test validation of valid sub-mission."""
        monkeypatch.chdir(test_mission_with_sub_missions)

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-A"])

        assert result.exit_code == 0
        assert "Validation Success" in result.stdout
        assert "is valid" in result.stdout

    def test_validate_submission_checks_id_format(self, test_mission, monkeypatch):
        """Test that validation checks sub-mission ID format."""
        monkeypatch.chdir(test_mission)

        # Create sub-mission with invalid ID
        sub_missions_dir = test_mission / ".missionforge" / "missions" / "MF-001" / "sub-missions"
        sub_missions_dir.mkdir()

        invalid_sub = sub_missions_dir / "MF-001-INVALID.yaml"
        invalid_sub.write_text("""id: MF-001-INVALID
parent: MF-001
title: "Invalid ID"
goal: "Test invalid ID format"
""")

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-INVALID"])

        assert result.exit_code == 1
        assert "Invalid sub-mission ID format" in result.stdout

    def test_validate_submission_checks_parent_reference(self, test_mission, monkeypatch):
        """Test that validation checks parent reference."""
        monkeypatch.chdir(test_mission)

        # Create sub-mission with wrong parent
        sub_missions_dir = test_mission / ".missionforge" / "missions" / "MF-001" / "sub-missions"
        sub_missions_dir.mkdir()

        wrong_parent = sub_missions_dir / "MF-001-A.yaml"
        wrong_parent.write_text("""id: MF-001-A
parent: MF-999
title: "Wrong parent"
goal: "Test wrong parent reference"
""")

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-A"])

        assert result.exit_code == 1
        # The schema validator enforces the parent constraint at parse time,
        # so the error is a schema validation failure rather than the later
        # command-level "Parent mismatch" check.
        assert "does not match parent ID" in result.stdout

    def test_validate_submission_checks_forbidden_paths(self, test_mission, monkeypatch):
        """Test that validation checks forbidden paths."""
        monkeypatch.chdir(test_mission)

        # Create sub-mission with forbidden path
        sub_missions_dir = test_mission / ".missionforge" / "missions" / "MF-001" / "sub-missions"
        sub_missions_dir.mkdir()

        forbidden_path = sub_missions_dir / "MF-001-A.yaml"
        forbidden_path.write_text("""id: MF-001-A
parent: MF-001
title: "Forbidden path"
goal: "Test forbidden path"
allowed_paths:
  - ".git/config"
""")

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-A"])

        assert result.exit_code == 1
        assert "conflict" in result.stdout.lower()

    def test_validate_submission_checks_dependencies(
        self, test_mission_with_sub_missions, monkeypatch
    ):
        """Test that validation checks dependencies exist."""
        monkeypatch.chdir(test_mission_with_sub_missions)

        # Create sub-mission with missing dependency
        sub_missions_dir = (
            test_mission_with_sub_missions
            / ".missionforge"
            / "missions"
            / "MF-001"
            / "sub-missions"
        )

        missing_dep = sub_missions_dir / "MF-001-C.yaml"
        missing_dep.write_text("""id: MF-001-C
parent: MF-001
title: "Missing dependency"
goal: "Test missing dependency"
depends_on:
  - MF-001-Z
""")

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-C"])

        assert result.exit_code == 1
        assert "Missing dependencies" in result.stdout
        assert "MF-001-Z" in result.stdout

    def test_validate_submission_warns_about_overlapping_paths(
        self, test_mission_with_sub_missions, monkeypatch
    ):
        """Test that validation warns about overlapping paths."""
        monkeypatch.chdir(test_mission_with_sub_missions)

        # Create sub-mission with overlapping path
        sub_missions_dir = (
            test_mission_with_sub_missions
            / ".missionforge"
            / "missions"
            / "MF-001"
            / "sub-missions"
        )

        overlap = sub_missions_dir / "MF-001-C.yaml"
        overlap.write_text("""id: MF-001-C
parent: MF-001
title: "Overlapping path"
goal: "Test overlapping path"
allowed_paths:
  - "src/module_a/**"
""")

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-C"])

        # Should succeed but with warnings
        assert result.exit_code == 0
        assert "overlaps" in result.stdout.lower()
        # The conflicting path must appear in the warning text
        assert "src/module_a/**" in result.stdout

    def test_validate_submission_no_duplicate_overlap_warnings(
        self, test_mission_with_sub_missions, monkeypatch
    ):
        """Identical paths in two sub-missions must produce exactly one warning.

        MF-001-A already declares 'src/module_a/**'. When MF-001-C uses the same
        path the bidirectional overlap check previously emitted two warnings for
        the same path (one per direction). Only one warning should appear.
        """
        monkeypatch.chdir(test_mission_with_sub_missions)

        sub_missions_dir = (
            test_mission_with_sub_missions
            / ".missionforge"
            / "missions"
            / "MF-001"
            / "sub-missions"
        )

        overlap = sub_missions_dir / "MF-001-C.yaml"
        overlap.write_text("""id: MF-001-C
parent: MF-001
title: "Same path as A"
goal: "Test duplicate warning suppression"
allowed_paths:
  - "src/module_a/**"
""")

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-C"])

        assert result.exit_code == 0
        # The conflicting path must appear exactly once, not duplicated
        assert result.stdout.count("src/module_a/**") == 1

    def test_validate_submission_fails_for_nonexistent_file(self, test_mission, monkeypatch):
        """Test that validation fails for non-existent sub-mission file."""
        monkeypatch.chdir(test_mission)

        result = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-Z"])

        assert result.exit_code == 1
        assert "not found" in result.stdout


class TestDecomposeWorkflow:
    """Test complete decompose workflow."""

    def test_full_decompose_workflow(self, test_mission, monkeypatch):
        """Test complete workflow from decompose to validation."""
        monkeypatch.chdir(test_mission)

        # Step 1: Run decompose
        result = runner.invoke(app, ["decompose", "MF-001"])
        assert result.exit_code == 0

        # Step 2: Create sub-mission files
        sub_missions_dir = test_mission / ".missionforge" / "missions" / "MF-001" / "sub-missions"

        sub_a = sub_missions_dir / "MF-001-A.yaml"
        sub_a.write_text("""id: MF-001-A
parent: MF-001
title: "First sub-mission"
goal: "Implement feature A"
allowed_paths:
  - "src/feature_a/**"
test_command: "pytest tests/test_feature_a.py"
""")

        sub_b = sub_missions_dir / "MF-001-B.yaml"
        sub_b.write_text("""id: MF-001-B
parent: MF-001
title: "Second sub-mission"
goal: "Implement feature B"
depends_on:
  - MF-001-A
allowed_paths:
  - "src/feature_b/**"
test_command: "pytest tests/test_feature_b.py"
""")

        # Step 3: Validate each sub-mission
        result_a = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-A"])
        assert result_a.exit_code == 0
        assert "is valid" in result_a.stdout

        result_b = runner.invoke(app, ["validate-submission", "MF-001", "MF-001-B"])
        assert result_b.exit_code == 0
        assert "is valid" in result_b.stdout

        # Step 4: Create plan.yaml
        mission_dir = test_mission / ".missionforge" / "missions" / "MF-001"
        plan_yaml = mission_dir / "plan.yaml"
        plan_yaml.write_text("""execution_order:
  - MF-001-A
  - MF-001-B
dependency_graph:
  MF-001-A: []
  MF-001-B: [MF-001-A]
""")

        # Step 5: Run decompose again to see updated status
        result_final = runner.invoke(app, ["decompose", "MF-001"])
        assert result_final.exit_code == 0
        assert "MF-001-A.yaml" in result_final.stdout
        assert "MF-001-B.yaml" in result_final.stdout
        assert "plan.yaml" in result_final.stdout
        assert "Valid" in result_final.stdout

    def test_decompose_detects_id_mismatch(self, test_mission, monkeypatch):
        """Test that decompose detects ID mismatches in status."""
        monkeypatch.chdir(test_mission)

        # Create sub-mission with ID that doesn't match parent
        sub_missions_dir = test_mission / ".missionforge" / "missions" / "MF-001" / "sub-missions"
        sub_missions_dir.mkdir()

        wrong_id = sub_missions_dir / "MF-002-A.yaml"
        wrong_id.write_text("""id: MF-002-A
parent: MF-002
title: "Wrong parent"
goal: "Test wrong parent"
""")

        result = runner.invoke(app, ["decompose", "MF-001"])

        assert result.exit_code == 0
        assert "Current Status" in result.stdout
        # Verify the status table lists the offending file
        assert "MF-002-A.yaml" in result.stdout
        # Verify the parent mismatch is flagged in the status column
        assert "Parent mismatch" in result.stdout
        # Verify the expected parent is shown in the validation column
        assert "Expected: MF-001" in result.stdout


# Made with Bob
