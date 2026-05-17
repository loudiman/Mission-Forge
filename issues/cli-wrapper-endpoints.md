# MF-019: CLI Wrapper Endpoints

## Priority
**NICE TO HAVE** - Increases polish and judging impact

## Phase
Phase 2 - Mission Board and Watsonx.ai Layer

## Dependencies
- MF-014 (Board Backend) - needs backend structure
- MF-001 through MF-011 (CLI commands must exist)

## Parallel Work
Can work in parallel with frontend issues (MF-015, MF-016, MF-017, MF-018)

## Objective
Allow the Mission Board to trigger selected CLI commands through the backend, keeping the CLI as the source of truth.

## Tasks
- [ ] Add backend endpoint: POST /api/missions/{mission_id}/validate
- [ ] Add backend endpoint: POST /api/missions/{mission_id}/report
- [ ] Add backend endpoint: POST /api/missions/{mission_id}/approve
- [ ] Add backend endpoint: POST /api/missions/refresh
- [ ] Execute CLI commands as subprocesses
- [ ] Capture command stdout and stderr
- [ ] Return structured success/failure responses
- [ ] Add timeout handling for long-running commands
- [ ] Prevent arbitrary shell command execution (security)
- [ ] Add command execution logging
- [ ] Add rate limiting to prevent abuse
- [ ] Add unit tests

## Acceptance Criteria
- [ ] Board can trigger CLI commands via API
- [ ] Command output is captured and returned
- [ ] Success/failure status is clear
- [ ] Timeouts prevent hanging
- [ ] No shell injection vulnerabilities
- [ ] Only safe, whitelisted commands can be executed
- [ ] Rate limiting prevents abuse
- [ ] Error messages are helpful
- [ ] Unit tests cover all endpoints

## API Examples

### POST /api/missions/MF-001/validate
```json
{
  "command": "validate",
  "args": ["--commit"]
}
```

Response:
```json
{
  "success": true,
  "output": "Mission MF-001 validation: PASSED\n...",
  "exit_code": 0,
  "duration_ms": 1234
}
```

## Technical Notes
- Use subprocess module with timeout
- Whitelist allowed commands (validate, report, approve)
- Never use shell=True
- Capture both stdout and stderr
- Add command execution queue for sequential processing
- Log all command executions for audit

## Security Considerations
- Only allow specific CLI commands (no arbitrary execution)
- Validate mission IDs before passing to CLI
- Add authentication if deploying publicly (stretch goal)
- Rate limit to prevent DoS

## Estimated Effort
**2-3 hours** (hackathon pace)

## Developer Assignment
Backend Developer (depends on MF-014)
