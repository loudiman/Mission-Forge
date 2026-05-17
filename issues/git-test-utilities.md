# MF-003: Git and Test Execution Utilities

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation) - needs base CLI structure

## Parallel Work
Can work in parallel with MF-002 (Schemas) after MF-001 is complete

## Objective
Implement git operations and test command execution utilities that the CLI uses for validation and evidence capture.

## Tasks
- [ ] Implement git diff wrapper to identify changed files
- [ ] Implement git status wrapper for workspace state
- [ ] Add file path comparison against allowed/forbidden globs
- [ ] Implement test command execution via subprocess
- [ ] Capture test command stdout/stderr
- [ ] Capture test command exit code
- [ ] Add timeout handling for long-running tests
- [ ] Implement safe subprocess execution (no shell injection)
- [ ] Add git repository detection and validation
- [ ] Create utility for checking if paths match glob patterns
- [ ] Add unit tests for all utilities

## Acceptance Criteria
- [ ] Git diff correctly identifies changed files since last commit
- [ ] Path matching works with glob patterns (**, *, etc.)
- [ ] Test commands execute safely in subprocess
- [ ] Test output is captured completely
- [ ] Exit codes are correctly reported
- [ ] Timeouts prevent hanging on long tests
- [ ] No shell injection vulnerabilities
- [ ] Works from any subdirectory in repo
- [ ] Unit test coverage > 80%

## Technical Notes
- Use subprocess module, NOT os.system or shell=True
- Git operations via subprocess calls to system git (no GitPython)
- Use pathlib.Path for path operations
- Glob matching should support ** (recursive) and * (single level)
- Consider using fnmatch or pathspec for glob matching
- Test execution should stream output for long-running commands

## Estimated Effort
**2-3 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (can work independently from MF-002)
