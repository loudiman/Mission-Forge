# Decompose Command Documentation

## Overview

The `missionforge decompose` command helps Bob (the AI assistant) break down a parent mission into manageable sub-missions. It provides clear instructions, templates, and validation to ensure a smooth decomposition workflow.

## Commands

### `missionforge decompose <mission-id>`

Initiates the decomposition process for a parent mission.

**What it does:**
1. Validates the parent mission exists and is valid
2. Creates the `sub-missions/` directory structure
3. Displays clear instructions for Bob
4. Shows sub-mission YAML template
5. Provides validation guidance
6. Displays plan.yaml guidance
7. Shows current status of sub-missions

**Example:**
```bash
missionforge decompose MF-001
```

### `missionforge validate-submission <mission-id> <sub-mission-id>`

Validates a specific sub-mission file.

**What it validates:**
- ✓ YAML syntax and schema compliance
- ✓ Sub-mission ID format (e.g., MF-001-A)
- ✓ Parent reference matches mission ID
- ✓ allowed_paths don't conflict with forbidden_paths
- ✓ Dependencies reference valid sub-missions
- ⚠ Warns about overlapping allowed_paths

**Example:**
```bash
missionforge validate-submission MF-001 MF-001-A
```

## Workflow

### Step 1: Validate Parent Mission

Before decomposing, ensure the parent mission is valid:

```bash
missionforge mission MF-001 --validate
```

### Step 2: Run Decompose

Start the decomposition process:

```bash
missionforge decompose MF-001
```

This will:
- Create `.missionforge/missions/MF-001/sub-missions/` directory
- Display instructions and templates
- Show current status

### Step 3: Create Sub-Mission Files

Bob should:
1. Read the codebase to understand the structure
2. Analyze the parent mission goal
3. Break down into logical sub-missions
4. Create YAML files in the sub-missions directory

**File naming convention:**
- `MF-001-A.yaml` - First sub-mission
- `MF-001-B.yaml` - Second sub-mission
- `MF-001-C.yaml` - Third sub-mission
- etc.

### Step 4: Validate Each Sub-Mission

After creating each file, validate it:

```bash
missionforge validate-submission MF-001 MF-001-A
missionforge validate-submission MF-001 MF-001-B
```

### Step 5: Create Execution Plan

Create `plan.yaml` in the mission directory:

```yaml
execution_order:
  - MF-001-A
  - MF-001-B
  - MF-001-C

dependency_graph:
  MF-001-A: []
  MF-001-B: [MF-001-A]
  MF-001-C: [MF-001-A, MF-001-B]
```

### Step 6: Verify Complete Setup

Run decompose again to see the updated status:

```bash
missionforge decompose MF-001
```

## Sub-Mission Template

```yaml
id: MF-001-A
parent: MF-001
title: "Short descriptive title"
goal: "Specific goal for this sub-mission"

# Dependencies (optional)
depends_on:
  - MF-001-B  # This sub-mission depends on B completing first

# Paths this sub-mission can modify
allowed_paths:
  - "src/module_a/**"
  - "tests/test_module_a.py"

# Metrics for this sub-mission (optional)
metrics:
  test_coverage:
    min: 80.0
    target: 90.0
  lines_added:
    max: 500

# Test command (optional, inherits from parent if not specified)
test_command: "pytest tests/test_module_a.py -v"
```

## Validation Rules

### Sub-Mission ID Format

**Pattern:** `^[A-Z]{2,4}-\d{3}-[A-Z]$`

**Valid examples:**
- `MF-001-A`
- `MF-001-B`
- `PROJ-042-Z`

**Invalid examples:**
- `MF-001-AA` (too many letters)
- `MF-001-1` (number instead of letter)
- `MF-001` (missing suffix)

### Parent Reference

The `parent` field must match the parent mission ID exactly:

```yaml
# For sub-mission MF-001-A
parent: MF-001  # ✓ Correct

parent: MF-002  # ✗ Wrong - doesn't match ID prefix
```

### Allowed Paths

**Rules:**
1. Must not conflict with parent's `forbidden_paths`
2. Should not overlap with other sub-missions (warning)
3. Use gitignore-style glob patterns

**Examples:**
```yaml
allowed_paths:
  - "src/feature_a/**"           # All files in feature_a
  - "tests/test_feature_a.py"    # Specific test file
  - "docs/feature_a.md"          # Documentation
  - "!src/feature_a/legacy/**"   # Exclude legacy code
```

### Dependencies

**Rules:**
1. Dependencies must reference valid sub-mission IDs
2. No circular dependencies allowed
3. Dependencies must exist before validation passes

**Example:**
```yaml
# MF-001-C depends on both A and B
depends_on:
  - MF-001-A
  - MF-001-B
```

## Common Issues

### Issue: "Invalid sub-mission ID format"

**Cause:** Sub-mission ID doesn't match the required pattern.

**Solution:** Ensure ID follows `PARENT-LETTER` format:
```yaml
# Wrong
id: MF-001-AB

# Correct
id: MF-001-A
```

### Issue: "Parent mismatch"

**Cause:** Parent field doesn't match the mission ID.

**Solution:** Update parent to match:
```yaml
# For MF-001-A
parent: MF-001  # Must match the prefix
```

### Issue: "Path conflicts with forbidden paths"

**Cause:** Sub-mission tries to modify forbidden paths.

**Solution:** Remove conflicting paths from `allowed_paths` or adjust parent's `forbidden_paths`.

### Issue: "Missing dependencies"

**Cause:** Sub-mission depends on non-existent sub-missions.

**Solution:** Create the dependency first or remove it from `depends_on`.

### Issue: "Overlapping allowed_paths"

**Cause:** Multiple sub-missions can modify the same files.

**Solution:** Refine the path patterns to avoid overlap:
```yaml
# Sub-mission A
allowed_paths:
  - "src/module_a/**"

# Sub-mission B
allowed_paths:
  - "src/module_b/**"  # Different module
```

## Best Practices

### 1. Logical Decomposition

Break missions into logical, independent units:
- ✓ By feature/module
- ✓ By layer (frontend/backend)
- ✓ By concern (data/logic/UI)

### 2. Clear Dependencies

Define dependencies explicitly:
```yaml
# Backend must complete before frontend
depends_on:
  - MF-001-A  # Backend API
```

### 3. Non-Overlapping Paths

Keep sub-missions independent:
```yaml
# Good - separate modules
MF-001-A: ["src/auth/**"]
MF-001-B: ["src/api/**"]

# Bad - overlapping
MF-001-A: ["src/**"]
MF-001-B: ["src/api/**"]  # Overlaps with A
```

### 4. Meaningful Metrics

Set realistic metrics:
```yaml
metrics:
  test_coverage:
    min: 80.0      # Minimum acceptable
    target: 90.0   # Ideal goal
  lines_added:
    max: 500       # Keep changes manageable
```

### 5. Validate Frequently

Validate after each file creation:
```bash
# Create file
vim .missionforge/missions/MF-001/sub-missions/MF-001-A.yaml

# Validate immediately
missionforge validate-submission MF-001 MF-001-A
```

## Integration with Other Commands

### Before Decompose
```bash
# 1. Initialize mission
missionforge init MF-001

# 2. Edit mission.yaml
vim .missionforge/missions/MF-001/mission.yaml

# 3. Validate parent
missionforge mission MF-001 --validate

# 4. Decompose
missionforge decompose MF-001
```

### After Decompose
```bash
# 1. Create sub-missions (Bob's work)
# 2. Validate each sub-mission
# 3. Create plan.yaml
# 4. Execute sub-missions (future feature)
```

## Output Examples

### Successful Decompose

```
Step 1: Validating parent mission MF-001...
✓ Parent mission is valid

Step 2: Setting up sub-missions directory...
✓ Created: .missionforge/missions/MF-001/sub-missions

Step 3: Create sub-mission files
┌─ 📋 Decomposition Guide ─────────────────────────┐
│ Instructions for Bob:                            │
│                                                  │
│ 1. Read the codebase to understand structure    │
│ 2. Analyze the parent goal: ...                 │
│ 3. Break down into logical sub-missions         │
│ ...                                              │
└──────────────────────────────────────────────────┘

[Template and guidance displayed...]

✓ Setup Complete
Decomposition workspace ready!
```

### Successful Validation

```
Validating: .missionforge/missions/MF-001/sub-missions/MF-001-A.yaml

✓ YAML syntax and schema valid
✓ ID format valid: MF-001-A
✓ Parent reference correct: MF-001
✓ No conflicts with forbidden paths
✓ All dependencies exist: MF-001-B

┌─ ✓ Validation Success ───────────────────────────┐
│ ✓ Sub-mission MF-001-A is valid!                │
└──────────────────────────────────────────────────┘
```

### Validation Errors

```
Validating: .missionforge/missions/MF-001/sub-missions/MF-001-A.yaml

✓ YAML syntax and schema valid
✗ Invalid sub-mission ID format: MF-001-AA
  Expected pattern: MF-001-[A-Z] (e.g., MF-001-A)

┌─ Validation Errors ──────────────────────────────┐
│ ✗ Validation failed                              │
│                                                  │
│ • Invalid sub-mission ID format: MF-001-AA       │
│   Expected pattern: MF-001-[A-Z] (e.g., MF-001-A)│
└──────────────────────────────────────────────────┘
```

## Technical Implementation

### File Structure
```
.missionforge/
└── missions/
    └── MF-001/
        ├── mission.yaml          # Parent mission
        ├── plan.yaml            # Execution plan
        └── sub-missions/        # Sub-missions directory
            ├── MF-001-A.yaml    # First sub-mission
            ├── MF-001-B.yaml    # Second sub-mission
            └── MF-001-C.yaml    # Third sub-mission
```

### Validation Flow
1. Load parent mission
2. Validate sub-mission schema
3. Check ID format with regex
4. Verify parent reference
5. Check forbidden paths
6. Validate dependencies
7. Warn about overlaps

### Path Conflict Detection
Uses `pathspec` library to match gitignore-style patterns:
```python
import pathspec

# Check if path matches forbidden pattern
forbidden_spec = pathspec.PathSpec.from_lines("gitignore", forbidden_paths)
if forbidden_spec.match_file(allowed_path):
    # Conflict detected
```

## Future Enhancements

- [ ] Auto-generate sub-missions using AI
- [ ] Interactive decomposition wizard
- [ ] Dependency graph visualization
- [ ] Automatic path conflict resolution
- [ ] Sub-mission execution tracking
- [ ] Progress reporting across sub-missions

## See Also

- [Mission Schema Documentation](schemas/mission-schema-examples.md)
- [Workspace Commands](../README.md#workspace-commands)
- [Validation Commands](../README.md#validation-commands)

---

**Made with Bob** 🤖