"""JSON Schema definitions for validation files."""

from typing import Any

# JSON Schema for baseline.json and baseline.todo.json
BASELINE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Mission Baseline",
    "description": "Baseline metrics captured before mission execution",
    "type": "object",
    "required": ["mission_id", "timestamp", "git_commit", "metrics"],
    "properties": {
        "mission_id": {
            "type": "string",
            "pattern": "^[A-Z]{2,4}-\\d{3}(-[A-Z])?$",
            "description": "Mission or sub-mission identifier",
            "examples": ["MF-001", "MF-001-A"],
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp of baseline capture",
        },
        "git_commit": {
            "type": "string",
            "pattern": "^[0-9a-f]{7,40}$",
            "description": "Git commit hash at baseline",
        },
        "metrics": {
            "type": "object",
            "required": ["files_changed", "lines_added", "lines_removed"],
            "properties": {
                "files_changed": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of files changed",
                },
                "lines_added": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of lines added",
                },
                "lines_removed": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of lines removed",
                },
                "test_coverage": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Test coverage percentage",
                },
                "custom_metrics": {
                    "type": "object",
                    "additionalProperties": {"type": "number"},
                    "description": "Custom metrics defined by mission",
                },
            },
        },
    },
}

# JSON Schema for validation.json and validation.todo.json
VALIDATION_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Mission Validation",
    "description": "Validation results after mission execution",
    "type": "object",
    "required": ["mission_id", "timestamp", "git_commit", "metrics", "passed"],
    "properties": {
        "mission_id": {
            "type": "string",
            "pattern": "^[A-Z]{2,4}-\\d{3}(-[A-Z])?$",
            "description": "Mission or sub-mission identifier",
            "examples": ["MF-001", "MF-001-A"],
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp of validation",
        },
        "git_commit": {
            "type": "string",
            "pattern": "^[0-9a-f]{7,40}$",
            "description": "Git commit hash at validation",
        },
        "metrics": {
            "type": "object",
            "required": ["files_changed", "lines_added", "lines_removed", "tests_passed"],
            "properties": {
                "files_changed": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of files changed",
                },
                "lines_added": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of lines added",
                },
                "lines_removed": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of lines removed",
                },
                "test_coverage": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Test coverage percentage",
                },
                "tests_passed": {
                    "type": "boolean",
                    "description": "Whether all tests passed",
                },
                "custom_metrics": {
                    "type": "object",
                    "additionalProperties": {"type": "number"},
                    "description": "Custom metrics defined by mission",
                },
            },
        },
        "passed": {
            "type": "boolean",
            "description": "Whether validation passed all checks",
        },
        "errors": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Validation errors if any",
        },
    },
}


def validate_json_against_schema(data: dict[str, Any], schema: dict[str, Any]) -> None:
    """Validate JSON data against a schema.

    Args:
        data: JSON data to validate.
        schema: JSON schema to validate against.

    Raises:
        jsonschema.ValidationError: If validation fails.
    """
    import jsonschema  # type: ignore[import-untyped]

    jsonschema.validate(instance=data, schema=schema)


def get_baseline_schema() -> dict[str, Any]:
    """Get baseline JSON schema.

    Returns:
        JSON schema for baseline files.
    """
    return BASELINE_SCHEMA


def get_validation_schema() -> dict[str, Any]:
    """Get validation JSON schema.

    Returns:
        JSON schema for validation files.
    """
    return VALIDATION_SCHEMA


# Made with Bob
