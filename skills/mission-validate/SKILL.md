---
name: mission-validate
description: Validate a mission.yaml file for correct structure, required fields, and constraint compliance.
version: 1.0.0
author: loudiman
triggers:
  - missionforge validate
  - validate mission
  - mission validate
  - check mission yaml
---

# mission-validate

Validate a `mission.yaml` file against the MissionForge schema. Catches structural errors, missing required fields, invalid glob patterns, and ID inconsistencies before decomposition.

## Usage

```bash
# Validate a parent mission
missionforge mission <MISSION_ID> --validate

# Validate a specific sub-mission file
missionforge validate-submission <MISSION_ID> <SUB_MISSION_ID>
```

## What Gets Checked

**Parent mission (`mission.yaml`):**
- YAML syntax is valid
- All required fields are present (`id`, `title`, `description`, `test_command`, etc.)
- Mission ID format matches the directory name
- Glob patterns in `allowed_paths` / `forbidden_paths` are syntactically valid
- `aggregate_metrics` structure is correct
- `test_command` is specified

**Sub-mission (`validate-submission`):**
- Sub-mission ID format (e.g., `MF-001-A`)
- `parent_id` references the correct parent
- No forbidden path conflicts
- Declared dependencies exist
- Path overlap warnings across sibling sub-missions

## Examples

```bash
# Validate parent mission MF-001
missionforge mission MF-001 --validate

# Validate sub-mission MF-001-A within MF-001
missionforge validate-submission MF-001 MF-001-A
```

## Exit Codes

- `0` — Validation passed
- `1` — Validation failed (errors printed to console)
