"""Unit tests for report generator."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from missionforge.core.report_generator import ReportGenerator
from missionforge.models.schemas import ParentMission


@pytest.fixture
def sample_mission_data():
    """Sample mission data for testing."""
    return {
        "id": "MF-001",
        "goal": "Test mission goal",
        "test_command": "pytest",
        "forbidden_paths": ["*.secret"],
        "aggregate_metrics": {
            "test_metric": {"target": 100.0}
        },
        "sub_missions": ["MF-001-A", "MF-001-B"]
    }


@pytest.fixture
def sample_sub_mission_data():
    """Sample sub-mission data for testing."""
    return {
        "id": "MF-001-A",
        "parent": "MF-001",
        "title": "Test Sub-Mission",
        "goal": "Test sub-mission goal",
        "depends_on": [],
        "allowed_paths": ["src/**"],
        "metrics": {},
        "test_command": "pytest tests/unit"
    }


@pytest.fixture
def sample_validation_data():
    """Sample validation data for testing."""
    return {
        "mission_id": "MF-001",
        "timestamp": "2026-05-17T10:00:00Z",
        "git_commit": "abc1234",
        "metrics": {
            "files_changed": 5,
            "lines_added": 100,
            "lines_removed": 50,
            "tests_passed": True,
            "test_coverage": 85.5,
            "custom_metrics": {
                "test_metric": 100.0
            }
        },
        "passed": True,
        "errors": []
    }


@pytest.fixture
def temp_mission_dir(tmp_path, sample_mission_data, sample_sub_mission_data, sample_validation_data):
    """Create temporary mission directory structure."""
    mission_dir = tmp_path / "MF-001"
    mission_dir.mkdir()

    # Create mission.yaml
    mission_file = mission_dir / "mission.yaml"
    mission_file.write_text(yaml.dump(sample_mission_data))

    # Create sub-missions directory
    sub_missions_dir = mission_dir / "sub-missions"
    sub_missions_dir.mkdir()

    # Create sub-mission file
    sub_mission_file = sub_missions_dir / "MF-001-A.yaml"
    sub_mission_file.write_text(yaml.dump(sample_sub_mission_data))

    # Create validation file
    validation_file = mission_dir / "validation.json"
    validation_file.write_text(json.dumps(sample_validation_data))

    # Create sub-mission validation file
    sub_validation_file = sub_missions_dir / "MF-001-A.validation.json"
    sub_validation_data = sample_validation_data.copy()
    sub_validation_data["mission_id"] = "MF-001-A"
    sub_validation_file.write_text(json.dumps(sub_validation_data))

    return mission_dir


class TestReportGenerator:
    """Test ReportGenerator class."""

    def test_init(self):
        """Test ReportGenerator initialization."""
        generator = ReportGenerator()
        assert generator.env is not None

    def test_generate_report_creates_file(self, temp_mission_dir):
        """Test that generate_report creates a report file."""
        generator = ReportGenerator()

        with patch("missionforge.core.report_generator.get_commit_hash") as mock_commit:
            with patch("missionforge.core.report_generator.get_diff_stats") as mock_stats:
                with patch("missionforge.core.report_generator.get_changed_files_detailed") as mock_files:
                    mock_commit.return_value = "abc1234567890"
                    mock_stats.return_value = {
                        "files_changed": 5,
                        "insertions": 100,
                        "deletions": 50
                    }
                    mock_files.return_value = {
                        "added": [Path("new_file.py")],
                        "modified": [Path("existing_file.py")],
                        "deleted": [],
                        "renamed": []
                    }

                    content, output_path = generator.generate_report(temp_mission_dir)

        assert output_path.exists()
        assert output_path.name == "report.md"
        assert len(content) > 0

    def test_generate_report_custom_output(self, temp_mission_dir):
        """Test generate_report with custom output path."""
        generator = ReportGenerator()
        custom_output = temp_mission_dir / "custom_report.md"

        with patch("missionforge.core.report_generator.get_commit_hash") as mock_commit:
            with patch("missionforge.core.report_generator.get_diff_stats") as mock_stats:
                with patch("missionforge.core.report_generator.get_changed_files_detailed") as mock_files:
                    mock_commit.return_value = "abc1234567890"
                    mock_stats.return_value = {
                        "files_changed": 5,
                        "insertions": 100,
                        "deletions": 50
                    }
                    mock_files.return_value = {
                        "added": [],
                        "modified": [],
                        "deleted": [],
                        "renamed": []
                    }

                    content, output_path = generator.generate_report(temp_mission_dir, custom_output)

        assert output_path == custom_output
        assert output_path.exists()

    def test_generate_report_content_structure(self, temp_mission_dir):
        """Test that generated report contains expected sections."""
        generator = ReportGenerator()

        with patch("missionforge.core.report_generator.get_commit_hash") as mock_commit:
            with patch("missionforge.core.report_generator.get_diff_stats") as mock_stats:
                with patch("missionforge.core.report_generator.get_changed_files_detailed") as mock_files:
                    mock_commit.return_value = "abc1234567890"
                    mock_stats.return_value = {
                        "files_changed": 5,
                        "insertions": 100,
                        "deletions": 50
                    }
                    mock_files.return_value = {
                        "added": [],
                        "modified": [],
                        "deleted": [],
                        "renamed": []
                    }

                    content, _ = generator.generate_report(temp_mission_dir)

        # Check for expected sections
        assert "# Mission MF-001" in content
        assert "Mission Goal" in content
        assert "Decomposition Summary" in content
        assert "Sub-Mission Results" in content
        assert "Aggregate Metrics" in content
        assert "Test Results" in content
        assert "Files Changed" in content
        assert "Forbidden Path Violations" in content
        assert "Next Steps" in content
        assert "Metadata" in content

    def test_calculate_overall_status_passed(self):
        """Test overall status calculation when all pass."""
        generator = ReportGenerator()
        validation_results = {
            "MF-001": {"passed": True},
            "MF-001-A": {"passed": True}
        }
        status = generator._calculate_overall_status(validation_results)
        assert status == "PASSED"

    def test_calculate_overall_status_failed(self):
        """Test overall status calculation when some fail."""
        generator = ReportGenerator()
        validation_results = {
            "MF-001": {"passed": True},
            "MF-001-A": {"passed": False}
        }
        status = generator._calculate_overall_status(validation_results)
        assert status == "FAILED"

    def test_calculate_overall_status_incomplete(self):
        """Test overall status calculation when no results."""
        generator = ReportGenerator()
        validation_results = {}
        status = generator._calculate_overall_status(validation_results)
        assert status == "INCOMPLETE"

    def test_load_sub_missions(self, temp_mission_dir):
        """Test loading sub-missions."""
        generator = ReportGenerator()
        sub_missions = generator._load_sub_missions(temp_mission_dir, "MF-001")

        assert len(sub_missions) == 1
        assert sub_missions[0]["id"] == "MF-001-A"
        assert sub_missions[0]["title"] == "Test Sub-Mission"

    def test_load_validation_results(self, temp_mission_dir):
        """Test loading validation results."""
        generator = ReportGenerator()
        sub_missions = [{"id": "MF-001-A"}]
        results = generator._load_validation_results(temp_mission_dir, sub_missions)

        assert "MF-001" in results
        assert "MF-001-A" in results
        assert results["MF-001"]["passed"] is True
        assert results["MF-001-A"]["passed"] is True

    def test_collect_metrics_comparison(self, sample_mission_data):
        """Test metrics comparison collection."""
        generator = ReportGenerator()
        parent_mission = ParentMission(**sample_mission_data)
        validation_results = {
            "MF-001": {
                "metrics": {
                    "custom_metrics": {
                        "test_metric": 100.0
                    }
                }
            }
        }

        comparisons = generator._collect_metrics_comparison(parent_mission, validation_results)

        assert len(comparisons) == 1
        assert comparisons[0]["name"] == "test_metric"
        assert comparisons[0]["target"] == 100.0
        assert comparisons[0]["final"] == 100.0
        assert comparisons[0]["status"] == "PASSED"

    def test_generate_dependency_diagram(self):
        """Test dependency diagram generation."""
        generator = ReportGenerator()
        sub_missions = [
            {"id": "MF-001-A", "depends_on": []},
            {"id": "MF-001-B", "depends_on": ["MF-001-A"]}
        ]

        diagram = generator._generate_dependency_diagram(sub_missions, None)

        assert "MF-001-A" in diagram
        assert "MF-001-B" in diagram
        assert "no dependencies" in diagram
        assert "depends on: MF-001-A" in diagram

    def test_check_forbidden_violations(self, sample_mission_data):
        """Test forbidden path violation checking."""
        generator = ReportGenerator()
        parent_mission = ParentMission(**sample_mission_data)
        validation_results = {
            "MF-001-A": {
                "errors": ["Modified forbidden path: secret.txt"]
            }
        }

        violations = generator._check_forbidden_violations(parent_mission, validation_results)

        assert len(violations) == 1
        assert "MF-001-A" in violations[0]
        assert "forbidden" in violations[0].lower()


# Made with Bob