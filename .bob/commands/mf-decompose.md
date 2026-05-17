# /mf-decompose

Decompose a parent mission into sub-missions with guided workflow.

## Usage
/mf-decompose <MISSION_ID>

## Runs
missionforge decompose $MISSION_ID

## What Bob Does Next
- **Read:** Decomposition instructions and template
- **Analyze:** Codebase structure to understand scope
- **Create:** Sub-mission YAML files in `sub-missions/` directory
  - `MF-001-A.yaml`, `MF-001-B.yaml`, etc.
- **Validate:** Each sub-mission with `missionforge validate-submission <MISSION_ID> <SUB_ID>`
- **Next command:** `/mf-plan <MISSION_ID>` (after all sub-missions validated)

## Example Prompts
- "Decompose MF-001 into sub-missions for auth, data, and UI layers"
- "Break down the migration into logical sub-missions for PROJ-042"
- "Create sub-missions for MF-003 based on module structure"
- "Analyze codebase and create 3-5 sub-missions for the refactor"

## Common Issues
- **Issue:** "Parent mission not validated"
  - **Fix:** Run `/mf-mission <MISSION_ID> --validate` first
- **Issue:** "Sub-mission validation failed"
  - **Fix:** Check ID format, parent reference, and path conflicts
- **Issue:** "Overlapping allowed_paths"
  - **Fix:** Refine path patterns to avoid overlap between sub-missions
- **Issue:** "Circular dependencies"
  - **Fix:** Remove one dependency to break the cycle