"""Parent mission validation service."""

import json
import os
import shlex
import stat
from datetime import UTC, datetime
from pathlib import Path

from ..models.schemas import (
    AggregateMetricResult,
    ForbiddenPathsCheck,
    ParentMissionValidation,
    ParentTestResult,
    SubMissionsAggregate,
    SubMissionSummary,
    SubMissionValidation,
)
from ..schemas.validators import SchemaValidator
from ..testing.executor import execute_test_command
from ..utils.path_matching import validate_paths_against_scope
from .exceptions import (
    ParentValidationFailedError,
    ParentValidationIncompleteError,
)
from .workspace import Workspace


class ParentValidationService:
    """Service for parent mission validation."""

    def __init__(self, workspace: Workspace | None = None):
        """Initialize service with workspace."""
        self.workspace = workspace or Workspace()

    def validate_parent_mission(self, mission_id: str) -> Path:
        """Execute complete parent validation flow.

        Args:
            mission_id: Parent mission identifier (e.g., 'MF-001')

        Returns:
            Path to created validation.json

        Raises:
            ParentValidationIncompleteError: Not all sub-missions validated
            ParentValidationFailedError: Validation checks failed
        """
        # Load parent mission definition
        mission_file = self.workspace.mission_path(mission_id) / "mission.yaml"
        parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)

        # Aggregate sub-missions
        sub_missions = self._aggregate_sub_missions(mission_id, parent_mission.sub_missions)

        # Check all sub-missions passed
        if sub_missions.failed > 0 or sub_missions.blocked > 0:
            raise ParentValidationFailedError(
                mission_id,
                f"{sub_missions.failed} sub-mission(s) FAILED, {sub_missions.blocked} BLOCKED",
            )

        # Execute parent test if defined
        parent_test: ParentTestResult | None = None
        if parent_mission.test_command:
            parent_test = self._execute_parent_test(
                parent_mission.test_command, self.workspace.root
            )
            if not parent_test.passed:
                raise ParentValidationFailedError(
                    mission_id, f"Parent test failed (exit code: {parent_test.exit_code})"
                )

        # Validate aggregate metrics if defined
        aggregate_metrics: list[AggregateMetricResult] = []
        if parent_mission.aggregate_metrics:
            aggregate_metrics = self._validate_aggregate_metrics(
                mission_id, parent_mission.aggregate_metrics
            )
            failed_metrics = [m.metric_id for m in aggregate_metrics if m.status == "FAILED"]
            if failed_metrics:
                raise ParentValidationFailedError(
                    mission_id, f"Aggregate metrics failed: {', '.join(failed_metrics)}"
                )

        # Check forbidden paths across all sub-missions
        forbidden_check = self._check_forbidden_paths(
            mission_id, parent_mission.sub_missions, parent_mission.forbidden_paths
        )
        if forbidden_check.violated:
            raise ParentValidationFailedError(
                mission_id, f"Forbidden paths violated: {len(forbidden_check.violations)} file(s)"
            )

        # Determine overall status
        status = self._determine_parent_status(
            sub_missions, parent_test, aggregate_metrics, forbidden_check
        )

        # Create validation result
        validation = ParentMissionValidation(
            mission_id=mission_id,
            timestamp=datetime.now(UTC).isoformat(),
            status=status,
            sub_missions=sub_missions,
            aggregate_metrics=aggregate_metrics,
            parent_test=parent_test,
            forbidden_paths_check=forbidden_check,
        )

        # Write immutable validation.json
        out_path = self.workspace.parent_validation_path(mission_id)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w") as f:
            json.dump(validation.model_dump(mode="json"), f, indent=2)

        # Make file read-only
        os.chmod(out_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        return out_path

    def _aggregate_sub_missions(
        self, mission_id: str, sub_mission_ids: list[str]
    ) -> SubMissionsAggregate:
        """Load and aggregate all sub-mission validation results."""
        details: list[SubMissionSummary] = []
        passed = failed = blocked = 0
        missing: list[str] = []

        for sub_id in sub_mission_ids:
            validation_path = self.workspace.validation_path(sub_id)

            if not validation_path.exists():
                missing.append(sub_id)
                continue

            with open(validation_path) as f:
                data = json.load(f)

            validation = SubMissionValidation(**data)
            status = validation.status

            if status == "PASSED":
                passed += 1
            elif status == "FAILED":
                failed += 1
            elif status == "BLOCKED":
                blocked += 1

            details.append(
                SubMissionSummary(id=sub_id, status=status, timestamp=validation.timestamp)
            )

        if missing:
            raise ParentValidationIncompleteError(mission_id, missing)

        return SubMissionsAggregate(
            total=len(sub_mission_ids),
            passed=passed,
            failed=failed,
            blocked=blocked,
            details=details,
        )

    def _execute_parent_test(self, test_command: str, cwd: Path) -> ParentTestResult:
        """Execute parent-level test command."""
        cmd = shlex.split(test_command)
        result = execute_test_command(cmd, cwd=cwd)

        combined_output = (result.stdout + "\n" + result.stderr).strip()

        return ParentTestResult(
            command=test_command,
            exit_code=result.exit_code,
            output=combined_output,
            passed=result.success,
            duration=round(result.duration, 2),
        )

    def _validate_aggregate_metrics(
        self, mission_id: str, metrics_def: dict
    ) -> list[AggregateMetricResult]:
        """Validate aggregate metrics.

        Note: For now, this is a placeholder. In a full implementation,
        this would prompt Bob to measure metrics. For testing purposes,
        we'll return empty list if no metrics are provided externally.
        """
        # TODO: Implement Bob prompting mechanism for aggregate metrics
        # For now, return empty list - this will be enhanced in future iterations
        return []

    def _check_forbidden_paths(
        self, mission_id: str, sub_mission_ids: list[str], forbidden_paths: list[str]
    ) -> ForbiddenPathsCheck:
        """Check forbidden paths across all sub-missions."""
        if not forbidden_paths:
            return ForbiddenPathsCheck(violated=False, violations=[])

        all_changed_files: list[str] = []

        # Collect all changed files from all sub-missions
        for sub_id in sub_mission_ids:
            validation_path = self.workspace.validation_path(sub_id)

            with open(validation_path) as f:
                data = json.load(f)

            validation = SubMissionValidation(**data)
            all_changed_files.extend(validation.deterministic_evidence.files_changed)

        # Remove duplicates
        all_changed_files = list(set(all_changed_files))

        # Check against forbidden paths
        result = validate_paths_against_scope(
            changed_files=[Path(f) for f in all_changed_files],
            allowed_patterns=[],  # Not checking allowed for parent
            forbidden_patterns=forbidden_paths,
        )

        violations = result["forbidden_files"]

        return ForbiddenPathsCheck(violated=len(violations) > 0, violations=violations)

    def _determine_parent_status(
        self,
        sub_missions: SubMissionsAggregate,
        parent_test: ParentTestResult | None,
        aggregate_metrics: list[AggregateMetricResult],
        forbidden_check: ForbiddenPathsCheck,
    ) -> str:
        """Determine overall parent mission status."""
        # FAILED: Any sub-mission not PASSED
        if sub_missions.failed > 0 or sub_missions.blocked > 0:
            return "FAILED"

        # FAILED: Parent test failed
        if parent_test is not None and not parent_test.passed:
            return "FAILED"

        # FAILED: Any aggregate metric failed
        if any(m.status == "FAILED" for m in aggregate_metrics):
            return "FAILED"

        # FAILED: Forbidden paths violated
        if forbidden_check.violated:
            return "FAILED"

        # PASSED: All checks passed
        return "PASSED"


# Made with Bob
