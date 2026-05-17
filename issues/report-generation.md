# MF-011: Evidence Report Generation

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-010 (Parent Validation) - needs validation results to report

## Parallel Work
Cannot start until MF-010 completes

## Objective
Generate PR-ready Markdown evidence report summarizing the completed mission with all sub-mission results, metrics, and test evidence.

## Tasks
- [ ] Implement `missionforge report <mission-id>` command
- [ ] Create Markdown report template using Jinja2
- [ ] Include in report:
  - Mission goal and status
  - Decomposition summary with dependency diagram
  - Sub-mission results table
  - Baseline vs final metrics comparison
  - Aggregate metrics results
  - Test results (parent and all sub-missions)
  - Files changed summary
  - Forbidden path violations (if any)
  - Next suggested mission (if available)
- [ ] Generate report.md in mission directory
- [ ] Format report for readability (tables, code blocks, status indicators)
- [ ] Add option to output to stdout or custom path
- [ ] Include timestamps and metadata
- [ ] Make report suitable for PR attachment
- [ ] Add unit tests for template rendering
- [ ] Add integration tests

## Acceptance Criteria
- [ ] Report contains all required sections
- [ ] Markdown formatting is clean and readable
- [ ] Tables render correctly
- [ ] Status indicators are clear (✓ PASS, ✗ FAIL)
- [ ] Dependency diagram is included (ASCII or Mermaid)
- [ ] Report is suitable for PR attachment
- [ ] Report is suitable as judging artifact
- [ ] Can generate report even if mission failed (shows what failed)
- [ ] Integration tests verify complete report generation

## Example Report Structure
```markdown
# Mission MF-001: Matchmaking Modernization

## Status: PASSED

## Goal
Modernize matchmaking from CORBA to REST...

## Decomposition
```
MF-001-A ───┬─── MF-001-B ───┐
            │                 │
            └─── MF-001-C ────┴─── MF-001-D
```

## Sub-Mission Results
| ID | Title | Status | Metrics | Tests |
|---|---|---|---|---|
| MF-001-A | REST Endpoint | ✓ PASSED | 2/2 | ✓ |
...

## Aggregate Metrics
| Metric | Baseline | Target | Final | Status |
|---|---|---|---|---|
| corba_refs_in_matchmaking | 7 | 0 | 0 | ✓ PASSED |

## Files Changed
- server/src/rest/MatchmakingEndpoint.java
- client-java/src/.../MatchmakingClient.java
...

## Next Mission
MF-002: Modernize game state synchronization
```

## Technical Notes
- Use Jinja2 for templating
- Support both ASCII and Mermaid diagram formats
- Include git diff summary (file list, not full diff)
- Add metadata: generation timestamp, CLI version
- Make template extensible for future enhancements

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (depends on MF-010)
