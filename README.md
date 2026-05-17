# MissionForge CLI

AI-assisted mission decomposition and validation CLI tool for managing complex software development missions.

## Installation

### Requirements
- Python 3.11 or higher
- pip

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd Mission-Forge

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

## Quick Start

### 1. Initialize a Mission Workspace

```bash
# Create a new mission (shorthand)
missionforge init MF-001

# Or via the workspace subcommand
missionforge workspace init MF-001

# This creates:
# .missionforge/
# └── missions/
#     └── MF-001/
#         ├── mission.yaml      # Mission definition
#         ├── plan.yaml         # Execution plan
#         ├── report.md         # Generated report
#         └── sub-missions/     # Sub-mission directory
```

### 2. Validate a Mission

```bash
# Validate mission.yaml structure and constraints
missionforge mission MF-001 --validate
```

The validator checks:
- YAML syntax
- Required fields present
- Mission ID format and directory-name consistency
- Glob patterns are valid
- Aggregate metrics structure
- Test command is specified

### 3. Check Workspace Status

```bash
missionforge workspace status
```

This displays a table of all missions with their status and sub-mission count.

### 4. View Help

```bash
# General help
missionforge --help

# Command-specific help
missionforge workspace --help
missionforge workspace init --help
missionforge mission --help
```

## CLI Commands

### Global Options

- `--verbose, -v`: Enable verbose output (DEBUG level logging)
- `--log-file PATH`: Write logs to specified file

### Init Command

#### `missionforge init <MISSION_ID>`

Initialize a new mission workspace (alias for `workspace init`).

**Arguments:**
- `MISSION_ID`: Mission identifier (format: `[A-Z]{2,4}-\d{3}[A-Z]?`, e.g., `MF-001`, `PROJ-042A`)

**Options:**
- `--force`: Overwrite existing mission

**Example:**
```bash
missionforge init MF-001
missionforge init PROJ-123 --force
```

### Mission Commands

#### `missionforge mission <MISSION_ID> --validate`

Validate a parent mission configuration file.

**Arguments:**
- `MISSION_ID`: Mission identifier

**Options:**
- `--validate`: Validate the mission.yaml file

**Example:**
```bash
missionforge mission MF-001 --validate

### Decompose Commands

#### `missionforge decompose <MISSION_ID>`

Decompose a parent mission into sub-missions with guided workflow.

**What it does:**
1. Validates the parent mission
2. Creates sub-missions directory structure
3. Displays instructions and templates for Bob
4. Shows validation guidance
5. Provides plan.yaml guidance
6. Displays current status

**Arguments:**
- `MISSION_ID`: Parent mission identifier

**Example:**
```bash
missionforge decompose MF-001
```

**See also:** [Decompose Command Documentation](docs/DECOMPOSE_COMMAND.md)

#### `missionforge validate-submission <MISSION_ID> <SUB_MISSION_ID>`

Validate a specific sub-mission file.

**What it validates:**
- Sub-mission ID format (e.g., MF-001-A)
- Parent reference correctness
- Forbidden path conflicts
- Dependency existence
- Path overlaps (warnings)

**Arguments:**
- `MISSION_ID`: Parent mission identifier
- `SUB_MISSION_ID`: Sub-mission identifier to validate

**Example:**
```bash
missionforge validate-submission MF-001 MF-001-A
```

```

### Workspace Commands

#### `missionforge workspace init <MISSION_ID>`

Initialize a new mission workspace.

**Arguments:**
- `MISSION_ID`: Mission identifier (format: `[A-Z]{2,4}-\d{3}[A-Z]?`, e.g., `MF-001`, `PROJ-042A`)

**Options:**
- `--force`: Overwrite existing mission

**Example:**
```bash
missionforge workspace init MF-001
missionforge workspace init PROJ-123 --force
```

#### `missionforge workspace status`

Show workspace status and list all missions.

**Example:**
```bash
missionforge workspace status
```

### Version Command

#### `missionforge version`

Display version information.

## Project Structure

```
missionforge/
├── src/missionforge/
│   ├── cli/                    # CLI application
│   │   ├── app.py             # Main Typer app
│   │   ├── commands/          # Command groups
│   │   │   ├── workspace.py   # Workspace commands
│   │   │   └── mission.py     # Mission commands
│   │   └── utils/             # CLI utilities
│   │       └── validation.py  # Input validation
│   ├── core/                  # Core functionality
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Exception hierarchy
│   │   ├── logging.py         # Logging setup
│   │   ├── mission_validator.py # Mission validation adapter
│   │   └── workspace.py       # Workspace path resolution
│   ├── git/                   # Git operations
│   │   └── operations.py      # Safe git wrappers
│   ├── models/                # Pydantic models
│   │   └── schemas.py         # Mission schema models
│   ├── plugins/               # Plugin system
│   │   ├── base.py           # Plugin base classes
│   │   └── registry.py       # Plugin discovery
│   ├── schemas/               # Schema validators
│   │   └── validators.py      # SchemaValidator
│   └── utils/                 # Utilities
│       └── subprocess_utils.py # Safe subprocess execution
├── tests/                     # Test suite
│   ├── conftest.py           # Pytest fixtures
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
└── pyproject.toml            # Project configuration
```

## Configuration

MissionForge supports optional user-level configuration via `~/.missionforge.config.yaml`:

```yaml
# Test execution
test_timeout: 300
test_retry_count: 0

# Logging
log_level: INFO
log_file: null

# Git operations
git_diff_context: 3

# Plugins
plugin_dirs: []
disabled_plugins: []
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=missionforge --cov-report=html

# Run specific test file
pytest tests/unit/test_mission_validator.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Architecture

### Core Principles

1. **Language Agnostic**: CLI handles deterministic operations only (git, tests, file paths)
2. **No Shell Injection**: All subprocess calls use list arguments, never `shell=True`
3. **Type Safe**: Full type hints with Pydantic models
4. **Extensible**: Plugin architecture for validators, metrics, formatters, and commands
5. **User Friendly**: Rich terminal output with clear error messages

### Key Features

- **Workspace Discovery**: Automatically finds `.missionforge` directory from any subdirectory
- **Mission ID Validation**: Enforces standard format for mission identifiers
- **Safe Git Operations**: No GitPython dependency, uses subprocess with proper error handling
- **Plugin System**: Extensible architecture for custom functionality
- **Comprehensive Testing**: Tests covering CLI commands, schema validation, and mission lifecycle

## Mission ID Format

### Parent Mission
Pattern: `[A-Z]{2,4}-\d{3}[A-Z]?`

Examples:
- `MF-001`
- `PROJ-042`
- `FG-123A`

### Sub-Mission
Pattern: `[A-Z]{2,4}-\d{3}-[A-Z]`

Examples:
- `MF-001-A`
- `PROJ-042-B`
- `FG-123-C`

## Security

### Subprocess Safety

All command execution uses safe subprocess calls:

```python
# WRONG - shell injection risk
subprocess.run(f"git diff {branch}", shell=True)

# CORRECT - safe
subprocess.run(["git", "diff", branch])
```

### No GitPython

Uses system git via subprocess instead of GitPython library for better security and reliability.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass: `pytest tests/`
5. Format code: `black src/ tests/`
6. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions, please use the GitHub issue tracker.
