"""Input validation utilities for CLI."""

import re
from pathlib import Path
from typing import Optional

from ...models.schemas import ParentMission, SubMission
from ...schemas.validators import SchemaValidator


def validate_mission_id(mission_id: str) -> bool:
    """Validate mission ID format.

    Mission IDs must match pattern: [A-Z]{2,4}-\\d{3}[A-Z]?
    Examples: MF-001, FG-042A, PROJ-123

    Args:
        mission_id: Mission identifier to validate.

    Returns:
        True if valid, False otherwise.
    """
    pattern = r"^[A-Z]{2,4}-\d{3}[A-Z]?$"
    return bool(re.match(pattern, mission_id))


def validate_sub_mission_id(sub_mission_id: str) -> bool:
    """Validate sub-mission ID format.

    Sub-mission IDs must match pattern: [A-Z]{2,4}-\\d{3}-[A-Z]
    Examples: MF-001-A, FG-042-B

    Args:
        sub_mission_id: Sub-mission identifier to validate.

    Returns:
        True if valid, False otherwise.
    """
    pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
    return bool(re.match(pattern, sub_mission_id))


def extract_parent_mission_id(sub_mission_id: str) -> str:
    """Extract parent mission ID from sub-mission ID.

    Args:
        sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

    Returns:
        Parent mission ID (e.g., 'MF-001').
    """
    # Remove the last part after the last hyphen
    parts = sub_mission_id.rsplit("-", 1)
    return parts[0] if len(parts) > 1 else sub_mission_id


def load_and_validate_mission(mission_file: Path) -> ParentMission:
    """Load and validate a parent mission file.

    Args:
        mission_file: Path to mission.yaml file.

    Returns:
        Validated ParentMission instance.

    Raises:
        ValidationError: If validation fails.
    """
    return SchemaValidator.validate_parent_mission_file(mission_file)


def load_and_validate_sub_mission(sub_mission_file: Path) -> SubMission:
    """Load and validate a sub-mission file.

    Args:
        sub_mission_file: Path to sub-mission YAML file.

    Returns:
        Validated SubMission instance.

    Raises:
        ValidationError: If validation fails.
    """
    return SchemaValidator.validate_sub_mission_file(sub_mission_file)


def validate_mission_structure(mission_path: Path) -> dict:
    """Validate complete mission directory structure.

    Args:
        mission_path: Path to mission directory.

    Returns:
        Dictionary with validation results.

    Raises:
        ValidationError: If critical validation fails.
    """
    return SchemaValidator.validate_mission_structure(mission_path)


# Made with Bob
