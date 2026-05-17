# /mf-next

Show next ready sub-mission to work on.

## Usage
/mf-next <MISSION_ID>

## Runs
missionforge plan $MISSION_ID

## What Bob Does Next
- **Read:** Output showing next ready sub-mission(s)
- **Review:** Parallelism levels (Level 0 = ready, Level 1+ = blocked)
- **Next command:** `/mf-baseline <SUB_ID> --capture` for the next ready sub-mission

## Example Prompts
- "What's the next sub-mission to work on for MF-001?"
- "Show me which sub-missions are ready to start in PROJ-042"
- "Which sub-mission should I implement next?"
- "Display ready sub-missions for MF-003"

## Common Issues
- **Issue:** "No plan found"
  - **Fix:** Run `/mf-plan <MISSION_ID>` first to generate execution plan
- **Issue:** "All sub-missions blocked"
  - **Fix:** Check if any sub-missions have been completed; may need to start with Level 0
- **Issue:** "Sub-mission already completed"
  - **Fix:** Move to the next sub-mission in the execution order