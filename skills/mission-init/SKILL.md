---
name: mission-init
description: Initialize a new MissionForge mission workspace with the required directory structure and template files.
version: 1.0.0
author: loudiman
triggers:
  - missionforge init
  - initialize mission
  - create mission workspace
  - new mission
---

# mission-init

Initialize a new MissionForge mission workspace. Creates the standard directory structure and template files needed to begin a mission.

## Usage

```bash
missionforge init <MISSION_ID>
# or
missionforge workspace init <MISSION_ID>
```

**Options:**
- `--force` — Overwrite an existing mission workspace

## What It Creates

```
.missionforge/
└── missions/
    └── <MISSION_ID>/
        ├── mission.yaml      # Mission definition (fill this in)
        ├── plan.yaml         # Execution plan
        ├── report.md         # Generated report
        └── sub-missions/     # Sub-mission directory
```

## Mission ID Format

- Parent missions: `[A-Z]{2,4}-\d{3}[A-Z]?` — e.g., `MF-001`, `PROJ-042`, `FG-123A`
- Sub-missions: `[A-Z]{2,4}-\d{3}-[A-Z]` — e.g., `MF-001-A`, `PROJ-042-B`

## Examples

```bash
# Create a new mission workspace
missionforge init MF-001

# Overwrite an existing workspace
missionforge init MF-001 --force

# Using the workspace subcommand
missionforge workspace init PROJ-123
```

## Next Steps

After initializing, edit `mission.yaml` to define your mission, then run:

```bash
missionforge mission MF-001 --validate
```
