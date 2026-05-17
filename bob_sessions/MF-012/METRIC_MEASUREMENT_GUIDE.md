# Metric Measurement Guide for Bob

## Overview
This guide explains how Bob should measure different types of metrics when filling `.todo.json` files during baseline capture and validation capture phases.

---

## Common Metric Types

### 1. Test Coverage (float)

**What it measures:** Percentage of code covered by tests

**How to measure:**
```bash
# Python (pytest-cov)
pytest --cov=src/module --cov-report=term

# JavaScript (Jest)
jest --coverage

# Look for line coverage percentage
```

**Example:**
```json
{
  "metric_id": "test_coverage",
  "baseline_value": 78.5,
  "target_value": 85.0,
  "final_value": 87.2
}
```

**Tips:**
- Use line coverage, not branch coverage (unless specified)
- Measure only within `allowed_paths`
- Round to 1 decimal place

---

### 2. Lines Added/Removed (int)

**What it measures:** Number of lines changed in implementation

**How to measure:**
```bash
# Git diff stats
git diff --stat baseline_commit..HEAD

# Or use CLI's deterministic evidence
# (already in validation.todo.json)
```

**Example:**
```json
{
  "metric_id": "lines_added",
  "baseline_value": 0,
  "target_value": null,
  "final_value": 342
}
```

**Tips:**
- Count only non-whitespace, non-comment lines
- Exclude generated files
- Use git diff stats as source of truth

---

### 3. Boolean Metrics (bool)

**What it measures:** Presence/absence of a feature or condition

**Common examples:**
- `rest_endpoint_exists`: Does a REST endpoint exist?
- `uses_legacy_api`: Is legacy API still in use?
- `has_documentation`: Is feature documented?

**How to measure:**
```bash
# Search for patterns
grep -r "RestEndpoint" src/module/

# Check file existence
test -f src/api/rest_endpoint.py && echo "true" || echo "false"

# Verify imports
grep "from legacy import" src/module/*.py
```

**Example:**
```json
{
  "metric_id": "rest_endpoint_exists",
  "baseline_value": false,
  "target_value": true,
  "final_value": true
}
```

**Tips:**
- Be precise: true means fully implemented, not partially
- Document your verification method in comments
- When in doubt, verify manually

---

### 4. Count Metrics (int)

**What it measures:** Number of occurrences of something

**Common examples:**
- `corba_references_count`: Number of CORBA references
- `deprecated_calls`: Number of deprecated API calls
- `todo_comments`: Number of TODO comments

**How to measure:**
```bash
# Count pattern occurrences
grep -r "CORBA" src/module/ | wc -l

# Count files matching pattern
find src/module/ -name "*.deprecated" | wc -l

# Count TODO comments
grep -r "TODO" src/module/ | wc -l
```

**Example:**
```json
{
  "metric_id": "corba_references_count",
  "baseline_value": 7,
  "target_value": 0,
  "final_value": 0
}
```

**Tips:**
- Be consistent in counting method
- Exclude test files unless specified
- Document edge cases

---

### 5. Complexity Metrics (int/float)

**What it measures:** Code complexity (cyclomatic, cognitive, etc.)

**How to measure:**
```bash
# Python (radon)
radon cc src/module/ -a

# JavaScript (complexity-report)
cr src/module/

# Look for average complexity
```

**Example:**
```json
{
  "metric_id": "avg_complexity",
  "baseline_value": 12.3,
  "target_value": 8.0,
  "final_value": 7.5
}
```

**Tips:**
- Use cyclomatic complexity by default
- Average across all functions in scope
- Exclude trivial functions (< 3 lines)

---

### 6. Performance Metrics (float)

**What it measures:** Execution time, memory usage, etc.

**How to measure:**
```bash
# Run benchmarks
pytest tests/benchmark_test.py --benchmark-only

# Time execution
time python src/module/main.py

# Memory profiling
python -m memory_profiler src/module/main.py
```

**Example:**
```json
{
  "metric_id": "api_response_time_ms",
  "baseline_value": 250.0,
  "target_value": 100.0,
  "final_value": 85.0
}
```

**Tips:**
- Run multiple times, use median
- Ensure consistent test environment
- Document test conditions

---

## Measurement Workflow

### Baseline Capture Phase

1. **CLI runs:** `missionforge baseline capture MF-001-A`
2. **CLI creates:** `baseline.todo.json` with empty metric values
3. **Bob's tasks:**
   ```
   a. Read allowed_paths from MF-001-A.yaml
   b. Analyze code within those paths
   c. For each metric in baseline.todo.json:
      - Determine measurement method
      - Run measurement tools
      - Record accurate value
   d. Fill all metric values
   e. Verify no values are null/missing
   ```
4. **Bob runs:** `missionforge baseline commit MF-001-A`
5. **CLI validates:** All metrics filled, creates immutable `baseline.json`

### Validation Capture Phase

1. **CLI runs:** `missionforge validate capture MF-001-A`
2. **CLI creates:** `validation.todo.json` with empty metric values
3. **Bob's tasks:**
   ```
   a. Read allowed_paths from MF-001-A.yaml
   b. Analyze FINAL code state within those paths
   c. For each metric in validation.todo.json:
      - Use SAME measurement method as baseline
      - Run measurement tools
      - Record accurate final value
   d. Fill all metric values
   e. Compare against targets
   ```
4. **Bob runs:** `missionforge validate commit MF-001-A`
5. **CLI compares:** baseline → target → final, determines PASS/FAIL

---

## Best Practices

### 1. Consistency is Critical
- Use the **same measurement method** for baseline and validation
- Document your method if non-obvious
- Automate measurements when possible

### 2. Scope Awareness
- Only measure within `allowed_paths`
- Exclude files outside scope
- Respect `forbidden_paths`

### 3. Accuracy Over Speed
- Take time to measure correctly
- Verify edge cases
- Round appropriately (1-2 decimal places for floats)

### 4. Documentation
- Comment your measurement approach
- Note any assumptions
- Explain unusual values

### 5. Automation
```bash
# Create measurement scripts
cat > measure_coverage.sh << 'EOF'
#!/bin/bash
pytest --cov=src/auth --cov-report=term | grep "TOTAL" | awk '{print $4}' | sed 's/%//'
EOF
chmod +x measure_coverage.sh
```

---

## Common Pitfalls

### ❌ Measuring Outside Scope
```yaml
# MF-001-A.yaml
allowed_paths:
  - "src/auth/**"

# WRONG: Measuring entire codebase
pytest --cov=src --cov-report=term

# CORRECT: Measuring only allowed paths
pytest --cov=src/auth --cov-report=term
```

### ❌ Inconsistent Methods
```json
// Baseline: Used line coverage
"test_coverage": 78.5

// Validation: Used branch coverage (WRONG!)
"test_coverage": 65.2

// Should use same method (line coverage)
```

### ❌ Missing Measurements
```json
// WRONG: Leaving values null
{
  "metric_id": "test_coverage",
  "baseline_value": null,  // ❌ Must fill!
  "target_value": 85.0,
  "final_value": null
}
```

### ❌ Imprecise Boolean Values
```json
// WRONG: Partially implemented
{
  "metric_id": "rest_endpoint_exists",
  "final_value": true  // But only 50% complete!
}

// CORRECT: Only true when fully implemented
{
  "metric_id": "rest_endpoint_exists",
  "final_value": false  // Not complete yet
}
```

---

## Aggregate Metrics (Parent Level)

Some metrics aggregate across all sub-missions:

### Sum Aggregation
```json
// Parent mission.yaml
"aggregate_metrics": {
  "total_lines_added": {
    "aggregation": "sum",
    "target": 2000
  }
}

// Calculated as: MF-001-A.lines_added + MF-001-B.lines_added + ...
```

### Average Aggregation
```json
// Parent mission.yaml
"aggregate_metrics": {
  "avg_test_coverage": {
    "aggregation": "avg",
    "target": 85.0
  }
}

// Calculated as: mean(MF-001-A.coverage, MF-001-B.coverage, ...)
```

### Min/Max Aggregation
```json
// Parent mission.yaml
"aggregate_metrics": {
  "min_test_coverage": {
    "aggregation": "min",
    "target": 80.0
  }
}

// Calculated as: min(MF-001-A.coverage, MF-001-B.coverage, ...)
```

**Note:** Bob doesn't measure aggregate metrics directly. The CLI calculates them from sub-mission validation.json files.

---

## Troubleshooting

### "Cannot measure test coverage"
**Solution:**
```bash
# Install coverage tool
pip install pytest-cov  # Python
npm install --save-dev jest  # JavaScript

# Run with coverage
pytest --cov=src/module --cov-report=term
```

### "Metric value seems wrong"
**Solution:**
1. Re-run measurement tool
2. Check scope (allowed_paths)
3. Verify measurement method
4. Compare with manual inspection

### "Don't know how to measure custom metric"
**Solution:**
1. Check metric definition in YAML
2. Look for similar metrics in other sub-missions
3. Ask for clarification in mission.yaml comments
4. Document your approach

---

## Example: Complete Measurement Session

```bash
# Sub-mission: MF-001-A (Auth Module Migration)
# Metrics: test_coverage, rest_endpoint_exists, corba_references_count

# 1. Baseline Capture
missionforge baseline capture MF-001-A

# 2. Measure baseline metrics
# a) Test coverage
pytest --cov=src/auth --cov-report=term
# Output: 78.5%

# b) REST endpoint exists
grep -r "class RestAuthEndpoint" src/auth/
# Output: (no matches) → false

# c) CORBA references
grep -r "CORBA" src/auth/ | wc -l
# Output: 7

# 3. Fill baseline.todo.json
{
  "metrics": [
    {
      "metric_id": "test_coverage",
      "baseline_value": 78.5,
      "target_value": 85.0
    },
    {
      "metric_id": "rest_endpoint_exists",
      "baseline_value": false,
      "target_value": true
    },
    {
      "metric_id": "corba_references_count",
      "baseline_value": 7,
      "target_value": 0
    }
  ]
}

# 4. Commit baseline
missionforge baseline commit MF-001-A

# 5. Implement changes
# ... (Bob makes code changes) ...

# 6. Validation Capture
missionforge validate capture MF-001-A

# 7. Measure final metrics (SAME METHODS!)
pytest --cov=src/auth --cov-report=term  # 87.2%
grep -r "class RestAuthEndpoint" src/auth/  # Found!
grep -r "CORBA" src/auth/ | wc -l  # 0

# 8. Fill validation.todo.json
{
  "metrics": [
    {
      "metric_id": "test_coverage",
      "baseline_value": 78.5,
      "target_value": 85.0,
      "final_value": 87.2  # ✓ PASSED (87.2 >= 85.0)
    },
    {
      "metric_id": "rest_endpoint_exists",
      "baseline_value": false,
      "target_value": true,
      "final_value": true  # ✓ PASSED
    },
    {
      "metric_id": "corba_references_count",
      "baseline_value": 7,
      "target_value": 0,
      "final_value": 0  # ✓ PASSED
    }
  ]
}

# 9. Commit validation
missionforge validate commit MF-001-A
# Output: Overall Status: PASSED ✓
```

---

**Made with Bob** 🤖