---
name: mission-decompose
description: Decompose a validated parent mission into sub-missions with guided scaffolding, templates, and validation.
version: 1.0.0
author: loudiman
triggers:
  - missionforge decompose
  - decompose mission
  - break down mission
  - split mission into sub-missions
---

# mission-decompose

Guided workflow for decomposing a parent mission into independently-executable sub-missions. Validates the parent, scaffolds the sub-mission directory, displays templates, and provides step-by-step instructions.

## Usage

```bash
missionforge decompose <MISSION_ID>
```

## What It Does

1. **Validates** the parent `mission.yaml` — aborts on errors
2. **Creates** the `sub-missions/` directory structure if it doesn't exist
3. **Displays** sub-mission YAML templates with the correct ID format
4. **Guides** you through filling in each sub-mission file
5. **Validates** each sub-mission as it's created
6. **Provides** `plan.yaml` guidance for sequencing

## Sub-Mission ID Format

```
<PARENT_ID>-<LETTER>
# e.g., MF-001-A, MF-001-B, MF-001-C
```

## Example

```bash
# Decompose parent mission MF-001
missionforge decompose MF-001
```

After decomposing, validate individual sub-missions:

```bash
missionforge validate-submission MF-001 MF-001-A
missionforge validate-submission MF-001 MF-001-B
```

## Sub-Mission YAML Template

```yaml
id: MF-001-A
parent_id: MF-001
title: "Sub-mission title"
description: "What this sub-mission accomplishes"
allowed_paths:
  - "src/module/**"
forbidden_paths: []
dependencies: []
metrics:
  - metric_id: example_metric
    baseline_target: 0
    success_target: 1
    metric_type: int
```

## Related Commands

- `missionforge baseline capture <SUB_MISSION_ID>` — capture baseline metrics after decomposing
- `missionforge plan <MISSION_ID>` — generate an execution plan
