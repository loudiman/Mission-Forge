# /mf-validate

Capture or commit validation metrics for a sub-mission.

## Usage
/mf-validate <SUB_MISSION_ID> --capture
/mf-validate <SUB_MISSION_ID> --commit

## Runs
missionforge validate capture $SUB_MISSION_ID
missionforge validate commit $SUB_MISSION_ID

## What Bob Does Next

### After --capture:
- **Read:** `validation.todo.json` to see required metrics
- **Analyze:** Final code state within `allowed_paths`
- **Measure:** Each metric using SAME methods as baseline
- **Fill:** All final metric values in `validation.todo.json`
- **Next command:** `/mf-validate <SUB_ID> --commit`

### After --commit:
- **Read:** `validation.json` to see PASS/FAIL status
- **Review:** Which metrics passed/failed against targets
- **Next command:** 
  - If more sub-missions: `/mf-next <MISSION_ID>` to get next sub-mission
  - If all complete: `missionforge validate parent <MISSION_ID>`

## Example Prompts
- "Validate MF-001-A implementation"
- "Measure final metrics for auth module in MF-001-A"
- "Fill validation metrics and check against targets for MF-001-B"
- "Commit validation after verifying all targets met for MF-001-A"

## Common Issues
- **Issue:** "Metric value missing"
  - **Fix:** Fill all metric values in `validation.todo.json` before commit
- **Issue:** "validation.json already exists"
  - **Fix:** Cannot re-validate; validation is immutable
- **Issue:** "Metric failed to meet target"
  - **Fix:** Review implementation, may need to improve code to meet target
- **Issue:** "Scope violation detected"
  - **Fix:** Modified files outside `allowed_paths`; revert changes
- **Issue:** "Tests failed"
  - **Fix:** Fix failing tests before committing validation