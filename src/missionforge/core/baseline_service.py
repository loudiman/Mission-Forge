"""Baseline capture and commit service."""

import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..models.schemas import SubMissionBaseline, SubMissionBaselineMetric
from ..schemas.validators import SchemaValidator
from .exceptions import (
    BaselineAlreadyExistsError,
    BaselineIncompleteError,
    BaselineNotCapturedError,
    BaselineValidationError,
)
from .workspace import Workspace


class BaselineService:
    """Service for baseline capture and commit operations."""

    def __init__(self, workspace: Workspace | None = None):
        """Initialize service with workspace.

        Args:
            workspace: Workspace instance. Defaults to current workspace.
        """
        self.workspace = workspace or Workspace()

    def capture_baseline(self, sub_mission_id: str, force: bool = False) -> Path:
        """Capture baseline metrics from sub-mission definition.

        Reads sub-mission.yaml, extracts metric definitions, and creates
        baseline.todo.json with empty values for Bob to fill.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
            force: If True, overwrite existing baseline.json.

        Returns:
            Path to created baseline.todo.json file.

        Raises:
            BaselineAlreadyExistsError: If baseline.json exists and force=False.
            ValidationError: If sub-mission.yaml is invalid.
        """
        # Check if baseline already exists
        baseline_path = self.workspace.baseline_path(sub_mission_id)
        if baseline_path.exists() and not force:
            raise BaselineAlreadyExistsError(sub_mission_id, str(baseline_path))

        # Get sub-mission file path
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        sub_mission_dir = self.workspace.sub_mission_path(parent_id, sub_mission_id)
        sub_mission_file = sub_mission_dir / "sub-mission.yaml"

        # Read and validate sub-mission
        sub_mission = SchemaValidator.validate_sub_mission_file(sub_mission_file)

        # Create baseline metrics from sub-mission metrics
        baseline_metrics: list[SubMissionBaselineMetric] = []
        for metric_id, metric_def in sub_mission.metrics.items():
            # Use target as baseline_target
            if metric_def.target is None:
                raise BaselineValidationError(
                    f"Metric '{metric_id}' in {sub_mission_id} has no target value",
                    "All metrics must have a target value for baseline capture",
                )

            baseline_metric = SubMissionBaselineMetric(
                metric_id=metric_id,
                description=f"Baseline measurement for {metric_id}",
                baseline_target=metric_def.target,
                value=None,  # Bob will fill this
            )
            baseline_metrics.append(baseline_metric)

        # Create baseline with captured status
        baseline = SubMissionBaseline(
            sub_mission_id=sub_mission_id,
            timestamp=None,  # Will be set on commit
            status="captured",
            metrics=baseline_metrics,
        )

        # Write to baseline.todo.json
        todo_path = self.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        with open(todo_path, "w") as f:
            json.dump(baseline.model_dump(mode="json"), f, indent=2)

        return todo_path

    def commit_baseline(self, sub_mission_id: str) -> Path:
        """Commit baseline from baseline.todo.json to immutable baseline.json.

        Validates all metric values are filled and types match, then writes
        to baseline.json with timestamp and makes file read-only.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to created baseline.json file.

        Raises:
            BaselineNotCapturedError: If baseline.todo.json doesn't exist.
            BaselineIncompleteError: If any metric values are None.
            BaselineValidationError: If value types don't match baseline_target types.
        """
        # Check if baseline.todo.json exists
        todo_path = self.workspace.baseline_todo_path(sub_mission_id)
        if not todo_path.exists():
            raise BaselineNotCapturedError(sub_mission_id)

        # Read baseline.todo.json
        with open(todo_path) as f:
            data = json.load(f)

        # Parse into SubMissionBaseline model
        baseline = SubMissionBaseline(**data)

        # Validate all values are filled
        unfilled_metrics: list[str] = []
        for metric in baseline.metrics:
            if metric.value is None:
                unfilled_metrics.append(metric.metric_id)

        if unfilled_metrics:
            raise BaselineIncompleteError(sub_mission_id, unfilled_metrics)

        # Validate value types match baseline_target types
        for metric in baseline.metrics:
            if metric.value is not None:
                target_type = type(metric.baseline_target)
                value_type = type(metric.value)
                
                # Allow numeric type compatibility (int/float are interchangeable)
                # But exclude bool since bool is a subclass of int in Python
                numeric_types = (int, float)
                is_target_numeric = isinstance(metric.baseline_target, numeric_types) and not isinstance(metric.baseline_target, bool)
                is_value_numeric = isinstance(metric.value, numeric_types) and not isinstance(metric.value, bool)
                is_numeric_compatible = is_target_numeric and is_value_numeric
                
                if not is_numeric_compatible and target_type != value_type:
                    raise BaselineValidationError(
                        f"Type mismatch for metric '{metric.metric_id}' in {sub_mission_id}: "
                        f"expected {target_type.__name__}, got {value_type.__name__}",
                        f"Ensure value type matches baseline_target type for {metric.metric_id}",
                    )

        # Add timestamp and update status
        baseline.timestamp = datetime.now(timezone.utc).isoformat()
        baseline.status = "committed"

        # Write to baseline.json
        baseline_path = self.workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)

        with open(baseline_path, "w") as f:
            json.dump(baseline.model_dump(mode="json"), f, indent=2)

        # Make file read-only
        os.chmod(baseline_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        return baseline_path

    def reset_baseline(self, sub_mission_id: str, force: bool = False) -> None:
        """Reset baseline by removing baseline files.

        Removes baseline.todo.json and baseline.json (if force=True).

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
            force: If True, remove read-only baseline.json.

        Raises:
            BaselineValidationError: If no baseline files exist or force required.
        """
        todo_path = self.workspace.baseline_todo_path(sub_mission_id)
        baseline_path = self.workspace.baseline_path(sub_mission_id)

        files_removed = []

        # Remove baseline.todo.json if exists
        if todo_path.exists():
            todo_path.unlink()
            files_removed.append("baseline.todo.json")

        # Remove baseline.json if exists (requires force)
        if baseline_path.exists():
            if not force:
                raise BaselineValidationError(
                    f"Cannot remove committed baseline.json for {sub_mission_id} without --force",
                    "Use --force flag to remove committed baseline",
                )
            # Remove read-only protection before deleting
            os.chmod(baseline_path, stat.S_IRUSR | stat.S_IWUSR)
            baseline_path.unlink()
            files_removed.append("baseline.json")

        # Raise error if no files existed
        if not files_removed:
            raise BaselineValidationError(
                f"No baseline files found for {sub_mission_id}",
                "Baseline has not been captured yet",
            )


# Made with Bob