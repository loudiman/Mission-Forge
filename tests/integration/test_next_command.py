# Made with Bob
"""Integration tests for the next command."""

import json
from pathlib import Path

from typer.testing import CliRunner

from missionforge.cli.app import app

runner = CliRunner()

MISSION_YAML = """id: MF-001
goal: "Test mission for next command"
test_command: "pytest tests/"
forbidden_paths:
  - ".git/**"
"""

SUB_A = """id: MF-001-A
parent: MF-001
title: "Sub-mission A"
goal: "First sub-mission, no deps"
allowed_paths:
  - "src/module_a/**"
"""

SUB_B_AFTER_A = """id: MF-001-B
parent: MF-001
title: "Sub-mission B"
goal: "Second sub-mission, depends on A"
depends_on:
  - MF-001-A
allowed_paths:
  - "src/module_b/**"
"""

SUB_C_AFTER_A = """id: MF-001-C
parent: MF-001
title: "Sub-mission C"
goal: "Third sub-mission, depends on A"
depends_on:
  - MF-001-A
allowed_paths:
  - "src/module_c/**"
"""

SUB_D_AFTER_BC = """id: MF-001-D
parent: MF-001
title: "Sub-mission D"
goal: "Fourth sub-mission, depends on B and C"
depends_on:
  - MF-001-B
  - MF-001-C
allowed_paths:
  - "src/module_d/**"
"""

VALIDATION_PASSED = {
    "status": "PASSED",
    "deterministic_evidence": {
        "files_changed": [],
        "scope_check": {
            "allowed_paths_satisfied": True,
            "forbidden_paths_violated": False,
            "violations": [],
        },
    },
    "metrics": [],
}

VALIDATION_FAILED = {**VALIDATION_PASSED, "status": "FAILED"}


def _setup_workspace(
    tmp_path: Path,
    plan_yaml: str,
    sub_missions: dict[str, str],
    validations: dict[str, dict] | None = None,
) -> Path:
    mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
    sub_dir = mission_dir / "sub-missions"
    sub_dir.mkdir(parents=True)
    (mission_dir / "mission.yaml").write_text(MISSION_YAML)
    (mission_dir / "plan.yaml").write_text(plan_yaml)

    for sub_id, content in sub_missions.items():
        sub_sub_dir = sub_dir / sub_id
        sub_sub_dir.mkdir(parents=True)
        (sub_sub_dir / "sub-mission.yaml").write_text(content)

    if validations:
        for sub_id, val_data in validations.items():
            val_data_with_id = {**val_data, "sub_mission_id": sub_id}
            val_path = sub_dir / sub_id / "validation.json"
            val_path.write_text(json.dumps(val_data_with_id))

    return tmp_path


LINEAR_PLAN = """execution_order:
  - MF-001-A
  - MF-001-B
dependency_graph:
  MF-001-A: []
  MF-001-B:
    - MF-001-A
"""

DIAMOND_PLAN = """execution_order:
  - MF-001-A
  - MF-001-B
  - MF-001-C
  - MF-001-D
dependency_graph:
  MF-001-A: []
  MF-001-B:
    - MF-001-A
  MF-001-C:
    - MF-001-A
  MF-001-D:
    - MF-001-B
    - MF-001-C
"""


class TestNextCommandFirstSubMission:
    def test_first_sub_mission_recommended(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 0
        assert "MF-001-A" in result.output
        assert "recommended next" in result.output

    def test_shows_progress_header(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert "0/2" in result.output


class TestNextCommandLinearChain:
    def test_second_ready_when_first_passed(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
            validations={"MF-001-A": VALIDATION_PASSED},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 0
        assert "MF-001-B" in result.output
        assert "recommended next" in result.output
        assert "MF-001-A" in result.output  # in COMPLETE section

    def test_shows_one_of_two_complete(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
            validations={"MF-001-A": VALIDATION_PASSED},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert "1/2" in result.output


class TestNextCommandDiamondDependency:
    def test_both_b_and_c_ready_when_a_passed(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            DIAMOND_PLAN,
            {
                "MF-001-A": SUB_A,
                "MF-001-B": SUB_B_AFTER_A,
                "MF-001-C": SUB_C_AFTER_A,
                "MF-001-D": SUB_D_AFTER_BC,
            },
            validations={"MF-001-A": VALIDATION_PASSED},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 0
        assert "MF-001-B" in result.output
        assert "MF-001-C" in result.output
        assert "MF-001-D" in result.output  # in BLOCKED section

    def test_d_ready_when_b_and_c_passed(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            DIAMOND_PLAN,
            {
                "MF-001-A": SUB_A,
                "MF-001-B": SUB_B_AFTER_A,
                "MF-001-C": SUB_C_AFTER_A,
                "MF-001-D": SUB_D_AFTER_BC,
            },
            validations={
                "MF-001-A": VALIDATION_PASSED,
                "MF-001-B": VALIDATION_PASSED,
                "MF-001-C": VALIDATION_PASSED,
            },
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 0
        assert "MF-001-D" in result.output
        assert "recommended next" in result.output


class TestNextCommandAllComplete:
    def test_exit_zero_and_complete_message(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
            validations={
                "MF-001-A": VALIDATION_PASSED,
                "MF-001-B": VALIDATION_PASSED,
            },
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 0
        assert "All sub-missions complete" in result.output

    def test_shows_two_of_two_complete(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
            validations={
                "MF-001-A": VALIDATION_PASSED,
                "MF-001-B": VALIDATION_PASSED,
            },
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert "2/2" in result.output


class TestNextCommandNoneReady:
    def test_exit_one_when_all_blocked(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
            validations={"MF-001-A": VALIDATION_FAILED},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 1

    def test_shows_failed_section(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            LINEAR_PLAN,
            {"MF-001-A": SUB_A, "MF-001-B": SUB_B_AFTER_A},
            validations={"MF-001-A": VALIDATION_FAILED},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert "FAILED" in result.output
        assert "MF-001-A" in result.output


class TestNextCommandMissingPlan:
    def test_error_when_no_plan_yaml(self, tmp_path, monkeypatch):
        mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
        mission_dir.mkdir(parents=True)
        (mission_dir / "mission.yaml").write_text(MISSION_YAML)
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 1
        assert "plan" in result.output.lower()

    def test_error_suggests_plan_command(self, tmp_path, monkeypatch):
        mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
        mission_dir.mkdir(parents=True)
        (mission_dir / "mission.yaml").write_text(MISSION_YAML)
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["next", "MF-001"])
        assert "missionforge plan" in result.output


class TestNextCommandPartialProgress:
    def test_c_ready_d_blocked_after_a_and_b_pass(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            DIAMOND_PLAN,
            {
                "MF-001-A": SUB_A,
                "MF-001-B": SUB_B_AFTER_A,
                "MF-001-C": SUB_C_AFTER_A,
                "MF-001-D": SUB_D_AFTER_BC,
            },
            validations={
                "MF-001-A": VALIDATION_PASSED,
                "MF-001-B": VALIDATION_PASSED,
            },
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["next", "MF-001"])
        assert result.exit_code == 0
        assert "MF-001-C" in result.output
        assert "MF-001-D" in result.output
        assert "BLOCKED" in result.output
