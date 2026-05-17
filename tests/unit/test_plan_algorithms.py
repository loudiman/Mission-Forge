# Made with Bob
"""Unit tests for plan command graph algorithms."""

import pytest

from missionforge.cli.commands.plan import (
    _check_all_path_overlaps,
    _compute_parallelism_levels,
    _detect_cycles,
    _topological_sort,
)
from missionforge.models.schemas import SubMission


def _make_sub_mission(sid: str, paths: list[str]) -> SubMission:
    parent = sid.rsplit("-", 1)[0]
    return SubMission(id=sid, parent=parent, title=sid, goal=sid, allowed_paths=paths)


class TestDetectCycles:
    def test_no_cycle_linear(self):
        graph = {"A": ["B"], "B": ["C"], "C": []}
        has_cycle, path = _detect_cycles(graph)
        assert not has_cycle
        assert path == []

    def test_simple_cycle(self):
        graph = {"A": ["B"], "B": ["A"]}
        has_cycle, path = _detect_cycles(graph)
        assert has_cycle
        assert "A" in path and "B" in path

    def test_complex_cycle(self):
        graph = {"A": ["B"], "B": ["C"], "C": ["A"]}
        has_cycle, path = _detect_cycles(graph)
        assert has_cycle
        assert len(path) == 4  # A→B→C→A

    def test_self_loop(self):
        graph = {"A": ["A"]}
        has_cycle, path = _detect_cycles(graph)
        assert has_cycle

    def test_diamond_no_cycle(self):
        graph = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
        has_cycle, path = _detect_cycles(graph)
        assert not has_cycle

    def test_empty_graph(self):
        graph: dict = {}
        has_cycle, path = _detect_cycles(graph)
        assert not has_cycle
        assert path == []

    def test_single_node_no_deps(self):
        graph = {"A": []}
        has_cycle, path = _detect_cycles(graph)
        assert not has_cycle

    def test_disconnected_no_cycle(self):
        graph = {"A": [], "B": [], "C": ["A"]}
        has_cycle, path = _detect_cycles(graph)
        assert not has_cycle


class TestTopologicalSort:
    def test_linear_chain(self):
        graph = {"A": [], "B": ["A"], "C": ["B"]}
        order = _topological_sort(graph)
        assert order == ["A", "B", "C"]

    def test_diamond_pattern(self):
        graph = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
        order = _topological_sort(graph)
        assert order[0] == "A"
        assert order[-1] == "D"
        assert set(order[1:3]) == {"B", "C"}

    def test_parallel_branches(self):
        graph = {"A": [], "B": [], "C": ["A"], "D": ["B"]}
        order = _topological_sort(graph)
        assert set(order[:2]) == {"A", "B"}
        assert set(order[2:]) == {"C", "D"}

    def test_single_node(self):
        graph = {"A": []}
        order = _topological_sort(graph)
        assert order == ["A"]

    def test_empty_graph(self):
        graph: dict = {}
        order = _topological_sort(graph)
        assert order == []

    def test_cycle_raises(self):
        graph = {"A": ["B"], "B": ["A"]}
        with pytest.raises(ValueError, match="[Cc]ycle"):
            _topological_sort(graph)

    def test_deterministic_alphabetical_order(self):
        graph = {"C": [], "A": [], "B": []}
        order = _topological_sort(graph)
        assert order == ["A", "B", "C"]

    def test_dependencies_precede_dependents(self):
        graph = {"Z": [], "A": ["Z"], "M": ["A", "Z"]}
        order = _topological_sort(graph)
        assert order.index("Z") < order.index("A")
        assert order.index("A") < order.index("M")


class TestComputeParallelismLevels:
    def test_linear_chain(self):
        graph = {"A": [], "B": ["A"], "C": ["B"]}
        order = ["A", "B", "C"]
        levels = _compute_parallelism_levels(graph, order)
        assert levels == {0: ["A"], 1: ["B"], 2: ["C"]}

    def test_diamond_pattern(self):
        graph = {"A": [], "B": ["A"], "C": ["A"], "D": ["B", "C"]}
        order = ["A", "B", "C", "D"]
        levels = _compute_parallelism_levels(graph, order)
        assert levels[0] == ["A"]
        assert set(levels[1]) == {"B", "C"}
        assert levels[2] == ["D"]

    def test_all_independent(self):
        graph = {"A": [], "B": [], "C": []}
        order = ["A", "B", "C"]
        levels = _compute_parallelism_levels(graph, order)
        assert levels == {0: ["A", "B", "C"]}

    def test_single_node(self):
        graph = {"A": []}
        order = ["A"]
        levels = _compute_parallelism_levels(graph, order)
        assert levels == {0: ["A"]}

    def test_level_uses_max_dep_depth(self):
        # D depends on both B (depth 1) and C (depth 2), so D should be at depth 3
        graph = {"A": [], "B": ["A"], "C": ["B"], "D": ["B", "C"]}
        order = _topological_sort(graph)
        levels = _compute_parallelism_levels(graph, order)
        assert levels[0] == ["A"]
        assert levels[1] == ["B"]
        assert levels[2] == ["C"]
        assert levels[3] == ["D"]


class TestCheckAllPathOverlaps:
    def test_no_overlap_disjoint_paths(self):
        sms = [
            _make_sub_mission("MF-001-A", ["src/module_a/**"]),
            _make_sub_mission("MF-001-B", ["src/module_b/**"]),
        ]
        assert _check_all_path_overlaps(sms) == []

    def test_symmetric_overlap_detected(self):
        # sm_b's path matches sm_a's glob
        sms = [
            _make_sub_mission("MF-001-A", ["src/shared/**"]),
            _make_sub_mission("MF-001-B", ["src/shared/util.py"]),
        ]
        warnings = _check_all_path_overlaps(sms)
        assert len(warnings) == 1
        assert warnings[0].sub_mission_a == "MF-001-A"
        assert warnings[0].sub_mission_b == "MF-001-B"
        assert warnings[0].overlapping_patterns == ["src/shared/util.py"]

    def test_asymmetric_overlap_detected(self):
        # sm_a has a specific file; sm_b has a broad glob that covers it.
        # The old forward-only check misses this because spec_a.match_file("src/shared/**")
        # is False, but spec_b.match_file("src/shared/config.py") is True.
        sms = [
            _make_sub_mission("MF-001-A", ["src/shared/config.py"]),
            _make_sub_mission("MF-001-B", ["src/shared/**"]),
        ]
        warnings = _check_all_path_overlaps(sms)
        assert len(warnings) == 1
        assert warnings[0].sub_mission_a == "MF-001-A"
        assert warnings[0].sub_mission_b == "MF-001-B"
        assert warnings[0].overlapping_patterns == ["src/shared/config.py"]

    def test_one_warning_per_pair(self):
        # Even if both directions match, only one warning per pair.
        sms = [
            _make_sub_mission("MF-001-A", ["src/**"]),
            _make_sub_mission("MF-001-B", ["src/mod/**"]),
        ]
        warnings = _check_all_path_overlaps(sms)
        assert len(warnings) == 1

    def test_no_paths_skipped(self):
        sms = [
            _make_sub_mission("MF-001-A", []),
            _make_sub_mission("MF-001-B", ["src/module_b/**"]),
        ]
        assert _check_all_path_overlaps(sms) == []

    def test_multiple_pairs_with_overlap(self):
        sms = [
            _make_sub_mission("MF-001-A", ["src/shared/**"]),
            _make_sub_mission("MF-001-B", ["src/shared/x.py"]),
            _make_sub_mission("MF-001-C", ["src/shared/y.py"]),
        ]
        warnings = _check_all_path_overlaps(sms)
        assert len(warnings) == 2
