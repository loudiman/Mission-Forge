# MF-013: Demo Mission Preparation

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 through MF-012 (all CLI functionality must be complete)
- Demo codebase (Boggle game with CORBA backend)

## Parallel Work
Can work independently once CLI is complete

## Objective
Prepare the first end-to-end modernization mission for the hackathon demo using the Boggle game codebase.

## Tasks

### Pre-Demo Validation
- [ ] Confirm Boggle game runs end-to-end:
  - Java Swing client connects and plays
  - Python TUI client connects and plays
  - Both clients can play against each other
  - CORBA backend handles matchmaking correctly
- [ ] Verify matchmaking is reasonably isolated from game logic
- [ ] Manually attempt the matchmaking modernization to confirm feasibility
- [ ] Identify potential issues before recording

### Mission Definition
- [ ] Write parent mission.yaml for matchmaking modernization
- [ ] Define clear goal statement
- [ ] Define forbidden_paths (game logic, scoring, session management)
- [ ] Define aggregate_metrics:
  - CORBA references in matchmaking (baseline: N, target: 0)
  - In-game CORBA flow still works (baseline: true, target: true)
- [ ] Define parent test_command (integration tests)
- [ ] Validate mission.yaml with CLI

### Test Infrastructure
- [ ] Write or verify integration tests for matchmaking flow
- [ ] Ensure tests cover both clients (Swing + Python)
- [ ] Ensure tests can run via command line
- [ ] Verify test output is clear and parseable
- [ ] Add regression tests for non-matchmaking CORBA flows

### REST Endpoint Design
- [ ] Design REST endpoint shape for matchmaking
- [ ] Document expected request/response format
- [ ] Ensure design matches existing CORBA IDL operations
- [ ] Plan delegation strategy (REST → CORBA initially)

### Dry Run
- [ ] Run complete mission flow manually:
  - Initialize mission
  - Decompose (manually create sub-missions)
  - Plan dependency graph
  - Execute each sub-mission
  - Validate results
  - Generate report
- [ ] Identify and fix any workflow issues
- [ ] Adjust scope if mission is too large
- [ ] Document any CLI improvements needed

### Recording Preparation
- [ ] Prepare clean git state
- [ ] Set up screen recording environment
- [ ] Prepare terminal windows and layouts
- [ ] Test Bob session flow
- [ ] Estimate Bobcoin cost (target: 6-9 Bobcoins)
- [ ] Create recording checklist

## Acceptance Criteria
- [ ] Boggle game runs reliably end-to-end
- [ ] Matchmaking modernization is manually achievable
- [ ] Parent mission.yaml is complete and validated
- [ ] Integration tests exist and pass
- [ ] REST endpoint design is documented
- [ ] Dry run completes successfully
- [ ] Recording environment is ready
- [ ] Team is confident in demo execution

## Demo Mission Scope
**Goal**: Modernize matchmaking from CORBA to REST while preserving multiplayer functionality across both clients.

**Sub-missions** (expected):
- MF-001-A: Add REST endpoint for matchmaking
- MF-001-B: Migrate Swing client to REST matchmaking
- MF-001-C: Migrate Python client to REST matchmaking
- MF-001-D: Add dual-client REST matchmaking integration test

**Dependency structure**: Diamond pattern (A → B,C → D)

## Technical Notes
- Matchmaking should be one CORBA operation (or small set)
- Keep scope tight - one operation, not entire matchmaking module
- Ensure forbidden paths are meaningful (prove scope held)
- Integration test is the key validation artifact

## Estimated Effort
**4-5 hours** (hackathon pace) (includes dry run and iteration)

## Developer Assignment
Full team (requires coordination across CLI, demo app, and testing)
