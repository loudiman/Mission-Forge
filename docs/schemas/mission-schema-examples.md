# Mission Schema Examples

This document provides examples of all mission schema formats used in MissionForge.

## Parent Mission Schema (mission.yaml)

```yaml
# Mission: MF-001
id: MF-001
goal: |
  Modernize the matchmaking service from CORBA to REST API
  while maintaining backward compatibility and game stability.

# Paths that sub-missions cannot modify
forbidden_paths:
  - "core/**"
  - "config/production/**"
  - "tests/integration/**"

# Aggregate metrics to validate across all sub-missions
aggregate_metrics:
  total_files_changed:
    max: 50
  total_lines_changed:
    max: 1000
  test_coverage:
    min: 80.0

# Test command to validate mission completion
test_command: "pytest tests/ --cov=src"

# Sub-missions will be listed here after decomposition
sub_missions:
  - MF-001-A
  - MF-001-B
  - MF-001-C
```

## Sub-Mission Schema (sub-missions/MF-001-A.yaml)

```yaml
# Sub-mission: MF-001-A
id: MF-001-A
parent: MF-001
title: "Extract CORBA interface definitions"
goal: |
  Extract and document all CORBA interface definitions
  from the matchmaking service for REST API design.

# Dependencies on other sub-missions
depends_on: []

# Paths this sub-mission can modify
allowed_paths:
  - "src/matchmaking/interfaces/**"
  - "docs/api/**"

# Metrics for this sub-mission
metrics:
  files_changed:
    max: 10
  lines_added:
    max: 500
  test_coverage:
    min: 85.0

# Test command for this sub-mission
test_command: "pytest tests/unit/matchmaking/interfaces/"
```

## Baseline Schema (baseline.json)

```json
{
  "mission_id": "MF-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "git_commit": "abc123def456789",
  "metrics": {
    "files_changed": 0,
    "lines_added": 0,
    "lines_removed": 0,
    "test_coverage": 78.5,
    "custom_metrics": {
      "cyclomatic_complexity": 42.0,
      "code_duplication": 5.2
    }
  }
}
```

## Validation Schema (validation.json)

```json
{
  "mission_id": "MF-001",
  "timestamp": "2024-01-20T15:45:00Z",
  "git_commit": "def789abc123456",
  "metrics": {
    "files_changed": 15,
    "lines_added": 450,
    "lines_removed": 120,
    "test_coverage": 85.2,
    "tests_passed": true,
    "custom_metrics": {
      "cyclomatic_complexity": 38.0,
      "code_duplication": 3.8
    }
  },
  "passed": true,
  "errors": []
}
```

## Execution Plan Schema (plan.yaml)

```yaml
# Execution plan for MF-001
execution_order:
  - MF-001-A
  - MF-001-B
  - MF-001-C

# Dependency graph
dependency_graph:
  MF-001-A: []
  MF-001-B: [MF-001-A]
  MF-001-C: [MF-001-A, MF-001-B]
```

## Mission ID Format Rules

### Parent Mission IDs
- Pattern: `[A-Z]{2,4}-\d{3}[A-Z]?`
- Examples:
  - `MF-001` - Standard format
  - `PROJ-123` - 4-letter prefix
  - `FG-042A` - With optional suffix letter

### Sub-Mission IDs
- Pattern: `[A-Z]{2,4}-\d{3}-[A-Z]`
- Examples:
  - `MF-001-A` - First sub-mission
  - `MF-001-B` - Second sub-mission
  - `PROJ-123-Z` - Last sub-mission

## Metric Definition Format

Metrics can have the following constraints:

```yaml
metric_name:
  min: 0.0        # Minimum allowed value (optional)
  max: 100.0      # Maximum allowed value (optional)
  target: 85.0    # Target value (optional)
```

At least one constraint (min, max, or target) must be specified.

## Path Pattern Format

Path patterns use gitignore-style glob patterns:

- `**` - Matches any number of directories
- `*` - Matches any characters except `/`
- `?` - Matches a single character
- `[abc]` - Matches any character in the set

Examples:
- `src/**/*.py` - All Python files in src and subdirectories
- `tests/unit/**` - All files in tests/unit and subdirectories
- `*.yaml` - All YAML files in current directory
- `config/[!p]*` - Config files not starting with 'p'

## Validation Rules

### Required Fields

**Parent Mission:**
- `id` - Mission identifier
- `goal` - Mission goal description

**Sub-Mission:**
- `id` - Sub-mission identifier
- `parent` - Parent mission ID
- `title` - Short descriptive title
- `goal` - Sub-mission goal description

**Baseline/Validation:**
- `mission_id` - Mission or sub-mission ID
- `timestamp` - ISO 8601 timestamp
- `git_commit` - Git commit hash
- `metrics` - Metrics object

### Validation Checks

1. **ID Format** - Mission and sub-mission IDs must match required patterns
2. **Parent-Child Relationship** - Sub-mission ID must match parent ID
3. **Path Patterns** - All path patterns must be valid glob patterns
4. **Forbidden Paths** - Sub-mission paths cannot conflict with forbidden paths
5. **Dependencies** - All dependencies must reference existing sub-missions
6. **Circular Dependencies** - Execution plan cannot have circular dependencies
7. **Metric Constraints** - Min cannot be greater than max

## Error Messages

The validators provide clear, actionable error messages:

```
❌ Mission validation failed for .missionforge/missions/MF-001/mission.yaml:
  • id: Invalid mission ID format: MF001. Must match pattern: [A-Z]{2,4}-\d{3}[A-Z]? (e.g., MF-001, FG-042A)
💡 Suggestion: Fix the validation errors listed above
```

```
❌ Sub-mission 'MF-001-B' has missing dependencies: MF-001-C
💡 Suggestion: Ensure these sub-missions exist: MF-001-C
```

```
❌ Sub-mission 'MF-001-A' has paths that conflict with forbidden paths: core/config.py
💡 Suggestion: Remove these paths from allowed_paths or adjust forbidden_paths in parent mission
```

# Made with Bob