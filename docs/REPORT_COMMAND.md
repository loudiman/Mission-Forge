# Report Command Documentation

## Overview

The `missionforge report` command generates comprehensive PR-ready Markdown evidence reports for completed missions. These reports summarize all mission activities, validation results, metrics, and test outcomes in a format suitable for pull request attachments and mission completion evidence.

## Command Syntax

```bash
missionforge report <mission-id> [OPTIONS]
```

## Arguments

- `<mission-id>` (required): The mission identifier (e.g., `MF-001`)

## Options

- `--output, -o <path>`: Custom output path for the report (default: `<mission-dir>/report.md`)
- `--stdout`: Output report to stdout instead of writing to a file
- `--help`: Show help message and exit

## Usage Examples

### Basic Report Generation

Generate a report in the default location (mission directory):

```bash
missionforge report MF-001
```

This creates `.missionforge/missions/MF-001/report.md`

### Custom Output Path

Generate a report at a specific location:

```bash
missionforge report MF-001 --output ./evidence/mission-report.md
```

### Output to Console

Display the report in the terminal without creating a file:

```bash
missionforge report MF-001 --stdout
```

This is useful for:
- Quick review of mission status
- Piping to other tools
- CI/CD integration

## Report Structure

The generated report includes the following sections:

### 1. Mission Header
- Mission ID and goal
- Overall status (PASSED/FAILED/INCOMPLETE)
- Generation timestamp and metadata
- Git commit hash

### 2. Mission Goal
- High-level mission objective
- Context and purpose

### 3. Decomposition Summary
- Dependency diagram (ASCII format)
- Sub-missions overview
- Total count of sub-missions

### 4. Sub-Mission Results
- Summary table with status, tests, and metrics
- Detailed results for each sub-mission:
  - Goal and dependencies
  - Validation status
  - Metrics (files changed, lines added/removed, test coverage)
  - Custom metrics
  - Errors (if any)

### 5. Aggregate Metrics
- Comparison table showing:
  - Metric name
  - Target/min/max values
  - Final achieved value
  - Pass/fail status

### 6. Test Results
- Parent mission test results
- Test command used
- Test metrics and coverage
- Sub-mission test summary table

### 7. Files Changed
- Total files changed count
- Breakdown by change type (added, modified, deleted, renamed)
- Git statistics (insertions, deletions)
- Complete list of changed files

### 8. Forbidden Path Violations
- List of any forbidden path violations detected
- Warnings if violations exist
- Confirmation if no violations

### 9. Next Steps
- Suggested next mission (if available)
- Recommendations based on mission status
- Action items for PR submission or fixes

### 10. Metadata
- Mission ID
- Report generation timestamp
- CLI version
- Full git commit hash

## Report Status Indicators

The report uses clear status indicators:

- ✓ PASSED - All checks passed successfully
- ✗ FAILED - One or more checks failed
- ⚠ INCOMPLETE - Validation data missing or incomplete
- ⚠ NO DATA - No validation results available

## Use Cases

### 1. Pull Request Evidence

Attach the generated report to your pull request:

```bash
missionforge report MF-001
# Attach .missionforge/missions/MF-001/report.md to PR
```

The report provides reviewers with:
- Complete mission context
- All validation results
- Test coverage metrics
- Files changed summary

### 2. Mission Completion Verification

Verify mission completion before submitting:

```bash
missionforge report MF-001 --stdout
```

Review the output to ensure:
- All sub-missions passed
- Metrics meet targets
- No forbidden path violations
- Tests pass

### 3. CI/CD Integration

Generate reports in automated pipelines:

```bash
# Generate report
missionforge report MF-001 --output ./artifacts/report.md

# Check exit code
if [ $? -eq 0 ]; then
    echo "Report generated successfully"
else
    echo "Report generation failed"
    exit 1
fi
```

### 4. Documentation Archive

Create mission completion archives:

```bash
# Generate report with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
missionforge report MF-001 --output ./archive/MF-001_${TIMESTAMP}.md
```

## Prerequisites

Before generating a report, ensure:

1. **Mission exists**: The mission directory and `mission.yaml` must exist
2. **Validation complete**: Run `missionforge validate <mission-id>` first
3. **Sub-missions defined**: At least one sub-mission should be defined
4. **Git repository**: The workspace should be in a git repository

## Error Handling

### Mission Not Found

```
Error: Mission MF-001 not found
Expected: .missionforge/missions/MF-001
```

**Solution**: Verify the mission ID and ensure the mission directory exists.

### Missing Mission File

```
Error: Mission file not found: .missionforge/missions/MF-001/mission.yaml
Initialize mission with: missionforge init MF-001
```

**Solution**: Create the mission file or initialize the mission.

### No Workspace

```
Error: No .missionforge workspace found
```

**Solution**: Run `missionforge workspace init` in your project root.

### Validation Data Missing

The report will still generate but will show "⚠ NO DATA" for missing validation results.

**Solution**: Run `missionforge validate <mission-id>` to generate validation data.

## Report Quality Tips

### 1. Complete All Sub-Missions

Ensure all sub-missions are completed and validated before generating the final report.

### 2. Run Parent Validation

Always run parent mission validation to get aggregate metrics:

```bash
missionforge validate MF-001
```

### 3. Verify Test Coverage

Check that test coverage meets your targets before generating the report.

### 4. Review Metrics

Ensure all custom metrics are captured in validation results.

### 5. Check Dependencies

Verify the dependency diagram accurately reflects sub-mission relationships.

## Integration with Other Commands

The report command works with other MissionForge commands:

```bash
# 1. Initialize mission
missionforge init MF-001

# 2. Define sub-missions (manual or via decompose)
# Edit .missionforge/missions/MF-001/mission.yaml

# 3. Complete sub-missions
# Work on each sub-mission

# 4. Validate mission
missionforge validate MF-001

# 5. Generate report
missionforge report MF-001

# 6. Review and submit PR with report attached
```

## Advanced Usage

### Custom Report Templates

The report uses Jinja2 templates located in `src/missionforge/templates/`. You can customize the template by modifying `mission_report.md.j2`.

### Programmatic Access

Use the `ReportGenerator` class directly in Python:

```python
from pathlib import Path
from missionforge.core.report_generator import ReportGenerator

generator = ReportGenerator()
mission_path = Path(".missionforge/missions/MF-001")
content, output_path = generator.generate_report(mission_path)

print(f"Report generated: {output_path}")
```

## Troubleshooting

### Report Shows "INCOMPLETE" Status

**Cause**: Missing validation data for one or more sub-missions.

**Solution**: Run validation for all sub-missions and the parent mission.

### Metrics Not Appearing

**Cause**: Custom metrics not captured in validation results.

**Solution**: Ensure your validation process captures all required metrics.

### Git Information Shows "unknown"

**Cause**: Not in a git repository or git commands failing.

**Solution**: Ensure the workspace is in a valid git repository.

### Template Rendering Errors

**Cause**: Missing or corrupted template file.

**Solution**: Verify `src/missionforge/templates/mission_report.md.j2` exists and is valid.

## Best Practices

1. **Generate reports after validation**: Always run validation before generating reports
2. **Review before PR submission**: Check the report for completeness and accuracy
3. **Archive reports**: Keep reports for historical reference
4. **Use in CI/CD**: Automate report generation in your pipeline
5. **Customize templates**: Adapt the report template to your team's needs

## Related Commands

- `missionforge validate` - Validate mission before generating report
- `missionforge init` - Initialize a new mission
- `missionforge workspace init` - Initialize workspace

## See Also

- [Mission Validation](./VALIDATION.md)
- [Mission Schema](./schemas/mission-schema-examples.md)
- [CLI Overview](../README.md)

---

*Generated by MissionForge CLI v0.1.0*