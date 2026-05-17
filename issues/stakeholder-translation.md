# MF-021: Stakeholder Translation

## Priority
**NICE TO HAVE** - Increases polish and judging impact

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- MF-014 (Board Backend) - needs backend structure
- MF-015 (Board Frontend) - needs base UI structure

## Parallel Work
Can work in parallel with MF-020 (Mission Chat)

## Objective
Translate technical mission state into business-friendly summaries using watsonx.ai for non-engineering stakeholders.

## Tasks

### Backend Integration
- [ ] Create endpoint: POST /api/missions/{mission_id}/stakeholder-summary
- [ ] Use watsonx.ai credentials from environment variables
- [ ] Gather mission context (same as Mission Chat)
- [ ] Create system prompt for technical-to-business translation
- [ ] Request structured JSON output with fields:
  - business_summary (one sentence)
  - status (in_progress | complete | at_risk | blocked)
  - percent_complete (0-100)
  - risk_callouts (array of brief risk notes)
  - user_impact (what changes for end users)
- [ ] Cache output until mission state changes
- [ ] Add error handling
- [ ] Add unit tests

### Frontend Integration
- [ ] Add stakeholder view toggle on mission cards
- [ ] Create stakeholder card component with:
  - Business-friendly summary
  - Status indicator with emoji
  - Progress percentage
  - Risk callouts (if any)
  - User impact statement
- [ ] Add stakeholder view toggle in detail panel
- [ ] Style for non-technical audience
- [ ] Add loading and error states

## Acceptance Criteria
- [ ] Endpoint generates business-friendly summaries
- [ ] Summaries are clear and non-technical
- [ ] Status indicators are intuitive
- [ ] Risk callouts are actionable
- [ ] User impact is clearly stated
- [ ] Toggle between technical and stakeholder views works smoothly
- [ ] Caching prevents repeated API calls
- [ ] Latency is acceptable (< 5 seconds)

## Example Stakeholder Summary
```json
{
  "business_summary": "Players in different regions can now find matches without latency spikes.",
  "status": "complete",
  "percent_complete": 100,
  "risk_callouts": [],
  "user_impact": "Faster matchmaking for all players, especially in peak hours."
}
```

## System Prompt Template
```
You are a technical translator. Convert the engineering mission state
below into a business-friendly summary with these fields:

- business_summary: one sentence, plain English, what this delivers
- status: in_progress | complete | at_risk | blocked
- percent_complete: integer 0-100 based on metric progress
- risk_callouts: array of brief risk notes (empty if no risks)
- user_impact: what changes for end users (empty if internal-only)

Return JSON only.
```

## Technical Notes
- Use Granite 3 8B Instruct model
- Cache translations until mission state changes
- Invalidate cache on mission updates
- Target latency: < 5 seconds
- Never commit API credentials

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend Developer + Frontend Developer (requires coordination)
