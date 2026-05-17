"""Integration tests for report command."""

import json
from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from missionforge.cli.app import app

runner = CliRunner()


@pytest.fixture
def mission_with_validation(tmp_path):
    """Create a complete mission structure with validation data."""
    # Create workspace structure
    workspace_dir = tmp_path / ".missionforge"
    missions_dir = workspace_dir / "missions"
    mission_dir = missions_dir / "MF-001"
    mission_dir.mkdir(parents=True)

    # Create mission.yaml
    mission_data = {
        "id": "MF-001",
        "goal": "Test mission for report generation",
        "test_command": "pytest",
        "forbidden_paths": ["*.secret"],
        "aggregate_metrics": {
            "code_quality": {"target": 90.0},
            "test_coverage": {"min": 80.0}
        },
        "sub_missions": ["MF-001-A", "MF-001-B"]
    }
    mission_file = mission_dir / "mission.yaml"
    mission_file.write_text(yaml.dump(mission_data))

    # Create sub-missions directory
    sub_missions_dir = mission_dir / "sub-missions"
    sub_missions_dir.mkdir()

    # Create sub-mission A
    sub_mission_a = {
        "id": "MF-001-A",
        "parent": "MF-001",
        "title": "Implement Feature A",
        "goal": "Add new feature A",
        "depends_on": [],
        "allowed_paths": ["src/feature_a/**"],
        "metrics": {
            "lines_of_code": {"max": 500.0}
        },
        "test_command": "pytest tests/test_feature_a.py"
    }
    sub_file_a = sub_missions_dir / "MF-001-A.yaml"
    sub_file_a.write_text(yaml.dump(sub_mission_a))

    # Create sub-mission B
    sub_mission_b = {
        "id": "MF-001-B",
        "parent": "MF-001",
        "title": "Implement Feature B",
        "goal": "Add new feature B",
        "depends_on": ["MF-001-A"],
        "allowed_paths": ["src/feature_b/**"],
        "metrics": {},
        "test_command": "pytest tests/test_feature_b.py"
    }
    sub_file_b = sub_missions_dir / "MF-001-B.yaml"
    sub_file_b.write_text(yaml.dump(sub_mission_b))

    # Create parent validation
    parent_validation = {
        "mission_id": "MF-001",
        "timestamp": "2026-05-17T10:00:00Z",
        "git_commit": "abc1234567890",
        "metrics": {
            "files_changed": 10,
            "lines_added": 200,
            "lines_removed": 50,
            "tests_passed": True,
            "test_coverage": 85.5,
            "custom_metrics": {
                "code_quality": 92.0,
                "test_coverage": 85.5
            }
        },
        "passed": True,
        "errors": []
    }
    validation_file = mission_dir / "validation.json"
    validation_file.write_text(json.dumps(parent_validation))

    # Create sub-mission A validation
    sub_validation_a = {
        "mission_id": "MF-001-A",
        "timestamp": "2026-05-17T09:00:00Z",
        "git_commit": "abc1234567890",
        "metrics": {
            "files_changed": 5,
            "lines_added": 100,
            "lines_removed": 20,
            "tests_passed": True,
            "test_coverage": 90.0,
            "custom_metrics": {
                "lines_of_code": 450.0
            }
        },
        "passed": True,
        "errors": []
    }
    sub_validation_file_a = sub_missions_dir / "MF-001-A.validation.json"
    sub_validation_file_a.write_text(json.dumps(sub_validation_a))

    # Create sub-mission B validation
    sub_validation_b = {
        "mission_id": "MF-001-B",
        "timestamp": "2026-05-17T09:30:00Z",
        "git_commit": "abc1234567890",
        "metrics": {
            "files_changed": 5,
            "lines_added": 100,
            "lines_removed": 30,
            "tests_passed": True,
            "test_coverage": 88.0,
            "custom_metrics": {}
        },
        "passed": True,
        "errors": []
    }
    sub_validation_file_b = sub_missions_dir / "MF-001-B.validation.json"
    sub_validation_file_b.write_text(json.dumps(sub_validation_b))

    # Create execution plan
    plan_data = {
        "execution_order": ["MF-001-A", "MF-001-B"],
        "dependency_graph": {
            "MF-001-A": [],
            "MF-001-B": ["MF-001-A"]
        }
    }
    plan_file = mission_dir / "plan.yaml"
    plan_file.write_text(yaml.dump(plan_data))

    return tmp_path


class TestReportCommand:
    """Test report command integration."""

    def test_report_command_success(self, mission_with_validation, monkeypatch):
        """Test successful report generation."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001"])

        assert result.exit_code == 0
        assert "Report generated successfully" in result.stdout

        # Check report file was created
        report_file = mission_with_validation / ".missionforge" / "missions" / "MF-001" / "report.md"
        assert report_file.exists()

        # Check report content
        content = report_file.read_text()
        assert "# Mission MF-001" in content
        assert "Test mission for report generation" in content
        assert "MF-001-A" in content
        assert "MF-001-B" in content

    def test_report_command_custom_output(self, mission_with_validation, monkeypatch):
        """Test report generation with custom output path."""
        monkeypatch.chdir(mission_with_validation)

        custom_output = mission_with_validation / "custom_report.md"
        result = runner.invoke(app, ["report", "MF-001", "--output", str(custom_output)])

        assert result.exit_code == 0
        assert custom_output.exists()

    def test_report_command_stdout(self, mission_with_validation, monkeypatch):
        """Test report generation to stdout."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001", "--stdout"])

        assert result.exit_code == 0
        assert "# Mission MF-001" in result.stdout
        assert "Test mission for report generation" in result.stdout

    def test_report_command_mission_not_found(self, mission_with_validation, monkeypatch):
        """Test report command with non-existent mission."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-999"])

        assert result.exit_code == 1
        assert "Mission MF-999 not found" in result.stdout

    def test_report_command_no_workspace(self, tmp_path, monkeypatch):
        """Test report command outside workspace."""
        monkeypatch.chdir(tmp_path)

        result = runner.invoke(app, ["report", "MF-001"])

        assert result.exit_code == 1

    def test_report_content_structure(self, mission_with_validation, monkeypatch):
        """Test that generated report has correct structure."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001"])
        assert result.exit_code == 0

        report_file = mission_with_validation / ".missionforge" / "missions" / "MF-001" / "report.md"
        content = report_file.read_text()

        # Check all required sections
        required_sections = [
            "# Mission MF-001",
            "Mission Goal",
            "Decomposition Summary",
            "Sub-Mission Results",
            "Aggregate Metrics",
            "Test Results",
            "Files Changed",
            "Forbidden Path Violations",
            "Next Steps",
            "Metadata"
        ]

        for section in required_sections:
            assert section in content, f"Missing section: {section}"

    def test_report_shows_passed_status(self, mission_with_validation, monkeypatch):
        """Test that report shows PASSED status when all validations pass."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001"])
        assert result.exit_code == 0

        report_file = mission_with_validation / ".missionforge" / "missions" / "MF-001" / "report.md"
        content = report_file.read_text()

        assert "PASSED" in content
        assert "**Status:**" in content

    def test_report_shows_sub_mission_details(self, mission_with_validation, monkeypatch):
        """Test that report includes sub-mission details."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001"])
        assert result.exit_code == 0

        report_file = mission_with_validation / ".missionforge" / "missions" / "MF-001" / "report.md"
        content = report_file.read_text()

        # Check sub-mission A details
        assert "MF-001-A" in content
        assert "Implement Feature A" in content
        assert "Add new feature A" in content

        # Check sub-mission B details
        assert "MF-001-B" in content
        assert "Implement Feature B" in content
        assert "Add new feature B" in content

    def test_report_shows_metrics(self, mission_with_validation, monkeypatch):
        """Test that report includes metrics comparison."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001"])
        assert result.exit_code == 0

        report_file = mission_with_validation / ".missionforge" / "missions" / "MF-001" / "report.md"
        content = report_file.read_text()

        # Check aggregate metrics
        assert "code_quality" in content
        assert "test_coverage" in content
        assert "92.0" in content  # code_quality value
        assert "85.5" in content  # test_coverage value

    def test_report_shows_test_results(self, mission_with_validation, monkeypatch):
        """Test that report includes test results."""
        monkeypatch.chdir(mission_with_validation)

        result = runner.invoke(app, ["report", "MF-001"])
        assert result.exit_code == 0

        report_file = mission_with_validation / ".missionforge" / "missions" / "MF-001" / "report.md"
        content = report_file.read_text()

        # Check test commands
        assert "pytest" in content
        assert "pytest tests/test_feature_a.py" in content
        assert "pytest tests/test_feature_b.py" in content


# Made with Bob