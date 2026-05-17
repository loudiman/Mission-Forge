# /mf-mission

Validate a parent mission configuration file.

## Usage
/mf-mission <MISSION_ID> --validate

## Runs
missionforge mission $MISSION_ID --validate

## What Bob Does Next
- **Read:** Validation errors (if any)
- **Fix:** Edit `mission.yaml` to fix validation errors
- **Next command:** `/mf-decompose <MISSION_ID>` (after validation passes)

## Example Prompts
- "Validate mission MF-001 configuration"
- "Check if mission.yaml is properly formatted for PROJ-042"
- "Fix validation errors in parent mission MF-003"

## Common Issues
- **Issue:** "Mission not found"
  - **Fix:** Run `/mf-init <MISSION_ID>` first
- **Issue:** "Invalid YAML syntax"
  - **Fix:** Check YAML formatting, ensure proper indentation
- **Issue:** "Required field missing"
  - **Fix:** Add missing fields (title, goal, test_command, etc.)
- **Issue:** "Invalid glob pattern"
  - **Fix:** Use valid gitignore-style patterns in allowed_paths/forbidden_paths