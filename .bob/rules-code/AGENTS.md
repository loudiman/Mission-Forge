# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Status
This is a **planning repository** for a 24-hour hackathon project. No implementation exists yet - only detailed specifications in [`issues/`](../../issues/).

## Code Mode Constraints

### No Implementation Yet
All code will be Python 3.11+ CLI using Click or Typer. See [`cli-foundation.md`](../../issues/cli-foundation.md) for structure.

### Subprocess Security (Critical)
NEVER use `shell=True` or `os.system()`. Always use subprocess with list arguments:
```python
# WRONG - shell injection risk
subprocess.run(f"git diff {branch}", shell=True)

# CORRECT - safe
subprocess.run(["git", "diff", branch])
```

### No GitPython Dependency
Use subprocess calls to system git, not GitPython library. See [`git-test-utilities.md`](../../issues/git-test-utilities.md).

### CLI Never Reads Source Code
Language-agnostic by design. CLI handles deterministic operations only (git diff, test execution, file paths). Bob handles code understanding.

### Immutable Files After Commit
[`baseline.json`](../../issues/baseline-flow.md) cannot be modified after commit without `--reset` flag. Implement file permission checks.

### Mission ID Validation
- Parent: `^[A-Z]{2,4}-\d{3}[A-Z]?$`
- Sub-mission: `^[A-Z]{2,4}-\d{3}-[A-Z]$`

Validate format before any file operations.

## Testing Requirements
- Unit test coverage > 80% for validation logic
- Integration tests for all CLI commands
- Test files must cover error cases and edge cases
- See individual issue files for acceptance criteria