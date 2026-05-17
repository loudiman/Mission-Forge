"""Schema validators for mission files."""

# ruff: noqa: B904

import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]
from pydantic import ValidationError

from ..core.exceptions import ValidationError as MFValidationError
from ..models.schemas import (
    Baseline,
    ExecutionPlan,
    ParentMission,
    SubMission,
    Validation,
)


class SchemaValidator:
    """Validates mission schemas and files."""

    @staticmethod
    def validate_parent_mission_file(file_path: Path) -> ParentMission:
        """Validate parent mission YAML file.

        Args:
            file_path: Path to mission.yaml file.

        Returns:
            Validated ParentMission instance.

        Raises:
            MFValidationError: If validation fails.
        """
        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)

            if not data:
                raise MFValidationError(
                    f"Empty or invalid YAML file: {file_path}",
                    "Ensure the file contains valid YAML content",
                )

            return ParentMission(**data)

        except FileNotFoundError:
            raise MFValidationError(
                f"Mission file not found: {file_path}",
                "Create the mission file using 'missionforge workspace init'",
            )
        except yaml.YAMLError as e:
            raise MFValidationError(
                f"Invalid YAML syntax in {file_path}: {e}",
                "Check YAML syntax - ensure proper indentation and structure",
            )
        except ValidationError as e:
            errors = SchemaValidator._format_pydantic_errors(e)
            raise MFValidationError(
                f"Mission validation failed for {file_path}:\n{errors}",
                "Fix the validation errors listed above",
            )
        except Exception as e:
            raise MFValidationError(
                f"Unexpected error validating {file_path}: {e}",
                "Check file format and content",
            )

    @staticmethod
    def validate_sub_mission_file(file_path: Path) -> SubMission:
        """Validate sub-mission YAML file.

        Args:
            file_path: Path to sub-mission YAML file.

        Returns:
            Validated SubMission instance.

        Raises:
            MFValidationError: If validation fails.
        """
        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)

            if not data:
                raise MFValidationError(
                    f"Empty or invalid YAML file: {file_path}",
                    "Ensure the file contains valid YAML content",
                )

            return SubMission(**data)

        except FileNotFoundError:
            raise MFValidationError(
                f"Sub-mission file not found: {file_path}",
                "Create the sub-mission file first",
            )
        except yaml.YAMLError as e:
            raise MFValidationError(
                f"Invalid YAML syntax in {file_path}: {e}",
                "Check YAML syntax - ensure proper indentation and structure",
            )
        except ValidationError as e:
            errors = SchemaValidator._format_pydantic_errors(e)
            raise MFValidationError(
                f"Sub-mission validation failed for {file_path}:\n{errors}",
                "Fix the validation errors listed above",
            )
        except Exception as e:
            raise MFValidationError(
                f"Unexpected error validating {file_path}: {e}",
                "Check file format and content",
            )

    @staticmethod
    def validate_baseline_file(file_path: Path) -> Baseline:
        """Validate baseline JSON file.

        Args:
            file_path: Path to baseline.json or baseline.todo.json file.

        Returns:
            Validated Baseline instance.

        Raises:
            MFValidationError: If validation fails.
        """
        try:
            with open(file_path) as f:
                data = json.load(f)

            return Baseline(**data)

        except FileNotFoundError:
            raise MFValidationError(
                f"Baseline file not found: {file_path}",
                "Capture baseline using 'missionforge baseline capture'",
            )
        except json.JSONDecodeError as e:
            raise MFValidationError(
                f"Invalid JSON syntax in {file_path}: {e}",
                "Check JSON syntax - ensure proper formatting",
            )
        except ValidationError as e:
            errors = SchemaValidator._format_pydantic_errors(e)
            raise MFValidationError(
                f"Baseline validation failed for {file_path}:\n{errors}",
                "Fix the validation errors listed above",
            )
        except Exception as e:
            raise MFValidationError(
                f"Unexpected error validating {file_path}: {e}",
                "Check file format and content",
            )

    @staticmethod
    def validate_validation_file(file_path: Path) -> Validation:
        """Validate validation JSON file.

        Args:
            file_path: Path to validation.json or validation.todo.json file.

        Returns:
            Validated Validation instance.

        Raises:
            MFValidationError: If validation fails.
        """
        try:
            with open(file_path) as f:
                data = json.load(f)

            return Validation(**data)

        except FileNotFoundError:
            raise MFValidationError(
                f"Validation file not found: {file_path}",
                "Run validation using 'missionforge validate'",
            )
        except json.JSONDecodeError as e:
            raise MFValidationError(
                f"Invalid JSON syntax in {file_path}: {e}",
                "Check JSON syntax - ensure proper formatting",
            )
        except ValidationError as e:
            errors = SchemaValidator._format_pydantic_errors(e)
            raise MFValidationError(
                f"Validation file validation failed for {file_path}:\n{errors}",
                "Fix the validation errors listed above",
            )
        except Exception as e:
            raise MFValidationError(
                f"Unexpected error validating {file_path}: {e}",
                "Check file format and content",
            )

    @staticmethod
    def validate_plan_file(file_path: Path) -> ExecutionPlan:
        """Validate execution plan YAML file.

        Args:
            file_path: Path to plan.yaml file.

        Returns:
            Validated ExecutionPlan instance.

        Raises:
            MFValidationError: If validation fails.
        """
        try:
            with open(file_path) as f:
                data = yaml.safe_load(f)

            if not data:
                raise MFValidationError(
                    f"Empty or invalid YAML file: {file_path}",
                    "Ensure the file contains valid YAML content",
                )

            return ExecutionPlan(**data)

        except FileNotFoundError:
            raise MFValidationError(
                f"Plan file not found: {file_path}",
                "Generate plan using 'missionforge plan generate'",
            )
        except yaml.YAMLError as e:
            raise MFValidationError(
                f"Invalid YAML syntax in {file_path}: {e}",
                "Check YAML syntax - ensure proper indentation and structure",
            )
        except ValidationError as e:
            errors = SchemaValidator._format_pydantic_errors(e)
            raise MFValidationError(
                f"Plan validation failed for {file_path}:\n{errors}",
                "Fix the validation errors listed above",
            )
        except Exception as e:
            raise MFValidationError(
                f"Unexpected error validating {file_path}: {e}",
                "Check file format and content",
            )

    @staticmethod
    def validate_sub_mission_dependencies(
        sub_mission: SubMission, available_missions: list[str]
    ) -> None:
        """Validate that sub-mission dependencies exist.

        Args:
            sub_mission: SubMission to validate.
            available_missions: List of available sub-mission IDs.

        Raises:
            MFValidationError: If dependencies are invalid.
        """
        missing_deps = []
        for dep in sub_mission.depends_on:
            if dep not in available_missions:
                missing_deps.append(dep)

        if missing_deps:
            raise MFValidationError(
                f"Sub-mission '{sub_mission.id}' has missing dependencies: {', '.join(missing_deps)}",
                f"Ensure these sub-missions exist: {', '.join(missing_deps)}",
            )

    @staticmethod
    def validate_forbidden_paths(
        parent_mission: ParentMission, sub_mission: SubMission
    ) -> None:
        """Validate that sub-mission paths don't conflict with forbidden paths.

        Args:
            parent_mission: Parent mission with forbidden paths.
            sub_mission: Sub-mission to validate.

        Raises:
            MFValidationError: If paths conflict.
        """
        import pathspec

        if not parent_mission.forbidden_paths:
            return

        forbidden_spec = pathspec.PathSpec.from_lines("gitignore", parent_mission.forbidden_paths)

        conflicts = []
        for allowed_path in sub_mission.allowed_paths:
            # Check if allowed path matches any forbidden pattern
            if forbidden_spec.match_file(allowed_path):
                conflicts.append(allowed_path)

        if conflicts:
            raise MFValidationError(
                f"Sub-mission '{sub_mission.id}' has paths that conflict with "
                f"forbidden paths: {', '.join(conflicts)}",
                "Remove these paths from allowed_paths or adjust forbidden_paths in parent mission",
            )

    @staticmethod
    def _format_pydantic_errors(error: ValidationError) -> str:
        """Format Pydantic validation errors into readable message.

        Args:
            error: Pydantic ValidationError.

        Returns:
            Formatted error message.
        """
        errors = []
        for err in error.errors():
            loc = " -> ".join(str(x) for x in err["loc"])
            msg = err["msg"]
            errors.append(f"  • {loc}: {msg}")

        return "\n".join(errors)

    @staticmethod
    def validate_mission_structure(mission_path: Path) -> dict[str, Any]:
        """Validate complete mission directory structure.

        Args:
            mission_path: Path to mission directory.

        Returns:
            Dictionary with validation results.

        Raises:
            MFValidationError: If critical validation fails.
        """
        results: dict[str, Any] = {
            "mission_file": False,
            "plan_file": False,
            "sub_missions": [],
            "errors": [],
            "warnings": [],
        }

        # Check mission.yaml
        mission_file = mission_path / "mission.yaml"
        if not mission_file.exists():
            results["errors"].append(f"Missing mission.yaml in {mission_path}")
            raise MFValidationError(
                f"Mission file not found: {mission_file}",
                "Create mission.yaml file",
            )

        try:
            parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)
            results["mission_file"] = True
        except MFValidationError as e:
            results["errors"].append(str(e))
            raise

        # Check plan.yaml
        plan_file = mission_path / "plan.yaml"
        if plan_file.exists():
            try:
                SchemaValidator.validate_plan_file(plan_file)
                results["plan_file"] = True
            except MFValidationError as e:
                results["warnings"].append(f"Plan file validation failed: {e}")
        else:
            results["warnings"].append("No plan.yaml found")

        # Check sub-missions
        sub_missions_dir = mission_path / "sub-missions"
        if sub_missions_dir.exists():
            available_missions = []
            for sub_file in sub_missions_dir.glob("*.yaml"):
                try:
                    sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
                    available_missions.append(sub_mission.id)
                    results["sub_missions"].append(sub_mission.id)

                    # Validate parent relationship
                    if sub_mission.parent != parent_mission.id:
                        results["errors"].append(
                            f"Sub-mission {sub_mission.id} parent mismatch: "
                            f"expected {parent_mission.id}, got {sub_mission.parent}"
                        )

                    # Validate forbidden paths
                    try:
                        SchemaValidator.validate_forbidden_paths(parent_mission, sub_mission)
                    except MFValidationError as e:
                        results["errors"].append(str(e))

                except MFValidationError as e:
                    results["errors"].append(f"Sub-mission {sub_file.name}: {e}")

            # Validate dependencies
            for sub_file in sub_missions_dir.glob("*.yaml"):
                try:
                    sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
                    SchemaValidator.validate_sub_mission_dependencies(
                        sub_mission, available_missions
                    )
                except MFValidationError as e:
                    results["errors"].append(str(e))

        return results


# Made with Bob
