"""Validation capture and commit service."""

import json
import os
import shlex
import stat
from datetime import UTC, datetime
from pathlib import Path

from ..git.operations import get_changed_files, get_repo_root, get_status
from ..models.schemas import (
    DeterministicEvidence,
    ScopeCheckResult,
    SubMissionValidation,
    TestResults,
    ValidationMetric,
)
from ..schemas.validators import SchemaValidator
from ..testing.executor import execute_test_command
from ..utils.path_matching import validate_paths_against_scope
from .exceptions import (
    GitOperationError,
    ValidationAlreadyExistsError,
    ValidationIncompleteError,
    ValidationNotCapturedError,
)
from .workspace import Workspace


class ValidationService:
    """Service for sub-mission validation capture and commit."""

    def __init__(self, workspace: Workspace | None = None):
        self.workspace = workspace or Workspace()

    def capture_validation(self, sub_mission_id: str, force: bool = False) -> Path:
        """Capture deterministic evidence and create validation.todo.json.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
            force: If True, overwrite existing validation.json.

        Returns:
            Path to created validation.todo.json.
        """
        validation_path = self.workspace.validation_path(sub_mission_id)
        if validation_path.exists():
            if not force:
                raise ValidationAlreadyExistsError(sub_mission_id, str(validation_path))
            os.chmod(validation_path, stat.S_IRUSR | stat.S_IWUSR)
            validation_path.unlink()

        parent_id = sub_mission_id.rsplit("-", 1)[0]
        sub_mission_file = self.workspace.sub_mission_definition_path(parent_id, sub_mission_id)
        sub_mission = SchemaValidator.validate_sub_mission_file(sub_mission_file)

        # Load baseline values for each metric
        baseline_values: dict[str, object] = {}
        baseline_file = self.workspace.baseline_path(sub_mission_id)
        if baseline_file.exists():
            with open(baseline_file) as f:
                baseline_data = json.load(f)
            for m in baseline_data.get("metrics", []):
                baseline_values[m["metric_id"]] = m.get("value")

        # Get changed files via git status (staged + unstaged)
        try:
            repo_root = get_repo_root(cwd=self.workspace.root)
            status = get_status(cwd=repo_root)
            all_changed = list({*status.staged, *status.unstaged, *status.untracked})
        except GitOperationError:
            all_changed = []

        # Also include diff vs HEAD
        try:
            diff_files = get_changed_files(base_ref="HEAD", cwd=self.workspace.root)
            for f in diff_files:
                if f not in all_changed:
                    all_changed.append(f)
        except GitOperationError:
            pass

        files_changed = [str(f) for f in all_changed]

        # Load parent mission forbidden_paths
        mission_file = self.workspace.mission_path(parent_id) / "mission.yaml"
        forbidden_paths: list[str] = []
        if mission_file.exists():
            parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)
            forbidden_paths = parent_mission.forbidden_paths

        # Scope validation
        scope_result = validate_paths_against_scope(
            changed_files=all_changed,
            allowed_patterns=sub_mission.allowed_paths,
            forbidden_patterns=forbidden_paths,
        )

        violations: list[str] = scope_result["forbidden_files"] + scope_result["out_of_scope_files"]
        scope_check = ScopeCheckResult(
            allowed_paths_satisfied=len(scope_result["out_of_scope_files"]) == 0,
            forbidden_paths_violated=len(scope_result["forbidden_files"]) > 0,
            violations=violations,
        )

        # Execute test command if defined
        test_results: TestResults | None = None
        if sub_mission.test_command:
            cmd = shlex.split(sub_mission.test_command)
            result = execute_test_command(cmd, cwd=self.workspace.root)
            combined_output = (result.stdout + "\n" + result.stderr).strip()
            test_results = TestResults(
                command=sub_mission.test_command,
                exit_code=result.exit_code,
                output=combined_output,
                passed=result.success,
                duration=round(result.duration, 2),
            )

        evidence = DeterministicEvidence(
            files_changed=files_changed,
            scope_check=scope_check,
            test_results=test_results,
        )

        # Build metrics list from sub-mission definition
        metrics: list[ValidationMetric] = []
        for metric_id, metric_def in sub_mission.metrics.items():
            metrics.append(
                ValidationMetric(
                    metric_id=metric_id,
                    baseline_value=baseline_values.get(metric_id),
                    target_value=metric_def.target,  # type: ignore[arg-type]
                    final_value=None,
                    status=None,
                )
            )

        validation = SubMissionValidation(
            sub_mission_id=sub_mission_id,
            timestamp=None,
            status="captured",
            deterministic_evidence=evidence,
            metrics=metrics,
        )

        todo_path = self.workspace.validation_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        with open(todo_path, "w") as f:
            json.dump(validation.model_dump(mode="json"), f, indent=2)

        return todo_path

    def commit_validation(self, sub_mission_id: str) -> Path:
        """Validate metrics and write immutable validation.json.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to created validation.json.
        """
        todo_path = self.workspace.validation_todo_path(sub_mission_id)
        if not todo_path.exists():
            raise ValidationNotCapturedError(sub_mission_id)

        with open(todo_path) as f:
            data = json.load(f)

        validation = SubMissionValidation(**data)

        # Check all final_values are filled
        unfilled = [m.metric_id for m in validation.metrics if m.final_value is None]
        if unfilled:
            raise ValidationIncompleteError(sub_mission_id, unfilled)

        # Determine per-metric status
        for metric in validation.metrics:
            metric.status = self._determine_metric_status(metric)

        # Determine overall status
        validation.status = self._determine_overall_status(validation)
        validation.timestamp = datetime.now(UTC).isoformat()

        out_path = self.workspace.validation_path(sub_mission_id)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w") as f:
            json.dump(validation.model_dump(mode="json"), f, indent=2)

        os.chmod(out_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        return out_path

    def _determine_metric_status(self, metric: ValidationMetric) -> str:
        """Determine PASSED/FAILED for a single metric."""
        final = metric.final_value
        target = metric.target_value
        baseline = metric.baseline_value

        # Boolean or string: exact match
        if isinstance(target, bool) or isinstance(target, str):
            return "PASSED" if final == target else "FAILED"

        # Numeric comparison
        try:
            f_val = float(final)  # type: ignore[arg-type]
            t_val = float(target)
        except (TypeError, ValueError):
            return "FAILED"

        # No baseline: pass if final meets or exceeds target (improvement direction)
        if baseline is None:
            return "PASSED" if f_val >= t_val else "FAILED"

        try:
            b_val = float(baseline)
        except (TypeError, ValueError):
            return "PASSED" if f_val >= t_val else "FAILED"

        if t_val > b_val:
            return "PASSED" if f_val >= t_val else "FAILED"
        elif t_val < b_val:
            return "PASSED" if f_val <= t_val else "FAILED"
        else:
            return "PASSED" if f_val == t_val else "FAILED"

    def _determine_overall_status(self, validation: SubMissionValidation) -> str:
        """Determine overall PASSED/FAILED/BLOCKED status."""
        evidence = validation.deterministic_evidence

        # BLOCKED: scope violations or test failures
        if (
            evidence.scope_check.forbidden_paths_violated
            or not evidence.scope_check.allowed_paths_satisfied
        ):
            return "BLOCKED"
        if evidence.test_results is not None and not evidence.test_results.passed:
            return "BLOCKED"

        # FAILED: any metric failed
        if any(m.status == "FAILED" for m in validation.metrics):
            return "FAILED"

        return "PASSED"


# Made with Bob
