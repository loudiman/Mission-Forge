---
name: baseline-capture
description: Capture and commit pre-implementation baseline metrics for a sub-mission to enable measurable success tracking.
version: 1.0.0
author: loudiman
triggers:
  - missionforge baseline
  - capture baseline
  - baseline capture
  - commit baseline
  - baseline metrics
---

# baseline-capture

Captures the current state of metrics defined in a sub-mission before implementation begins. Creates an immutable snapshot used to measure success against targets.

## Two-Step Workflow

### Step 1 — Capture

```bash
missionforge baseline capture <SUB_MISSION_ID>
```

Generates `baseline.todo.json` from the sub-mission's `metrics` definitions. Each metric is listed with its type (`bool`, `int`, `float`) and needs a measured value filled in.

**Output:**
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • test_coverage (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

### Step 2 — Fill & Commit

Manually edit `baseline.todo.json` with measured values, then commit:

```bash
missionforge baseline commit <SUB_MISSION_ID>
```

Produces an **immutable** `baseline.json`. Once committed, the baseline cannot be changed without `--force`.

## Additional Commands

```bash
# Overwrite an existing baseline.todo.json
missionforge baseline capture MF-001-A --force

# Reset baseline to allow re-capture (requires --force for committed baselines)
missionforge baseline reset MF-001-A --force
```

## File Locations

| File | Path | Mutable |
|------|------|---------|
| `baseline.todo.json` | `.missionforge/missions/<PARENT>/sub-missions/<ID>/` | Yes |
| `baseline.json` | Same directory | No (immutable after commit) |

## Why Baselines Matter

Baselines lock in the pre-implementation state so that post-implementation metrics can be compared against concrete starting points — not estimates. Without a committed baseline, success targets cannot be verified.
