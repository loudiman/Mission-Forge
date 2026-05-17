# MissionForge CLI Foundation - Detailed Implementation Plan

## Executive Summary

This plan outlines a **highly maintainable, extensible CLI architecture** for MissionForge, designed for rapid hackathon development while supporting future integrations through well-defined extension points.

**Key Decisions:**
- **Framework**: Typer (type-safe, modern Python 3.11+)
- **Package**: Pip-installable via pyproject.toml
- **Config**: Optional `.missionforge.config.yaml` for advanced users
- **Extensions**: Plugin architecture for validators, metrics, formatters, and commands
- **Error Handling**: Fail-fast with actionable error messages

---

## 1. Project Structure

```
missionforge/
├── pyproject.toml              # Modern Python packaging
├── README.md
├── .missionforge.config.yaml   # Optional user config (gitignored)
├── src/
│   └── missionforge/
│       ├── __init__.py
│       ├── __main__.py         # Entry point: python -m missionforge
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── app.py          # Main Typer app
│       │   ├── commands/       # Command groups
│       │   │   ├── __init__.py
│       │   │   ├── workspace.py    # init, status
│       │   │   ├── mission.py      # validate, decompose, plan
│       │   │   ├── baseline.py     # baseline operations
│       │   │   └── report.py       # report generation
│       │   └── utils/
│       │       ├── __init__.py
│       │       ├── output.py       # Rich console formatting
│       │       └── validation.py   # Input validation helpers
│       ├── core/
│       │   ├── __init__.py
│       │   ├── workspace.py        # Workspace path resolution
│       │   ├── config.py           # Config file management
│       │   ├── exceptions.py       # Custom exception hierarchy
│       │   └── logging.py          # Logging configuration
│       ├── models/
│       │   ├── __init__.py
│       │   ├── mission.py          # Pydantic models for missions
│       │   ├── baseline.py         # Baseline models
│       │   └── validation.py       # Validation result models
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── mission.json        # JSON schemas
│       │   ├── baseline.json
│       │   └── validators.py       # Schema validation logic
│       ├── git/
│       │   ├── __init__.py
│       │   ├── operations.py       # Git wrapper functions
│       │   └── diff.py             # Diff analysis
│       ├── testing/
│       │   ├── __init__.py
│       │   └── executor.py         # Test command execution
│       ├── plugins/
│       │   ├── __init__.py
│       │   ├── base.py             # Plugin base classes
│       │   ├── registry.py         # Plugin discovery/loading
│       │   ├── validators/         # Validator plugins
│       │   │   ├── __init__.py
│       │   │   └── default.py
│       │   ├── metrics/            # Metric collector plugins
│       │   │   ├── __init__.py
│       │   │   └── default.py
│       │   ├── formatters/         # Report formatter plugins
│       │   │   ├── __init__.py
│       │   │   └── markdown.py
│       │   └── commands/           # Command plugins
│       │       └── __init__.py
│       └── utils/
│           ├── __init__.py
│           ├── paths.py            # Path utilities
│           ├── yaml_utils.py       # YAML helpers
│           └── subprocess_utils.py # Safe subprocess execution
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── unit/
│   │   ├── test_workspace.py
│   │   ├── test_config.py
│   │   ├── test_git.py
│   │   └── test_plugins.py
│   └── integration/
│       ├── test_cli_commands.py
│       └── test_workspace_flow.py
└── docs/
    ├── architecture.md
    ├── plugin_development.md
    └── configuration.md
```

---

## 2. Technology Stack & Dependencies

### Core Dependencies (pyproject.toml)

```toml
[project]
name = "missionforge"
version = "0.1.0"
description = "AI-assisted mission decomposition and validation CLI"
requires-python = ">=3.11"
dependencies = [
    "typer[all]>=0.9.0",      # CLI framework with rich support
    "pydantic>=2.5.0",         # Data validation and models
    "pyyaml>=6.0.1",           # YAML parsing
    "jsonschema>=4.20.0",      # JSON schema validation
    "jinja2>=3.1.2",           # Template rendering
    "rich>=13.7.0",            # Terminal formatting
    "pathspec>=0.11.2",        # Gitignore-style path matching
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "black>=23.12.0",
    "ruff>=0.1.8",
    "mypy>=1.7.1",
]

[project.scripts]
missionforge = "missionforge.cli.app:main"

[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Rationale:**
- **Typer**: Type-safe CLI with automatic help generation, built on Click
- **Pydantic**: Runtime type validation, perfect for YAML/JSON models
- **Rich**: Beautiful terminal output with progress bars, tables, syntax highlighting
- **pathspec**: Industry-standard glob matching (same as gitignore)
- **No GitPython**: Using subprocess as per AGENTS.md constraints

---

## 3. Core Architecture Components

### 3.1 Workspace Path Resolution

**File**: `src/missionforge/core/workspace.py`

```python
from pathlib import Path
from typing import Optional
from .exceptions import WorkspaceNotFoundError

class Workspace:
    """Manages .missionforge workspace discovery and paths."""
    
    WORKSPACE_DIR = ".missionforge"
    MISSIONS_DIR = "missions"
    
    def __init__(self, start_path: Optional[Path] = None):
        self.root = self._find_workspace_root(start_path or Path.cwd())
        self.workspace_dir = self.root / self.WORKSPACE_DIR
        self.missions_dir = self.workspace_dir / self.MISSIONS_DIR
    
    def _find_workspace_root(self, start: Path) -> Path:
        """Walk up directory tree to find .missionforge/"""
        current = start.resolve()
        while current != current.parent:
            if (current / self.WORKSPACE_DIR).is_dir():
                return current
            current = current.parent
        raise WorkspaceNotFoundError(
            f"No .missionforge workspace found from {start}"
        )
    
    def mission_path(self, mission_id: str) -> Path:
        """Get path to mission directory."""
        return self.missions_dir / mission_id
    
    def exists(self) -> bool:
        """Check if workspace is initialized."""
        return self.workspace_dir.exists()
```

**Key Features:**
- Works from any subdirectory (walks up to find `.missionforge/`)
- Lazy initialization (only searches when needed)
- Clear error messages with suggested fixes
- Testable without filesystem (can mock Path)

---

### 3.2 Configuration Management

**File**: `src/missionforge/core/config.py`

```python
from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, Field

class MissionForgeConfig(BaseModel):
    """User configuration model."""
    
    # Test execution
    test_timeout: int = Field(default=300, description="Test timeout in seconds")
    test_retry_count: int = Field(default=0, description="Number of test retries")
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[Path] = Field(default=None, description="Log file path")
    
    # Git operations
    git_diff_context: int = Field(default=3, description="Lines of context in diffs")
    
    # Plugins
    plugin_dirs: list[Path] = Field(default_factory=list, description="Additional plugin directories")
    disabled_plugins: list[str] = Field(default_factory=list, description="Disabled plugin names")
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "MissionForgeConfig":
        """Load config from file or use defaults."""
        if config_path and config_path.exists():
            with open(config_path) as f:
                data = yaml.safe_load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: Path) -> None:
        """Save config to file."""
        with open(config_path, 'w') as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)
```

**Key Features:**
- Optional (works without config file)
- Type-safe with Pydantic validation
- Extensible for future settings
- Can be overridden by CLI flags

---

### 3.3 Exception Hierarchy

**File**: `src/missionforge/core/exceptions.py`

```python
class MissionForgeError(Exception):
    """Base exception for all MissionForge errors."""
    
    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(message)
    
    def format_error(self) -> str:
        """Format error with suggestion."""
        msg = f"❌ {self.message}"
        if self.suggestion:
            msg += f"\n💡 Suggestion: {self.suggestion}"
        return msg

class WorkspaceNotFoundError(MissionForgeError):
    """Raised when .missionforge workspace not found."""
    
    def __init__(self, path: str):
        super().__init__(
            f"No .missionforge workspace found from {path}",
            "Run 'missionforge init <mission-id>' to create a workspace"
        )

class InvalidMissionIDError(MissionForgeError):
    """Raised when mission ID format is invalid."""
    
    def __init__(self, mission_id: str):
        super().__init__(
            f"Invalid mission ID: {mission_id}",
            "Mission IDs must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001, FG-042A)"
        )

class ValidationError(MissionForgeError):
    """Raised when validation fails."""
    pass

class GitOperationError(MissionForgeError):
    """Raised when git operation fails."""
    pass

class TestExecutionError(MissionForgeError):
    """Raised when test execution fails."""
    pass
```

**Key Features:**
- Hierarchical (easy to catch specific errors)
- Built-in suggestions for common fixes
- Rich formatting support
- Extensible for plugins

---

### 3.4 Logging Strategy

**File**: `src/missionforge/core/logging.py`

```python
import logging
import sys
from pathlib import Path
from typing import Optional
from rich.logging import RichHandler

def setup_logging(
    level: str = "INFO",
    log_file: Optional[Path] = None,
    rich_output: bool = True
) -> logging.Logger:
    """Configure logging with Rich handler."""
    
    logger = logging.getLogger("missionforge")
    logger.setLevel(level.upper())
    
    # Console handler with Rich
    if rich_output:
        console_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            show_path=False
        )
    else:
        console_handler = logging.StreamHandler(sys.stdout)
    
    console_handler.setLevel(level.upper())
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel("DEBUG")  # Always debug in file
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger
```

**Key Features:**
- Rich terminal output with colors and formatting
- Optional file logging for debugging
- Separate log levels for console vs file
- Structured logging ready for future JSON output

---

## 4. Plugin Architecture

### 4.1 Plugin Base Classes

**File**: `src/missionforge/plugins/base.py`

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel

class Plugin(ABC):
    """Base class for all plugins."""
    
    name: str
    version: str
    description: str
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with configuration."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass

class ValidatorPlugin(Plugin):
    """Base class for custom validators."""
    
    @abstractmethod
    def validate(self, data: BaseModel) -> list[str]:
        """Validate data and return list of error messages."""
        pass

class MetricCollectorPlugin(Plugin):
    """Base class for custom metric collectors."""
    
    @abstractmethod
    def collect(self, mission_id: str) -> Dict[str, Any]:
        """Collect metrics for a mission."""
        pass

class FormatterPlugin(Plugin):
    """Base class for custom report formatters."""
    
    @abstractmethod
    def format(self, data: Dict[str, Any]) -> str:
        """Format report data to string."""
        pass

class CommandPlugin(Plugin):
    """Base class for custom CLI commands."""
    
    @abstractmethod
    def register(self, app: Any) -> None:
        """Register command with Typer app."""
        pass
```

### 4.2 Plugin Registry

**File**: `src/missionforge/plugins/registry.py`

```python
from pathlib import Path
from typing import Dict, List, Type
import importlib.util
import inspect
from .base import Plugin

class PluginRegistry:
    """Discovers and manages plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
    
    def discover(self, plugin_dirs: List[Path]) -> None:
        """Discover plugins in specified directories."""
        for plugin_dir in plugin_dirs:
            if not plugin_dir.exists():
                continue
            
            for py_file in plugin_dir.glob("*.py"):
                if py_file.name.startswith("_"):
                    continue
                
                self._load_plugin_from_file(py_file)
    
    def _load_plugin_from_file(self, file_path: Path) -> None:
        """Load plugin from Python file."""
        spec = importlib.util.spec_from_file_location(
            file_path.stem, file_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find Plugin subclasses
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, Plugin) and 
                    obj is not Plugin):
                    plugin = obj()
                    self._plugins[plugin.name] = plugin
    
    def get(self, name: str) -> Plugin:
        """Get plugin by name."""
        return self._plugins.get(name)
    
    def list_plugins(self, plugin_type: Type[Plugin] = None) -> List[Plugin]:
        """List all plugins or plugins of specific type."""
        if plugin_type:
            return [p for p in self._plugins.values() 
                   if isinstance(p, plugin_type)]
        return list(self._plugins.values())
```

**Key Features:**
- Automatic plugin discovery from directories
- Type-based plugin filtering
- Lazy loading (only load when needed)
- Extensible for future plugin types

---

## 5. CLI Command Structure

### 5.1 Main App

**File**: `src/missionforge/cli/app.py`

```python
import typer
from rich.console import Console
from pathlib import Path
from typing import Optional

from ..core.workspace import Workspace
from ..core.config import MissionForgeConfig
from ..core.logging import setup_logging
from ..core.exceptions import MissionForgeError
from .commands import workspace, mission, baseline, report

app = typer.Typer(
    name="missionforge",
    help="AI-assisted mission decomposition and validation",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()

# Global state
_workspace: Optional[Workspace] = None
_config: Optional[MissionForgeConfig] = None

def get_workspace() -> Workspace:
    """Get or create workspace instance."""
    global _workspace
    if _workspace is None:
        _workspace = Workspace()
    return _workspace

def get_config() -> MissionForgeConfig:
    """Get or create config instance."""
    global _config
    if _config is None:
        config_path = Path.home() / ".missionforge.config.yaml"
        _config = MissionForgeConfig.load(config_path)
    return _config

# Register command groups
app.add_typer(workspace.app, name="workspace")
app.add_typer(mission.app, name="mission")
app.add_typer(baseline.app, name="baseline")
app.add_typer(report.app, name="report")

@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    log_file: Optional[Path] = typer.Option(None, "--log-file", help="Log to file"),
):
    """MissionForge CLI - AI-assisted mission management."""
    
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(level=log_level, log_file=log_file)
    
    # Store in context for commands
    ctx.obj = {
        "workspace": get_workspace,
        "config": get_config,
        "console": console
    }

@app.command()
def version():
    """Show version information."""
    console.print("[bold]MissionForge[/bold] v0.1.0")
    console.print("Python 3.11+ required")

def cli_main():
    """Entry point with error handling."""
    try:
        app()
    except MissionForgeError as e:
        console.print(e.format_error(), style="bold red")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    cli_main()
```

### 5.2 Command Group Example

**File**: `src/missionforge/cli/commands/workspace.py`

```python
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path

from ...core.workspace import Workspace
from ...core.exceptions import InvalidMissionIDError
from ...utils.validation import validate_mission_id

app = typer.Typer(help="Workspace management commands")
console = Console()

@app.command("init")
def init_workspace(
    mission_id: str = typer.Argument(..., help="Mission ID (e.g., MF-001)"),
    force: bool = typer.Option(False, "--force", help="Overwrite existing mission"),
):
    """Initialize a new mission workspace."""
    
    # Validate mission ID
    if not validate_mission_id(mission_id):
        raise InvalidMissionIDError(mission_id)
    
    workspace = Workspace()
    mission_path = workspace.mission_path(mission_id)
    
    if mission_path.exists() and not force:
        console.print(
            f"[yellow]Mission {mission_id} already exists[/yellow]",
            f"\nUse --force to overwrite"
        )
        raise typer.Exit(1)
    
    # Create directory structure
    mission_path.mkdir(parents=True, exist_ok=True)
    (mission_path / "sub-missions").mkdir(exist_ok=True)
    
    # Create template files
    _create_mission_template(mission_path / "mission.yaml", mission_id)
    _create_plan_template(mission_path / "plan.yaml")
    (mission_path / "report.md").touch()
    
    console.print(f"[green]✓[/green] Initialized mission {mission_id}")
    console.print(f"\n[bold]Next steps:[/bold]")
    console.print(f"1. Edit {mission_path / 'mission.yaml'}")
    console.print(f"2. Run: missionforge mission {mission_id} --validate")

@app.command("status")
def workspace_status():
    """Show workspace status and missions."""
    
    workspace = Workspace()
    
    if not workspace.exists():
        console.print("[yellow]No workspace initialized[/yellow]")
        console.print("Run: missionforge workspace init <mission-id>")
        raise typer.Exit(1)
    
    # List missions
    missions = list(workspace.missions_dir.glob("*/mission.yaml"))
    
    if not missions:
        console.print("[yellow]No missions found[/yellow]")
        return
    
    table = Table(title="Missions")
    table.add_column("Mission ID", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Sub-missions", justify="right")
    
    for mission_file in missions:
        mission_id = mission_file.parent.name
        sub_missions = list((mission_file.parent / "sub-missions").glob("*.yaml"))
        table.add_row(mission_id, "Active", str(len(sub_missions)))
    
    console.print(table)

def _create_mission_template(path: Path, mission_id: str):
    """Create mission.yaml template."""
    template = f"""# Mission: {mission_id}
id: {mission_id}
goal: |
  Describe the high-level goal of this mission.
  What should be accomplished?

# Paths that sub-missions cannot modify
forbidden_paths:
  - "core/**"
  - "config/**"

# Aggregate metrics to validate across all sub-missions
aggregate_metrics:
  total_files_changed:
    max: 50
  total_lines_changed:
    max: 1000

# Test command to validate mission completion
test_command: "pytest tests/"

# Sub-missions will be listed here after decomposition
sub_missions: []
"""
    path.write_text(template)

def _create_plan_template(path: Path):
    """Create plan.yaml template."""
    template = """# Execution plan (generated by 'missionforge plan')
execution_order: []
dependency_graph: {}
"""
    path.write_text(template)
```

---

## 6. Git Operations (No GitPython)

**File**: `src/missionforge/git/operations.py`

```python
import subprocess
from pathlib import Path
from typing import List, Optional
from ..core.exceptions import GitOperationError

def run_git_command(
    args: List[str],
    cwd: Optional[Path] = None,
    check: bool = True
) -> subprocess.CompletedProcess:
    """Run git command safely via subprocess."""
    
    cmd = ["git"] + args
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
            timeout=30
        )
        return result
    except subprocess.CalledProcessError as e:
        raise GitOperationError(
            f"Git command failed: {' '.join(cmd)}",
            f"Error: {e.stderr}"
        )
    except subprocess.TimeoutExpired:
        raise GitOperationError(
            f"Git command timed out: {' '.join(cmd)}",
            "Consider increasing timeout or checking repository state"
        )

def get_changed_files(
    base_ref: str = "HEAD",
    cwd: Optional[Path] = None
) -> List[Path]:
    """Get list of changed files since base_ref."""
    
    result = run_git_command(
        ["diff", "--name-only", base_ref],
        cwd=cwd
    )
    
    files = [Path(line) for line in result.stdout.strip().split("\n") if line]
    return files

def get_repo_root(cwd: Optional[Path] = None) -> Path:
    """Get git repository root directory."""
    
    result = run_git_command(
        ["rev-parse", "--show-toplevel"],
        cwd=cwd
    )
    
    return Path(result.stdout.strip())

def is_git_repo(cwd: Optional[Path] = None) -> bool:
    """Check if directory is a git repository."""
    
    result = run_git_command(
        ["rev-parse", "--git-dir"],
        cwd=cwd,
        check=False
    )
    
    return result.returncode == 0
```

**Key Features:**
- No shell injection (uses list arguments)
- Timeout protection
- Clear error messages
- Works from any directory in repo

---

## 7. Implementation Phases

### Phase 1: Core Infrastructure (2-3 hours)

1. **Setup project structure** (30 min)
   - Create directory layout
   - Setup pyproject.toml
   - Configure dev tools (black, ruff, mypy)

2. **Implement core modules** (1 hour)
   - Workspace path resolution
   - Config management
   - Exception hierarchy
   - Logging setup

3. **Basic CLI skeleton** (1 hour)
   - Main Typer app
   - Command groups structure
   - Global error handling
   - Help text and version command

4. **Testing setup** (30 min)
   - Pytest configuration
   - Basic fixtures
   - Mock utilities

### Phase 2: Essential Commands (1-2 hours)

1. **Workspace commands** (45 min)
   - `init` command with templates
   - `status` command with Rich tables

2. **Git utilities** (45 min)
   - Safe subprocess wrappers
   - Changed files detection
   - Repo validation

3. **Integration tests** (30 min)
   - End-to-end CLI tests
   - Workspace creation flow

### Phase 3: Plugin System (1 hour)

1. **Plugin base classes** (30 min)
2. **Plugin registry** (30 min)
3. **Example plugins** (optional)

---

## 8. Testing Strategy

### Unit Tests
```python
# tests/unit/test_workspace.py
def test_workspace_finds_root(tmp_path):
    """Test workspace root discovery."""
    workspace_dir = tmp_path / ".missionforge"
    workspace_dir.mkdir()
    
    # Should find from subdirectory
    subdir = tmp_path / "src" / "app"
    subdir.mkdir(parents=True)
    
    ws = Workspace(start_path=subdir)
    assert ws.root == tmp_path

def test_workspace_not_found_raises_error(tmp_path):
    """Test error when workspace not found."""
    with pytest.raises(WorkspaceNotFoundError):
        Workspace(start_path=tmp_path)
```

### Integration Tests
```python
# tests/integration/test_cli_commands.py
def test_init_command_creates_structure(runner, tmp_path):
    """Test init command creates proper structure."""
    result = runner.invoke(app, ["workspace", "init", "MF-001"])
    
    assert result.exit_code == 0
    assert (tmp_path / ".missionforge" / "missions" / "MF-001").exists()
    assert (tmp_path / ".missionforge" / "missions" / "MF-001" / "mission.yaml").exists()
```

---

## 9. Documentation Requirements

### User Documentation
- **README.md**: Quick start guide
- **docs/installation.md**: Installation instructions
- **docs/commands.md**: Command reference
- **docs/configuration.md**: Config file format

### Developer Documentation
- **docs/architecture.md**: System architecture
- **docs/plugin_development.md**: Plugin development guide
- **docs/contributing.md**: Contribution guidelines

---

## 10. Success Metrics

### Functional Requirements
- ✅ CLI runs from any subdirectory
- ✅ Clear error messages with suggestions
- ✅ Help text is comprehensive
- ✅ Workspace initialization works
- ✅ Config file is optional

### Non-Functional Requirements
- ✅ Test coverage > 80%
- ✅ Type hints on all public APIs
- ✅ Passes mypy strict mode
- ✅ Formatted with black
- ✅ Linted with ruff

### Maintainability
- ✅ Clear separation of concerns
- ✅ Plugin system for extensions
- ✅ Comprehensive documentation
- ✅ Easy to add new commands

---

## 11. Future Extension Points

### Planned Extensions
1. **Custom Validators**: Language-specific validation plugins
2. **Metric Collectors**: Code complexity, test coverage, etc.
3. **Report Formatters**: HTML, PDF, JSON outputs
4. **Command Plugins**: Custom workflow commands
5. **Bob Integration**: Slash commands and skills

### Extension Example
```python
# plugins/validators/python_validator.py
from missionforge.plugins.base import ValidatorPlugin

class PythonValidator(ValidatorPlugin):
    name = "python"
    version = "1.0.0"
    description = "Python-specific validation"
    
    def validate(self, data):
        errors = []
        # Check Python-specific rules
        return errors
```

---

## 12. Risk Mitigation

### Technical Risks
1. **Git subprocess failures**: Comprehensive error handling + timeouts
2. **Path resolution issues**: Extensive testing on different OS
3. **Plugin conflicts**: Namespace isolation + version checks
4. **Config file corruption**: Schema validation + backup

### Hackathon Risks
1. **Time constraints**: Prioritize core features, defer plugins
2. **Integration issues**: Clear API contracts between modules
3. **Testing time**: Focus on critical path tests first

---

## Summary

This plan provides a **solid, maintainable foundation** for MissionForge CLI with:

✅ **Modern Python practices** (Typer, Pydantic, Rich)
✅ **Clear architecture** (separation of concerns, plugin system)
✅ **Extensibility** (4 plugin types for future integrations)
✅ **Safety** (no shell injection, comprehensive error handling)
✅ **Developer experience** (type hints, clear errors, good docs)
✅ **Testability** (high coverage, clear fixtures)

**Estimated effort**: 4-6 hours for full implementation with tests and docs.