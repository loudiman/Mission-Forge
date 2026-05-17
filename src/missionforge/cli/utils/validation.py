"""Input validation utilities for CLI."""

import re


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


# Made with Bob
