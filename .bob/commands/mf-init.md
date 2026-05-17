# /mf-init

Initialize a new mission workspace.

## Usage
/mf-init <MISSION_ID>

## Runs
missionforge init $MISSION_ID

## What Bob Does Next
- **Read:** `.missionforge/missions/<MISSION_ID>/mission.yaml`
- **Edit:** Fill in mission details (title, goal, test_command, etc.)
- **Next command:** `/mf-mission <MISSION_ID> --validate`

## Example Prompts
- "Initialize mission MF-001 for REST API migration"
- "Create new mission PROJ-042 for authentication refactor"
- "Set up mission workspace for database migration MF-003"

## Common Issues
- **Issue:** "Mission already exists"
  - **Fix:** Use `--force` flag to overwrite: `missionforge init MF-001 --force`
- **Issue:** "Invalid mission ID format"
  - **Fix:** Use format `[A-Z]{2,4}-\d{3}[A-Z]?` (e.g., `MF-001`, `PROJ-042A`)