# MF-010: Parent Mission Validation - Planning Summary

## Overview
This directory contains comprehensive planning documentation for implementing parent-level mission validation in the Mission-Forge CLI tool. This is a **MUST FINISH** feature required for project viability.

## Planning Documents

### 1. [Implementation Plan](./implementation_plan.md)
**Purpose**: High-level implementation roadmap with phases, tasks, and acceptance criteria

**Key Sections**:
- Architecture overview and design principles
- Data models and schemas
- Implementation phases (1-4 hours breakdown)
- Validation logic details
- File structure and examples
- CLI usage patterns
- Error handling strategies
- Testing strategy
- Edge cases and performance considerations

**Use this for**: Understanding the overall approach and breaking down work into phases

### 2. [Architecture Diagram](./architecture_diagram.md)
**Purpose**: Visual representations of system architecture and data flow

**Key Sections**:
- System architecture diagram (components and interactions)
- Validation flow sequence diagram
- Data flow diagram
- Status determination logic flowchart
- Component interaction matrix
- Error propagation flow
- File system layout
- Validation state machine
- Key design decisions
- Performance characteristics

**Use this for**: Understanding how components interact and data flows through the system

### 3. [Technical Specification](./technical_specification.md)
**Purpose**: Detailed API contracts, code examples, and implementation details

**Key Sections**:
- API contracts for all classes and methods
- Complete Pydantic model definitions
- Exception hierarchy with examples
- Implementation details with code snippets
- CLI output format examples
- Testing strategy with test cases
- Performance benchmarks
- Migration path and future enhancements

**Use this for**: Writing actual code with specific method signatures and logic

## Quick Start Guide

### For Implementers

1. **Read in this order**:
   - Start with [Implementation Plan](./implementation_plan.md) for context
   - Review [Architecture Diagram](./architecture_diagram.md) for visual understanding
   - Reference [Technical Specification](./technical_specification.md) while coding

2. **Implementation sequence**:
   ```
   Phase 1: Schema & Models (1 hour)
   ├── Add models to schemas.py
   ├── Add exceptions to exceptions.py
   └── Add workspace methods
   
   Phase 2: Service Layer (1.5 hours)
   ├── Create ParentValidationService
   ├── Implement aggregation logic
   ├── Implement validation logic
   └── Implement status determination
   
   Phase 3: CLI Command (0.5 hours)
   ├── Add parent command to validate.py
   └── Implement output formatting
   
   Phase 4: Testing (1 hour)
   ├── Write unit tests
   ├── Write integration tests
   └── Write CLI tests
   ```

3. **Key files to modify**:
   - [`src/missionforge/models/schemas.py`](../../src/missionforge/models/schemas.py)
   - [`src/missionforge/core/exceptions.py`](../../src/missionforge/core/exceptions.py)
   - [`src/missionforge/core/workspace.py`](../../src/missionforge/core/workspace.py)
   - [`src/missionforge/cli/commands/validate.py`](../../src/missionforge/cli/commands/validate.py)

4. **New files to create**:
   - `src/missionforge/core/parent_validation_service.py`
   - `tests/unit/test_parent_validation_service.py`
   - `tests/integration/test_parent_validation_flow.py`

### For Reviewers

1. **Architecture review**: Check [Architecture Diagram](./architecture_diagram.md)
   - Verify component interactions make sense
   - Check data flow is logical
   - Validate error handling paths

2. **API review**: Check [Technical Specification](./technical_specification.md)
   - Verify method signatures are complete
   - Check exception handling is comprehensive
   - Validate data models are correct

3. **Implementation review**: Check [Implementation Plan](./implementation_plan.md)
   - Verify all acceptance criteria are met
   - Check edge cases are handled
   - Validate testing strategy is comprehensive

## Key Design Decisions

### 1. Two-Level Validation Architecture
**Decision**: Parent validation is separate from and dependent on sub-mission validation

**Rationale**: 
- Allows catching integration issues that individual sub-missions miss
- Provides clear separation of concerns
- Enables parallel sub-mission development

**Impact**: Parent can fail even if all sub-missions pass individually

### 2. Immutable validation.json
**Decision**: Parent validation.json is read-only after creation

**Rationale**:
- Provides audit trail
- Prevents tampering
- Ensures validation integrity

**Impact**: Must use explicit re-validation to update

### 3. Language-Agnostic CLI
**Decision**: CLI handles deterministic operations, Bob handles code analysis

**Rationale**:
- Maintains architectural consistency
- Keeps CLI simple and fast
- Leverages Bob's code understanding capabilities

**Impact**: Requires Bob interaction for aggregate metrics

### 4. Comprehensive Forbidden Paths Check
**Decision**: Check forbidden paths across ALL sub-mission changes

**Rationale**:
- Prevents circumventing restrictions by splitting work
- Catches integration-level violations
- Provides stronger guarantees

**Impact**: More thorough validation than individual checks

## Success Criteria

✅ **Functional Requirements**:
- Command validates all sub-missions passed before proceeding
- Parent test command executes correctly
- Aggregate metrics are validated against targets
- Forbidden paths check covers all sub-mission changes
- Parent validation.json contains complete evidence
- Clear pass/fail status with detailed reasons

✅ **Non-Functional Requirements**:
- Terminal output shows comprehensive summary
- Handles edge cases (no sub-missions, partial completion)
- Integration tests cover various scenarios
- Performance meets benchmarks (< 2s excluding tests)
- Error messages are clear and actionable

## Dependencies

### Required (Must Complete First)
- ✅ MF-001: CLI Foundation
- ✅ MF-002: Schemas
- ✅ MF-003: Git/Test Utilities
- ⚠️ MF-009: Sub-Mission Validation (currently implemented)

### Optional (Can Work In Parallel)
- None - this is a terminal node in the dependency graph

## Estimated Effort

**Total**: 3-4 hours at hackathon pace

**Breakdown**:
- Phase 1 (Schema & Models): 1 hour
- Phase 2 (Service Layer): 1.5 hours
- Phase 3 (CLI Command): 0.5 hours
- Phase 4 (Testing): 1 hour

## Testing Strategy

### Unit Tests (30 min)
- Test sub-mission aggregation logic
- Test status determination logic
- Test metric validation logic
- Test forbidden paths checking

### Integration Tests (20 min)
- Test complete parent validation flow
- Test with all sub-missions PASSED
- Test with one sub-mission FAILED
- Test with missing sub-mission validation
- Test parent test execution
- Test aggregate metrics validation
- Test forbidden paths violations

### CLI Tests (10 min)
- Test command invocation
- Test output formatting
- Test error messages
- Test file creation

## Example Usage

```bash
# After all sub-missions validated
missionforge validate parent MF-001

# Output shows:
# ✓ Sub-missions: 4/4 PASSED
# ✓ Parent tests: PASSED (45.2s)
# ✓ Aggregate metrics: 2/2 PASSED
# ✓ Forbidden paths: No violations
# ✓ Parent Mission Validation: PASSED
```

## Related GitHub Issue

**Issue**: [#10 - MF-010: Parent Mission Validation](https://github.com/loudiman/Mission-Forge/issues/10)

**Priority**: MUST FINISH - Required for project viability

**Phase**: Phase 1 - Core CLI Harness

## Next Steps

1. **Review planning documents** with team
2. **Get approval** on architecture and approach
3. **Switch to Code mode** to begin implementation
4. **Follow implementation plan** phase by phase
5. **Run tests** after each phase
6. **Update GitHub issue** with progress

## Questions or Concerns?

If you have questions about:
- **Architecture**: See [Architecture Diagram](./architecture_diagram.md)
- **Implementation**: See [Technical Specification](./technical_specification.md)
- **Planning**: See [Implementation Plan](./implementation_plan.md)
- **GitHub Issue**: See [Issue #10](https://github.com/loudiman/Mission-Forge/issues/10)

## Document Metadata

- **Created**: 2026-05-17
- **Author**: Bob (Planning Mode)
- **Status**: Planning Complete, Ready for Implementation
- **Estimated Effort**: 3-4 hours
- **Priority**: MUST FINISH