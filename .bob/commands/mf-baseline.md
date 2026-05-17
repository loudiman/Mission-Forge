# /mf-baseline

Capture or commit baseline metrics for a sub-mission.

## Usage
/mf-baseline <SUB_MISSION_ID> --capture
/mf-baseline <SUB_MISSION_ID> --commit

## Runs
missionforge baseline capture $SUB_MISSION_ID
missionforge baseline commit $SUB_MISSION_ID

## What Bob Does Next

### After --capture:
- **Read:** `baseline.todo.json` to see required metrics
- **Analyze:** Code within `allowed_paths` from sub-mission YAML
- **Measure:** Each metric using appropriate tools (coverage, line counts, etc.)
- **Fill:** All metric values in `baseline.todo.json`
- **Next command:** `/mf-baseline <SUB_ID> --commit`

### After --commit:
- **Read:** `baseline.json` to verify committed values
- **Implement:** Make code changes within `allowed_paths`
- **Next command:** `/mf-validate <SUB_ID> --capture` (after implementation)

## Example Prompts
- "Capture baseline for MF-001-A"
- "Measure current test coverage for auth module in MF-001-A"
- "Fill baseline metrics for sub-mission MF-001-B"
- "Commit baseline after filling all metrics for MF-001-A"

## Common Issues
- **Issue:** "Metric value missing"
  - **Fix:** Fill all metric values in `baseline.todo.json` before commit
- **Issue:** "baseline.json already exists"
  - **Fix:** Use `missionforge baseline reset <SUB_ID> --force` to reset
- **Issue:** "baseline.json is immutable"
  - **Fix:** Cannot modify after commit; use reset if needed
- **Issue:** "Cannot measure metric"
  - **Fix:** Check SKILL.md metric measurement guide for tools and methods