# MF-020: Watsonx.ai Mission Chat

## Priority
**NICE TO HAVE** - Increases polish and judging impact

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- MF-014 (Board Backend) - needs backend structure
- MF-016 (Mission Detail Panel) - needs UI to embed chat

## Parallel Work
Can work in parallel with MF-021 (Stakeholder Translation)

## Objective
Allow users to ask questions about mission state from the Board using watsonx.ai for grounded answers.

## Tasks

### Backend Integration
- [ ] Add watsonx.ai credentials via environment variables:
  - IBM_API_KEY
  - WATSONX_PROJECT_ID
  - WATSONX_URL
- [ ] Install ibm-watsonx-ai Python SDK
- [ ] Create endpoint: POST /api/missions/{mission_id}/chat
- [ ] Gather grounding context from:
  - mission.yaml
  - plan.yaml
  - baseline.json files
  - validation.json files
  - report.md
  - git diff summary
- [ ] Create system prompt restricting answers to mission state
- [ ] Implement chat completion call to Granite 3 8B Instruct
- [ ] Add response streaming (optional)
- [ ] Add caching for repeated queries
- [ ] Add error handling for API failures
- [ ] Add unit tests

### Frontend Integration
- [ ] Create chat UI component in mission detail panel
- [ ] Add chat input field
- [ ] Add message history display
- [ ] Add loading indicator
- [ ] Add error states
- [ ] Style chat messages (user vs assistant)
- [ ] Add example questions as suggestions
- [ ] Add clear chat button

## Acceptance Criteria
- [ ] Chat endpoint works with watsonx.ai
- [ ] Responses are grounded in mission state
- [ ] Chat UI is intuitive and responsive
- [ ] Loading states are clear
- [ ] Error handling works gracefully
- [ ] Example questions help users get started
- [ ] Responses are helpful and accurate
- [ ] Latency is acceptable (< 5 seconds)

## Example Questions
- "Why is this mission blocked?"
- "Which files changed?"
- "Why are these two sub-missions independent?"
- "Summarize this mission for a standup update."
- "What is the risk if I lower this metric target?"
- "Explain the matchmaking modernization in plain English."

## System Prompt Template
```
You are a mission assistant for MissionForge. Answer questions about
the mission below using ONLY the provided data. Do not speculate
about code you cannot see. If a question requires reading source
code, say so and suggest the user check with Bob in the IDE.

Mission state:
{mission_context}
```

## Technical Notes
- Use Granite 3 8B Instruct model (ibm/granite-3-8b-instruct)
- Keep context small (few hundred lines) for fast responses
- Cache responses for identical questions
- Add timeout (10 seconds)
- Never commit API credentials to git
- Latency target: < 5 seconds per query

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend Developer + Frontend Developer (requires coordination)
