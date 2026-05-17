# Made with Bob
"""Integration tests for the plan command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from missionforge.cli.app import app
from missionforge.schemas import SchemaValidator

runner = CliRunner()

MISSION_YAML = """id: MF-001
goal: "Test mission for plan command"
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


def _setup_workspace(
    tmp_path: Path,
    sub_missions: dict[str, str],
    *,
    layout: str = "flat",
    mission_yaml: str = MISSION_YAML,
) -> Path:
    """Create a test workspace with the given sub-mission YAML files."""
    mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
    sub_dir = mission_dir / "sub-missions"
    sub_dir.mkdir(parents=True)
    (mission_dir / "mission.yaml").write_text(mission_yaml)

    for filename, content in sub_missions.items():
        if layout == "canonical":
            sub_id = Path(filename).stem
            target_dir = sub_dir / sub_id
            target_dir.mkdir(parents=True)
            (target_dir / "sub-mission.yaml").write_text(content)
        else:
            (sub_dir / filename).write_text(content)

    return tmp_path


@pytest.fixture
def mission_linear(tmp_path):
    return _setup_workspace(tmp_path, {
        "MF-001-A.yaml": SUB_A,
        "MF-001-B.yaml": SUB_B_AFTER_A,
    })


@pytest.fixture
def mission_diamond(tmp_path):
    return _setup_workspace(tmp_path, {
        "MF-001-A.yaml": SUB_A,
        "MF-001-B.yaml": SUB_B_AFTER_A,
        "MF-001-C.yaml": SUB_C_AFTER_A,
        "MF-001-D.yaml": SUB_D_AFTER_BC,
    })


@pytest.fixture
def mission_with_cycle(tmp_path):
    cycle_a = """id: MF-001-A
parent: MF-001
title: "Cycle A"
goal: "A depends on B"
depends_on:
  - MF-001-B
allowed_paths:
  - "src/a/**"
"""
    cycle_b = """id: MF-001-B
parent: MF-001
title: "Cycle B"
goal: "B depends on A"
depends_on:
  - MF-001-A
allowed_paths:
  - "src/b/**"
"""
    return _setup_workspace(tmp_path, {
        "MF-001-A.yaml": cycle_a,
        "MF-001-B.yaml": cycle_b,
    })


@pytest.fixture
def mission_missing_dep(tmp_path):
    missing = """id: MF-001-A
parent: MF-001
title: "Missing dep"
goal: "A depends on non-existent Z"
depends_on:
  - MF-001-Z
allowed_paths:
  - "src/a/**"
"""
    return _setup_workspace(tmp_path, {"MF-001-A.yaml": missing})


class TestPlanCommandSuccess:
    def test_exit_code_zero_linear(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 0

    def test_supports_canonical_sub_mission_layout(self, tmp_path, monkeypatch):
        ws = _setup_workspace(
            tmp_path,
            {"MF-001-A.yaml": SUB_A, "MF-001-B.yaml": SUB_B_AFTER_A},
            layout="canonical",
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 0
        plan_file = ws / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert plan.execution_order == ["MF-001-A", "MF-001-B"]

    def test_creates_plan_yaml(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_linear / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        assert plan_file.exists()

    def test_plan_yaml_is_valid(self, mission_diamond, monkeypatch):
        monkeypatch.chdir(mission_diamond)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_diamond / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert len(plan.execution_order) == 4
        assert len(plan.dependency_graph) == 4
        assert plan.sub_missions == plan.execution_order

    def test_linear_order_correct(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_linear / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert plan.execution_order.index("MF-001-A") < plan.execution_order.index("MF-001-B")

    def test_diamond_a_first_d_last(self, mission_diamond, monkeypatch):
        monkeypatch.chdir(mission_diamond)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_diamond / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert plan.execution_order[0] == "MF-001-A"
        assert plan.execution_order[-1] == "MF-001-D"

    def test_output_shows_execution_plan(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert "Execution Plan" in result.stdout

    def test_output_shows_parallelism(self, mission_diamond, monkeypatch):
        monkeypatch.chdir(mission_diamond)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert "Parallelism" in result.stdout
        assert "Level 0" in result.stdout
        assert "Level 1" in result.stdout

    def test_output_shows_ready_and_blocked(self, mission_diamond, monkeypatch):
        monkeypatch.chdir(mission_diamond)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert "Ready" in result.stdout
        assert "Blocked" in result.stdout
        assert "waiting on" in result.stdout

    def test_plan_yaml_contains_mission_id(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_linear / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        content = plan_file.read_text()
        assert "mission_id: MF-001" in content

    def test_plan_yaml_schema_includes_mission_id(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_linear / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert plan.mission_id == "MF-001"

    def test_plan_yaml_includes_rationale_when_present(self, tmp_path, monkeypatch):
        mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
        sub_dir = mission_dir / "sub-missions"
        sub_dir.mkdir(parents=True)
        (mission_dir / "mission.yaml").write_text(
            MISSION_YAML + "decomposition_rationale: Split by domain concerns\n"
        )
        (sub_dir / "MF-001-A.yaml").write_text(SUB_A)
        monkeypatch.chdir(tmp_path)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_dir / "plan.yaml"
        content = plan_file.read_text()
        assert "decomposition_rationale" in content
        assert "Split by domain concerns" in content

    def test_plan_yaml_omits_rationale_when_absent(self, mission_linear, monkeypatch):
        monkeypatch.chdir(mission_linear)
        runner.invoke(app, ["plan", "MF-001"])
        plan_file = mission_linear / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        content = plan_file.read_text()
        assert "decomposition_rationale" not in content

    def test_single_sub_mission(self, tmp_path, monkeypatch):
        ws = _setup_workspace(tmp_path, {"MF-001-A.yaml": SUB_A})
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 0
        plan_file = ws / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert plan.execution_order == ["MF-001-A"]

    def test_syncs_parent_mission_sub_missions(self, mission_diamond, monkeypatch):
        monkeypatch.chdir(mission_diamond)
        runner.invoke(app, ["plan", "MF-001"])
        mission_file = mission_diamond / ".missionforge" / "missions" / "MF-001" / "mission.yaml"
        parent = SchemaValidator.validate_parent_mission_file(mission_file)
        assert parent.sub_missions == ["MF-001-A", "MF-001-B", "MF-001-C", "MF-001-D"]

    def test_persists_path_overlap_warnings(self, tmp_path, monkeypatch):
        overlap_a = """id: MF-001-A
parent: MF-001
title: "Overlap A"
goal: "Broad path"
allowed_paths:
  - "src/shared/**"
"""
        overlap_b = """id: MF-001-B
parent: MF-001
title: "Overlap B"
goal: "Specific path"
allowed_paths:
  - "src/shared/config.py"
"""
        ws = _setup_workspace(
            tmp_path,
            {"MF-001-A.yaml": overlap_a, "MF-001-B.yaml": overlap_b},
        )
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 0
        plan_file = ws / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        plan = SchemaValidator.validate_plan_file(plan_file)
        assert len(plan.path_overlaps) == 1
        assert plan.path_overlaps[0].sub_mission_a == "MF-001-A"
        assert plan.path_overlaps[0].sub_mission_b == "MF-001-B"
        assert plan.path_overlaps[0].overlapping_patterns == ["src/shared/config.py"]


class TestPlanCommandErrors:
    def test_detects_cycle_exit_code(self, mission_with_cycle, monkeypatch):
        monkeypatch.chdir(mission_with_cycle)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 1

    def test_detects_cycle_output(self, mission_with_cycle, monkeypatch):
        monkeypatch.chdir(mission_with_cycle)
        result = runner.invoke(app, ["plan", "MF-001"])
        output_lower = result.stdout.lower()
        assert "circular" in output_lower or "cycle" in output_lower

    def test_missing_dependency_exit_code(self, mission_missing_dep, monkeypatch):
        monkeypatch.chdir(mission_missing_dep)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 1

    def test_missing_dependency_names_it(self, mission_missing_dep, monkeypatch):
        monkeypatch.chdir(mission_missing_dep)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert "MF-001-Z" in result.stdout

    def test_missing_parent_mission(self, tmp_path, monkeypatch):
        (tmp_path / ".missionforge" / "missions").mkdir(parents=True)
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["plan", "MF-999"])
        assert result.exit_code == 1

    def test_no_sub_missions_exit_code(self, tmp_path, monkeypatch):
        mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
        mission_dir.mkdir(parents=True)
        (mission_dir / "mission.yaml").write_text(MISSION_YAML)
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 1

    def test_no_sub_missions_suggests_decompose(self, tmp_path, monkeypatch):
        mission_dir = tmp_path / ".missionforge" / "missions" / "MF-001"
        mission_dir.mkdir(parents=True)
        (mission_dir / "mission.yaml").write_text(MISSION_YAML)
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert "No sub-missions" in result.stdout

    def test_invalid_sub_mission_blocks_plan(self, tmp_path, monkeypatch):
        ws = _setup_workspace(tmp_path, {
            "MF-001-A.yaml": SUB_A,
            "MF-001-B.yaml": "id: [\n",
        })
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 1
        assert "Sub-Mission Errors" in result.stdout
        plan_file = ws / ".missionforge" / "missions" / "MF-001" / "plan.yaml"
        assert not plan_file.exists()

    def test_filename_id_mismatch_blocks_plan(self, tmp_path, monkeypatch):
        mismatch = SUB_A.replace("id: MF-001-A", "id: MF-001-B")
        ws = _setup_workspace(tmp_path, {"MF-001-A.yaml": mismatch})
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 1
        assert "does not match" in result.stdout

    def test_duplicate_ids_across_layouts_block_plan(self, tmp_path, monkeypatch):
        ws = _setup_workspace(tmp_path, {"MF-001-A.yaml": SUB_A})
        sub_dir = ws / ".missionforge" / "missions" / "MF-001" / "sub-missions"
        canonical_dir = sub_dir / "MF-001-A"
        canonical_dir.mkdir()
        (canonical_dir / "sub-mission.yaml").write_text(SUB_A)
        monkeypatch.chdir(ws)
        result = runner.invoke(app, ["plan", "MF-001"])
        assert result.exit_code == 1
        assert "Duplicate sub-mission ID" in result.stdout
