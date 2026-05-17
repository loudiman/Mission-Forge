# /mf-plan

Generate execution plan with dependency graph resolution.

## Usage
/mf-plan <MISSION_ID>

## Runs
missionforge plan $MISSION_ID

## What Bob Does Next
- **Read:** `plan.yaml` to see execution order and dependencies
- **Review:** Parallelism analysis (which sub-missions can run in parallel)
- **Next command:** `/mf-next <MISSION_ID>` to see which sub-mission to start

## Example Prompts
- "Generate execution plan for MF-001"
- "Create dependency graph and execution order for PROJ-042"
- "Show me the plan for mission MF-003"
- "Resolve dependencies and create plan"

## Common Issues
- **Issue:** "No sub-missions found"
  - **Fix:** Run `/mf-decompose <MISSION_ID>` first to create sub-missions
- **Issue:** "Circular dependency detected"
  - **Fix:** Remove one dependency to break the cycle in sub-mission YAMLs
- **Issue:** "Dependency not found"
  - **Fix:** Ensure all referenced sub-missions exist
- **Issue:** "Invalid parent reference"
  - **Fix:** Check that all sub-missions reference the correct parent ID