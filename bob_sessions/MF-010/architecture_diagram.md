# MF-010: Parent Mission Validation - Architecture & Data Flow

## System Architecture

```mermaid
graph TB
    subgraph "CLI Layer"
        CMD[validate parent command]
    end
    
    subgraph "Service Layer"
        PVS[ParentValidationService]
        VS[ValidationService]
        TE[TestExecutor]
    end
    
    subgraph "Data Layer"
        WS[Workspace]
        PM[ParentMission YAML]
        SM1[Sub-Mission-A validation.json]
        SM2[Sub-Mission-B validation.json]
        SM3[Sub-Mission-C validation.json]
        PV[Parent validation.json]
    end
    
    subgraph "Validation Logic"
        AGG[Aggregate Sub-Missions]
        TEST[Execute Parent Tests]
        METRICS[Validate Aggregate Metrics]
        PATHS[Check Forbidden Paths]
        STATUS[Determine Status]
    end
    
    CMD --> PVS
    PVS --> WS
    PVS --> AGG
    PVS --> TEST
    PVS --> METRICS
    PVS --> PATHS
    PVS --> STATUS
    
    AGG --> SM1
    AGG --> SM2
    AGG --> SM3
    
    TEST --> TE
    METRICS --> VS
    PATHS --> SM1
    PATHS --> SM2
    PATHS --> SM3
    
    STATUS --> PV
    
    WS --> PM
    WS --> SM1
    WS --> SM2
    WS --> SM3
    WS --> PV
```

## Validation Flow Sequence

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant PVS as ParentValidationService
    participant WS as Workspace
    participant FS as FileSystem
    participant Bob
    
    User->>CLI: missionforge validate parent MF-001
    CLI->>PVS: validate_parent_mission("MF-001")
    
    Note over PVS: Phase 1: Load Mission
    PVS->>WS: mission_path("MF-001")
    WS->>FS: Read mission.yaml
    FS-->>PVS: ParentMission data
    
    Note over PVS: Phase 2: Aggregate Sub-Missions
    PVS->>WS: Get sub-mission IDs
    loop For each sub-mission
        PVS->>WS: validation_path(sub_id)
        WS->>FS: Read validation.json
        FS-->>PVS: SubMissionValidation
    end
    PVS->>PVS: Check all PASSED
    
    alt Any sub-mission not PASSED
        PVS-->>CLI: Error: Sub-mission failed
        CLI-->>User: Display error
    end
    
    Note over PVS: Phase 3: Execute Parent Tests
    PVS->>PVS: execute_test_command()
    PVS->>FS: Run test command
    FS-->>PVS: Test results
    
    alt Tests failed
        PVS-->>CLI: Error: Tests failed
        CLI-->>User: Display error
    end
    
    Note over PVS: Phase 4: Aggregate Metrics
    PVS->>Bob: Prompt for metric values
    Bob-->>PVS: Filled metric values
    PVS->>PVS: Validate metrics
    
    alt Any metric failed
        PVS-->>CLI: Error: Metric failed
        CLI-->>User: Display error
    end
    
    Note over PVS: Phase 5: Forbidden Paths
    PVS->>PVS: Collect all changed files
    PVS->>PVS: Check against forbidden_paths
    
    alt Paths violated
        PVS-->>CLI: Error: Forbidden paths
        CLI-->>User: Display error
    end
    
    Note over PVS: Phase 6: Write Result
    PVS->>PVS: Determine overall status
    PVS->>WS: parent_validation_path()
    PVS->>FS: Write validation.json (immutable)
    FS-->>PVS: Success
    
    PVS-->>CLI: Validation complete
    CLI-->>User: Display summary
```

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph Input
        PM[mission.yaml]
        SM1[MF-001-A/validation.json]
        SM2[MF-001-B/validation.json]
        SM3[MF-001-C/validation.json]
    end
    
    subgraph Processing
        AGG[Aggregate<br/>Sub-Missions]
        TEST[Execute<br/>Parent Tests]
        METRICS[Validate<br/>Aggregate Metrics]
        PATHS[Check<br/>Forbidden Paths]
    end
    
    subgraph Output
        PV[validation.json]
        REPORT[Terminal Report]
    end
    
    PM --> AGG
    SM1 --> AGG
    SM2 --> AGG
    SM3 --> AGG
    
    PM --> TEST
    PM --> METRICS
    PM --> PATHS
    
    SM1 --> PATHS
    SM2 --> PATHS
    SM3 --> PATHS
    
    AGG --> PV
    TEST --> PV
    METRICS --> PV
    PATHS --> PV
    
    PV --> REPORT
```

## Status Determination Logic

```mermaid
flowchart TD
    START[Start Validation]
    
    CHECK_SUBS{All sub-missions<br/>have validation.json?}
    CHECK_SUBS_PASS{All sub-missions<br/>PASSED?}
    CHECK_TEST{Parent test<br/>defined?}
    RUN_TEST[Execute parent test]
    CHECK_TEST_PASS{Test passed?}
    CHECK_METRICS{Aggregate metrics<br/>defined?}
    VALIDATE_METRICS[Validate metrics]
    CHECK_METRICS_PASS{All metrics<br/>PASSED?}
    CHECK_PATHS[Check forbidden paths]
    CHECK_PATHS_PASS{No violations?}
    
    INCOMPLETE[Status: INCOMPLETE]
    FAILED[Status: FAILED]
    PASSED[Status: PASSED]
    
    START --> CHECK_SUBS
    CHECK_SUBS -->|No| INCOMPLETE
    CHECK_SUBS -->|Yes| CHECK_SUBS_PASS
    
    CHECK_SUBS_PASS -->|No| FAILED
    CHECK_SUBS_PASS -->|Yes| CHECK_TEST
    
    CHECK_TEST -->|No| CHECK_METRICS
    CHECK_TEST -->|Yes| RUN_TEST
    RUN_TEST --> CHECK_TEST_PASS
    CHECK_TEST_PASS -->|No| FAILED
    CHECK_TEST_PASS -->|Yes| CHECK_METRICS
    
    CHECK_METRICS -->|No| CHECK_PATHS
    CHECK_METRICS -->|Yes| VALIDATE_METRICS
    VALIDATE_METRICS --> CHECK_METRICS_PASS
    CHECK_METRICS_PASS -->|No| FAILED
    CHECK_METRICS_PASS -->|Yes| CHECK_PATHS
    
    CHECK_PATHS --> CHECK_PATHS_PASS
    CHECK_PATHS_PASS -->|No| FAILED
    CHECK_PATHS_PASS -->|Yes| PASSED
```

## Component Interaction Matrix

| Component | Reads From | Writes To | Depends On |
|-----------|-----------|-----------|------------|
| CLI Command | User input | Terminal output | ParentValidationService |
| ParentValidationService | mission.yaml, sub-mission validation.json | parent validation.json | Workspace, TestExecutor |
| Workspace | File system | - | - |
| TestExecutor | Test command | Test output | subprocess_utils |
| ValidationService | - | - | Used for metric logic |

## Error Propagation

```mermaid
flowchart TD
    E1[Sub-mission missing validation.json]
    E2[Sub-mission FAILED/BLOCKED]
    E3[Parent test failed]
    E4[Aggregate metric failed]
    E5[Forbidden path violated]
    
    H1[ParentValidationIncompleteError]
    H2[ParentValidationFailedError]
    H3[ParentTestFailedError]
    H4[AggregateMetricFailedError]
    H5[ForbiddenPathViolationError]
    
    CLI[CLI Error Handler]
    USER[User sees formatted error]
    
    E1 --> H1
    E2 --> H2
    E3 --> H3
    E4 --> H4
    E5 --> H5
    
    H1 --> CLI
    H2 --> CLI
    H3 --> CLI
    H4 --> CLI
    H5 --> CLI
    
    CLI --> USER
```

## File System Layout

```
.missionforge/
└── missions/
    └── MF-001/                          # Parent mission directory
        ├── mission.yaml                 # Parent mission definition
        ├── plan.yaml                    # Execution plan
        ├── validation.json              # ← NEW: Parent validation result
        └── sub-missions/
            ├── MF-001-A/
            │   ├── sub-mission.yaml
            │   ├── baseline.json
            │   └── validation.json      # Sub-mission validation (input)
            ├── MF-001-B/
            │   ├── sub-mission.yaml
            │   ├── baseline.json
            │   └── validation.json      # Sub-mission validation (input)
            ├── MF-001-C/
            │   ├── sub-mission.yaml
            │   ├── baseline.json
            │   └── validation.json      # Sub-mission validation (input)
            └── MF-001-D/
                ├── sub-mission.yaml
                ├── baseline.json
                └── validation.json      # Sub-mission validation (input)
```

## Validation States

```mermaid
stateDiagram-v2
    [*] --> NotStarted: Initial state
    NotStarted --> InProgress: validate parent command
    InProgress --> CheckingSubs: Load sub-missions
    CheckingSubs --> Incomplete: Missing validation.json
    CheckingSubs --> RunningTests: All subs PASSED
    RunningTests --> Failed: Test failed
    RunningTests --> ValidatingMetrics: Test passed
    ValidatingMetrics --> Failed: Metric failed
    ValidatingMetrics --> CheckingPaths: Metrics passed
    CheckingPaths --> Failed: Path violated
    CheckingPaths --> Passed: All checks passed
    
    Incomplete --> [*]
    Failed --> [*]
    Passed --> [*]
```

## Key Design Decisions

### 1. Two-Level Validation
**Decision**: Parent validation is separate from sub-mission validation
**Rationale**: Allows catching integration issues that individual sub-missions miss
**Impact**: Parent can fail even if all sub-missions pass

### 2. Immutable validation.json
**Decision**: Parent validation.json is read-only after creation
**Rationale**: Provides audit trail and prevents tampering
**Impact**: Must use --force flag to re-validate

### 3. Aggregate Metrics via Bob
**Decision**: Bob measures aggregate metrics, not CLI
**Rationale**: Maintains language-agnostic CLI design
**Impact**: Requires Bob interaction during validation

### 4. Cross-Sub-Mission Forbidden Paths
**Decision**: Check forbidden paths across ALL sub-mission changes
**Rationale**: Prevents circumventing restrictions by splitting work
**Impact**: More comprehensive validation than individual checks

### 5. Status Hierarchy
**Decision**: INCOMPLETE < FAILED < PASSED
**Rationale**: Clear distinction between not-ready and failed
**Impact**: Different error messages and recovery paths

## Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| Load sub-missions | O(n) | O(n) | n = number of sub-missions |
| Aggregate status | O(n) | O(1) | Single pass through sub-missions |
| Execute tests | O(t) | O(1) | t = test execution time |
| Validate metrics | O(m) | O(m) | m = number of metrics |
| Check paths | O(n*p) | O(n*p) | n = sub-missions, p = paths per sub |

## Security Considerations

1. **File Permissions**: validation.json is read-only (444)
2. **Path Validation**: All file paths validated to prevent traversal
3. **Command Injection**: Test commands sanitized before execution
4. **Output Sanitization**: Test output sanitized before display
5. **Metric Validation**: Type checking on all metric values

## Extensibility Points

1. **Custom Validators**: Plugin system for custom validation logic
2. **Custom Metrics**: Support for domain-specific aggregate metrics
3. **Custom Formatters**: Different output formats (JSON, HTML, etc.)
4. **Notification Hooks**: Webhooks for validation completion
5. **Report Generators**: Custom report generation from validation.json