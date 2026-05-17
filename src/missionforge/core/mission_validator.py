"""Mission validation adapter for CLI commands."""

from pathlib import Path

from ..schemas import SchemaValidator
from .exceptions import ValidationError as MFValidationError


class MissionValidator:
    """Validates parent mission configuration."""

    def __init__(self) -> None:
        """Initialize validator."""

    def validate_file(self, mission_path: Path) -> tuple[bool, list[str]]:
        """Validate mission.yaml file.

        Args:
            mission_path: Path to mission.yaml file.

        Returns:
            Tuple of (is_valid, error_messages).
        """
        try:
            mission = SchemaValidator.validate_parent_mission_file(mission_path)
        except MFValidationError as e:
            return False, [e.format_error()]

        errors = []
        # test_command is required by the schema, but may be whitespace-only (e.g. "   ");
        # Pydantic accepts non-None strings, so catch semantically empty values here.
        if not mission.test_command or not mission.test_command.strip():
            errors.append("test_command is required")
        errors.extend(self._validate_mission_id_consistency(mission.id, mission_path))

        return len(errors) == 0, errors

    def _validate_mission_id_consistency(self, mission_id: str, mission_path: Path) -> list[str]:
        """Validate mission ID matches directory name.

        Args:
            mission_id: Validated mission ID.
            mission_path: Path to mission.yaml file.

        Returns:
            List of error messages.
        """
        errors: list[str] = []
        expected_id = mission_path.parent.name

        if mission_id != expected_id:
            errors.append(
                f"Mission ID '{mission_id}' does not match directory name '{expected_id}'"
            )
        return errors


# Made with Bob
