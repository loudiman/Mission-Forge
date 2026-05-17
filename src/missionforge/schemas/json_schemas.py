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

# JSON Schema for sub-mission baseline.todo.json (value can be null)
SUB_MISSION_BASELINE_TODO_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sub-Mission Baseline TODO",
    "description": "Baseline metrics template for Bob to fill",
    "type": "object",
    "required": ["sub_mission_id", "metrics"],
    "properties": {
        "sub_mission_id": {
            "type": "string",
            "pattern": "^[A-Z]{2,4}-\\d{3}-[A-Z]$",
            "description": "Sub-mission identifier",
            "examples": ["MF-001-A", "FG-042-B"],
        },
        "metrics": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["metric_id", "description", "baseline_target", "value"],
                "properties": {
                    "metric_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Unique identifier for the metric",
                    },
                    "description": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Human-readable description of what is measured",
                    },
                    "baseline_target": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "Expected baseline value before implementation",
                    },
                    "value": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                            {"type": "null"},
                        ],
                        "description": "Actual measured value (null until filled by Bob)",
                    },
                },
            },
        },
    },
}

# JSON Schema for sub-mission baseline.json (value must be filled)
SUB_MISSION_BASELINE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sub-Mission Baseline",
    "description": "Committed baseline metrics for sub-mission",
    "type": "object",
    "required": ["sub_mission_id", "timestamp", "status", "metrics"],
    "properties": {
        "sub_mission_id": {
            "type": "string",
            "pattern": "^[A-Z]{2,4}-\\d{3}-[A-Z]$",
            "description": "Sub-mission identifier",
            "examples": ["MF-001-A", "FG-042-B"],
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp when baseline was committed",
        },
        "status": {
            "type": "string",
            "enum": ["captured", "committed"],
            "description": "Baseline status",
        },
        "metrics": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["metric_id", "description", "baseline_target", "value"],
                "properties": {
                    "metric_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Unique identifier for the metric",
                    },
                    "description": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Human-readable description of what is measured",
                    },
                    "baseline_target": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "Expected baseline value before implementation",
                    },
                    "value": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "Actual measured value (must be filled)",
                    },
                },
            },
        },
    },
}


def get_sub_mission_baseline_todo_schema() -> dict[str, Any]:
    """Get sub-mission baseline TODO JSON schema.

    Returns:
        JSON schema for baseline.todo.json files.
    """
    return SUB_MISSION_BASELINE_TODO_SCHEMA


def get_sub_mission_baseline_schema() -> dict[str, Any]:
    """Get sub-mission baseline JSON schema.

    Returns:
        JSON schema for baseline.json files.
    """
    return SUB_MISSION_BASELINE_SCHEMA



# Made with Bob
