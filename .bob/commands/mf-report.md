# /mf-report

Generate final mission report with evidence summary.

## Usage
/mf-report <MISSION_ID>

## Runs
missionforge plan $MISSION_ID

## What Bob Does Next
- **Read:** `report.md` to see mission completion evidence
- **Review:** All sub-mission results and aggregate metrics
- **Confirm:** Mission objectives achieved
- **Done:** Mission complete! 🎉

## Example Prompts
- "Generate final report for MF-001"
- "Show me the mission completion evidence for PROJ-042"
- "Create report for completed mission MF-003"
- "Display mission results and metrics"

## Common Issues
- **Issue:** "Parent validation not complete"
  - **Fix:** Run `missionforge validate parent <MISSION_ID>` first
- **Issue:** "Not all sub-missions validated"
  - **Fix:** Complete validation for all sub-missions before generating report
- **Issue:** "Report not found"
  - **Fix:** Ensure parent validation has been run successfully