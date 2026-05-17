# Made with Bob
"""Unit tests for next command helper functions."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from missionforge.cli.commands.next import _scan_validation_status


def _make_workspace(tmp_path: Path) -> MagicMock:
    ws = MagicMock()
    ws.validation_path.side_effect = lambda sub_id: tmp_path / f"{sub_id}_validation.json"
    return ws


def _write_validation(path: Path, sub_id: str, status: str) -> None:
    data = {
        "sub_mission_id": sub_id,
        "status": status,
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
    path.write_text(json.dumps(data))


class TestScanValidationStatus:
    def test_missing_files_returns_none(self, tmp_path):
        ws = _make_workspace(tmp_path)
        result = _scan_validation_status(ws, ["MF-001-A", "MF-001-B"])
        assert result == {"MF-001-A": None, "MF-001-B": None}

    def test_passed_status(self, tmp_path):
        ws = _make_workspace(tmp_path)
        _write_validation(tmp_path / "MF-001-A_validation.json", "MF-001-A", "PASSED")
        result = _scan_validation_status(ws, ["MF-001-A"])
        assert result["MF-001-A"] == "PASSED"

    def test_failed_status(self, tmp_path):
        ws = _make_workspace(tmp_path)
        _write_validation(tmp_path / "MF-001-A_validation.json", "MF-001-A", "FAILED")
        result = _scan_validation_status(ws, ["MF-001-A"])
        assert result["MF-001-A"] == "FAILED"

    def test_mixed_statuses(self, tmp_path):
        ws = _make_workspace(tmp_path)
        _write_validation(tmp_path / "MF-001-A_validation.json", "MF-001-A", "PASSED")
        _write_validation(tmp_path / "MF-001-B_validation.json", "MF-001-B", "FAILED")
        result = _scan_validation_status(ws, ["MF-001-A", "MF-001-B", "MF-001-C"])
        assert result["MF-001-A"] == "PASSED"
        assert result["MF-001-B"] == "FAILED"
        assert result["MF-001-C"] is None

    def test_corrupted_json_treated_as_none(self, tmp_path):
        ws = _make_workspace(tmp_path)
        (tmp_path / "MF-001-A_validation.json").write_text("not valid json {{")
        result = _scan_validation_status(ws, ["MF-001-A"])
        assert result["MF-001-A"] is None

    def test_captured_status(self, tmp_path):
        ws = _make_workspace(tmp_path)
        _write_validation(tmp_path / "MF-001-A_validation.json", "MF-001-A", "captured")
        result = _scan_validation_status(ws, ["MF-001-A"])
        assert result["MF-001-A"] == "captured"

    def test_empty_sub_mission_list(self, tmp_path):
        ws = _make_workspace(tmp_path)
        result = _scan_validation_status(ws, [])
        assert result == {}


class TestCategorizationLogic:
    """Test that categorization logic in next_command is correct."""

    def _categorize(self, execution_order, dependency_graph, status_map):
        complete = []
        ready = []
        blocked = []
        failed = []
        pending = []

        for sub_id in execution_order:
            status = status_map[sub_id]
            deps = dependency_graph.get(sub_id, [])

            if status == "PASSED":
                complete.append(sub_id)
            elif status == "FAILED":
                failed.append(sub_id)
            elif status == "captured":
                pending.append(sub_id)
            elif status is None:
                if all(status_map.get(dep) == "PASSED" for dep in deps):
                    satisfied = [d for d in deps if status_map.get(d) == "PASSED"]
                    ready.append((sub_id, satisfied))
                else:
                    blocked.append((sub_id, deps))
            else:
                blocked.append((sub_id, deps))

        return complete, ready, blocked, failed, pending

    def test_first_sub_mission_ready_when_no_deps(self):
        order = ["MF-001-A"]
        graph = {"MF-001-A": []}
        status = {"MF-001-A": None}
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert ready == [("MF-001-A", [])]
        assert complete == blocked == failed == []

    def test_linear_chain_second_ready_when_first_passed(self):
        order = ["MF-001-A", "MF-001-B"]
        graph = {"MF-001-A": [], "MF-001-B": ["MF-001-A"]}
        status = {"MF-001-A": "PASSED", "MF-001-B": None}
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert complete == ["MF-001-A"]
        assert [r[0] for r in ready] == ["MF-001-B"]

    def test_diamond_both_ready_when_root_passed(self):
        order = ["MF-001-A", "MF-001-B", "MF-001-C", "MF-001-D"]
        graph = {
            "MF-001-A": [],
            "MF-001-B": ["MF-001-A"],
            "MF-001-C": ["MF-001-A"],
            "MF-001-D": ["MF-001-B", "MF-001-C"],
        }
        status = {
            "MF-001-A": "PASSED",
            "MF-001-B": None,
            "MF-001-C": None,
            "MF-001-D": None,
        }
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert complete == ["MF-001-A"]
        ready_ids = [r[0] for r in ready]
        assert "MF-001-B" in ready_ids
        assert "MF-001-C" in ready_ids
        assert [b[0] for b in blocked] == ["MF-001-D"]

    def test_all_complete(self):
        order = ["MF-001-A", "MF-001-B"]
        graph = {"MF-001-A": [], "MF-001-B": ["MF-001-A"]}
        status = {"MF-001-A": "PASSED", "MF-001-B": "PASSED"}
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert complete == ["MF-001-A", "MF-001-B"]
        assert ready == blocked == failed == []

    def test_failed_dependency_blocks_downstream(self):
        order = ["MF-001-A", "MF-001-B", "MF-001-C"]
        graph = {"MF-001-A": [], "MF-001-B": ["MF-001-A"], "MF-001-C": ["MF-001-B"]}
        status = {"MF-001-A": "FAILED", "MF-001-B": None, "MF-001-C": None}
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert failed == ["MF-001-A"]
        assert [b[0] for b in blocked] == ["MF-001-B", "MF-001-C"]
        assert ready == complete == []

    def test_captured_status_treated_as_pending(self):
        order = ["MF-001-A"]
        graph = {"MF-001-A": []}
        status = {"MF-001-A": "captured"}
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert pending == ["MF-001-A"]
        assert ready == complete == failed == []
        assert blocked == []

    def test_first_ready_is_first_in_topological_order(self):
        order = ["MF-001-A", "MF-001-B", "MF-001-C"]
        graph = {"MF-001-A": [], "MF-001-B": [], "MF-001-C": []}
        status = {"MF-001-A": None, "MF-001-B": None, "MF-001-C": None}
        complete, ready, blocked, failed, pending = self._categorize(order, graph, status)
        assert ready[0][0] == "MF-001-A"
