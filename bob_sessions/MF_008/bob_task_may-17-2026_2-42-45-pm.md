**User:**

<task>
Implement Phase 2 of MF-008: Core Service Layer

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. Phase 1 (data models) and Phase 4 (infrastructure) are complete. Now we need to create the core service layer that implements the business logic.

**Your Task:**
Create a new file `src/missionforge/core/baseline_service.py` with the BaselineService class that implements:

1. **capture_baseline(sub_mission_id, force=False) -> Path**:
   - Read sub-mission.yaml using SchemaValidator
   - Extract metrics dictionary from SubMission model
   - For each metric, create SubMissionBaselineMetric with baseline_target from metric definition
   - Set value to None for Bob to fill
   - Create SubMissionBaseline with status="captured"
   - Write to baseline.todo.json
   - Raise BaselineAlreadyExistsError if baseline.json exists (unless force=True)
   - Return path to baseline.todo.json

2. **commit_baseline(sub_mission_id) -> Path**:
   - Read baseline.todo.json
   - Validate all metric values are filled (not None)
   - Validate value types match baseline_target types
   - Add timestamp (ISO 8601 UTC) and status="committed"
   - Write to baseline.json
   - Make file read-only using os.chmod (stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
   - Raise BaselineNotCapturedError if baseline.todo.json doesn't exist
   - Raise BaselineIncompleteError if any values are None
   - Raise BaselineValidationError if type mismatch
   - Return path to baseline.json

3. **reset_baseline(sub_mission_id, force=False) -> None**:
   - Remove baseline.todo.json if exists
   - Remove baseline.json if exists (requires force=True if read-only)
   - Raise error if no baseline files exist

**Implementation Requirements:**

```python
"""Baseline capture and commit service."""

import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..models.schemas import SubMissionBaseline, SubMissionBaselineMetric
from ..schemas.validators import SchemaValidator
from .exceptions import (
    BaselineAlreadyExistsError,
    BaselineIncompleteError,
    BaselineNotCapturedError,
    BaselineValidationError,
)
from .workspace import Workspace


class BaselineService:
    """Service for baseline capture and commit operations."""
    
    def __init__(self, workspace: Workspace | None = None):
        """Initialize service with workspace."""
        self.workspace = workspace or Workspace()
```

**Key Implementation Details:**

- Use `SchemaValidator.validate_sub_mission_file()` to read sub-mission.yaml
- Extract metrics from SubMission.metrics (dict[str, MetricDefinition])
- For each metric_id, get the target value from MetricDefinition.target
- Use `baseline_target = metric_def.target` for each metric
- Type validation: `type(value) == type(baseline_target)`
- Timestamp format: `datetime.now(timezone.utc).isoformat()`
- File permissions: `os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)`

**Scope:**
- Create NEW file `src/missionforge/core/baseline_service.py`
- Implement all three methods with complete error handling
- Add comprehensive docstrings
- Follow existing code style from other core modules

When complete, use `attempt_completion` with a summary of the implementation.
</task>
<environment_details>
# VSCode Visible Files
src/missionforge/core/workspace.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:42:00.959Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (/Users/benny/Mission-Forge) Files
.gitignore
pyproject.toml
README.md
.claude/
.github/
bob_sessions/
bob_sessions/MF_001/
bob_sessions/MF_001/001.png
bob_sessions/MF_001/002.png
bob_sessions/MF_001/003.png
bob_sessions/MF_001/bob_task_may-17-2026_3-30-34-am.md
bob_sessions/MF_001/bob_task_may-17-2026_3-57-48-am.md
bob_sessions/MF_001/bob_task_may-17-2026_4-15-08-am.md
bob_sessions/MF_001/session-2026-05-16T16-22-c5f971d9.json
bob_sessions/MF_001/session-2026-05-16T16-59-c5f971d9.json
bob_sessions/MF-002/
bob_sessions/MF-002/bob_task_may-17-2026_10-13-36-am.md
bob_sessions/MF-002/mf_002_consumption_summary.png
bob_sessions/MF-003/
bob_sessions/MF-003/bob_task_may-17-2026_1-20-04-pm.md
bob_sessions/MF-003/bob_task_may-17-2026_1-20-04-pm.png
bob_sessions/MF-003/bob_task_may-17-2026_1-42-53-pm.md
bob_sessions/MF-003/bob_task_may-17-2026_1-42-53-pm.png
docs/
docs/schemas/
docs/schemas/mission-schema-examples.md
src/
src/missionforge/
src/missionforge/__init__.py
src/missionforge/__main__.py
src/missionforge/cli/
src/missionforge/cli/__init__.py
src/missionforge/cli/app.py
src/missionforge/cli/commands/
src/missionforge/cli/commands/__init__.py
src/missionforge/cli/commands/workspace.py
src/missionforge/cli/utils/
src/missionforge/cli/utils/__init__.py
src/missionforge/cli/utils/validation.py
src/missionforge/core/
src/missionforge/core/__init__.py
src/missionforge/core/config.py
src/missionforge/core/exceptions.py
src/missionforge/core/logging.py
src/missionforge/core/workspace.py
src/missionforge/git/
src/missionforge/git/__init__.py
src/missionforge/git/operations.py
src/missionforge/models/
src/missionforge/models/__init__.py
src/missionforge/models/schemas.py
src/missionforge/plugins/
src/missionforge/plugins/__init__.py
src/missionforge/plugins/base.py
src/missionforge/plugins/registry.py
src/missionforge/plugins/commands/
src/missionforge/plugins/commands/__init__.py
src/missionforge/plugins/formatters/
src/missionforge/plugins/formatters/__init__.py
src/missionforge/plugins/metrics/
src/missionforge/plugins/metrics/__init__.py
src/missionforge/plugins/validators/
src/missionforge/plugins/validators/__init__.py
src/missionforge/schemas/
src/missionforge/schemas/__init__.py
src/missionforge/schemas/json_schemas.py
src/missionforge/schemas/validators.py
src/missionforge/testing/
src/missionforge/testing/__init__.py
src/missionforge/testing/executor.py
src/missionforge/utils/
src/missionforge/utils/__init__.py
src/missionforge/utils/path_matching.py
src/missionforge/utils/subprocess_utils.py
tests/
tests/__init__.py
tests/conftest.py
tests/test_git_operations.py
tests/test_path_matching.py
tests/test_subprocess_utils.py
tests/test_test_executor.py
tests/integration/
tests/integration/__init__.py
tests/integration/test_cli_commands.py
tests/unit/
tests/unit/__init__.py
tests/unit/test_config.py
tests/unit/test_workspace.py
tests/unit/models/
tests/unit/models/__init__.py
tests/unit/models/test_schemas.py
tests/unit/schemas/
tests/unit/schemas/__init__.py
tests/unit/schemas/test_validators.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll implement the BaselineService class with all three methods. Let me start by reading the relevant files to understand the existing structure and dependencies.

<read_file>
<args>
<file>
<path>src/missionforge/core/exceptions.py</path>
</file>
<file>
<path>src/missionforge/core/workspace.py</path>
</file>
<file>
<path>src/missionforge/models/schemas.py</path>
</file>
<file>
<path>src/missionforge/schemas/validators.py</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>src/missionforge/core/exceptions.py</path>
<content lines="1-107">
  1 | """Custom exception hierarchy for MissionForge."""
  2 | 
  3 | 
  4 | class MissionForgeError(Exception):
  5 |     """Base exception for all MissionForge errors."""
  6 | 
  7 |     def __init__(self, message: str, suggestion: str | None = None):
  8 |         self.message = message
  9 |         self.suggestion = suggestion
 10 |         super().__init__(message)
 11 | 
 12 |     def format_error(self) -> str:
 13 |         """Format error with suggestion."""
 14 |         msg = f"❌ {self.message}"
 15 |         if self.suggestion:
 16 |             msg += f"\n💡 Suggestion: {self.suggestion}"
 17 |         return msg
 18 | 
 19 | 
 20 | class WorkspaceNotFoundError(MissionForgeError):
 21 |     """Raised when .missionforge workspace not found."""
 22 | 
 23 |     def __init__(self, path: str):
 24 |         super().__init__(
 25 |             f"No .missionforge workspace found from {path}",
 26 |             "Run 'missionforge workspace init <mission-id>' to create a workspace",
 27 |         )
 28 | 
 29 | 
 30 | class InvalidMissionIDError(MissionForgeError):
 31 |     """Raised when mission ID format is invalid."""
 32 | 
 33 |     def __init__(self, mission_id: str):
 34 |         super().__init__(
 35 |             f"Invalid mission ID: {mission_id}",
 36 |             "Mission IDs must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001, FG-042A)",
 37 |         )
 38 | 
 39 | 
 40 | class ValidationError(MissionForgeError):
 41 |     """Raised when validation fails."""
 42 | 
 43 |     pass
 44 | 
 45 | 
 46 | class GitOperationError(MissionForgeError):
 47 |     """Raised when git operation fails."""
 48 | 
 49 |     pass
 50 | 
 51 | 
 52 | class TestExecutionError(MissionForgeError):
 53 |     """Raised when test execution fails."""
 54 | 
 55 |     pass
 56 | 
 57 | 
 58 | class ConfigurationError(MissionForgeError):
 59 |     """Raised when configuration is invalid."""
 60 | 
 61 |     pass
 62 | 
 63 | 
 64 | class PluginError(MissionForgeError):
 65 |     """Raised when plugin operation fails."""
 66 | 
 67 |     pass
 68 | 
 69 | 
 70 | class BaselineAlreadyExistsError(MissionForgeError):
 71 |     """Raised when baseline already committed."""
 72 | 
 73 |     def __init__(self, sub_mission_id: str, baseline_path: str):
 74 |         super().__init__(
 75 |             f"Baseline already exists for {sub_mission_id} at {baseline_path}",
 76 |             "Use 'missionforge baseline reset <id> --force' to remove and re-capture",
 77 |         )
 78 | 
 79 | 
 80 | class BaselineNotCapturedError(MissionForgeError):
 81 |     """Raised when trying to commit without capture."""
 82 | 
 83 |     def __init__(self, sub_mission_id: str):
 84 |         super().__init__(
 85 |             f"No baseline.todo.json found for {sub_mission_id}",
 86 |             "Run 'missionforge baseline capture <id>' first to generate baseline.todo.json",
 87 |         )
 88 | 
 89 | 
 90 | class BaselineValidationError(MissionForgeError):
 91 |     """Raised when baseline validation fails."""
 92 | 
 93 |     pass
 94 | 
 95 | 
 96 | class BaselineIncompleteError(MissionForgeError):
 97 |     """Raised when baseline has unfilled values."""
 98 | 
 99 |     def __init__(self, sub_mission_id: str, unfilled_metrics: list[str]):
100 |         metrics_list = "\n  • ".join(unfilled_metrics)
101 |         super().__init__(
102 |             f"Baseline for {sub_mission_id} has unfilled metric values:\n  • {metrics_list}",
103 |             "Fill all metric values in baseline.todo.json before committing",
104 |         )
105 | 
106 | 
107 | # Made with Bob
</content>
</file>
<file><path>src/missionforge/core/workspace.py</path>
<content lines="1-126">
  1 | """Workspace path resolution and management."""
  2 | 
  3 | from pathlib import Path
  4 | 
  5 | from .exceptions import WorkspaceNotFoundError
  6 | 
  7 | 
  8 | class Workspace:
  9 |     """Manages .missionforge workspace discovery and paths."""
 10 | 
 11 |     WORKSPACE_DIR = ".missionforge"
 12 |     MISSIONS_DIR = "missions"
 13 | 
 14 |     def __init__(self, start_path: Path | None = None):
 15 |         """Initialize workspace from start path.
 16 | 
 17 |         Args:
 18 |             start_path: Starting directory for workspace search. Defaults to current directory.
 19 | 
 20 |         Raises:
 21 |             WorkspaceNotFoundError: If no .missionforge workspace found.
 22 |         """
 23 |         self.root = self._find_workspace_root(start_path or Path.cwd())
 24 |         self.workspace_dir = self.root / self.WORKSPACE_DIR
 25 |         self.missions_dir = self.workspace_dir / self.MISSIONS_DIR
 26 | 
 27 |     def _find_workspace_root(self, start: Path) -> Path:
 28 |         """Walk up directory tree to find .missionforge/.
 29 | 
 30 |         Args:
 31 |             start: Starting directory for search.
 32 | 
 33 |         Returns:
 34 |             Path to workspace root directory.
 35 | 
 36 |         Raises:
 37 |             WorkspaceNotFoundError: If no workspace found.
 38 |         """
 39 |         current = start.resolve()
 40 |         while current != current.parent:
 41 |             if (current / self.WORKSPACE_DIR).is_dir():
 42 |                 return current
 43 |             current = current.parent
 44 |         raise WorkspaceNotFoundError(str(start))
 45 | 
 46 |     def mission_path(self, mission_id: str) -> Path:
 47 |         """Get path to mission directory.
 48 | 
 49 |         Args:
 50 |             mission_id: Mission identifier (e.g., 'MF-001').
 51 | 
 52 |         Returns:
 53 |             Path to mission directory.
 54 |         """
 55 |         return self.missions_dir / mission_id
 56 | 
 57 |     def sub_mission_path(self, mission_id: str, sub_mission_id: str) -> Path:
 58 |         """Get path to sub-mission directory.
 59 | 
 60 |         Args:
 61 |             mission_id: Parent mission identifier.
 62 |             sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
 63 | 
 64 |         Returns:
 65 |             Path to sub-mission directory.
 66 |         """
 67 |         return self.mission_path(mission_id) / "sub-missions" / sub_mission_id
 68 | 
 69 |     def exists(self) -> bool:
 70 |         """Check if workspace is initialized.
 71 | 
 72 |         Returns:
 73 |             True if workspace directory exists.
 74 |         """
 75 |         return self.workspace_dir.exists()
 76 | 
 77 |     def initialize(self) -> None:
 78 |         """Initialize workspace directory structure.
 79 | 
 80 |         Creates .missionforge/missions/ directory structure.
 81 |         """
 82 |         self.missions_dir.mkdir(parents=True, exist_ok=True)
 83 | 
 84 |     def list_missions(self) -> list[str]:
 85 |         """List all mission IDs in workspace.
 86 | 
 87 |         Returns:
 88 |             List of mission IDs.
 89 |         """
 90 |         if not self.missions_dir.exists():
 91 |             return []
 92 | 
 93 |         missions = []
 94 |         for mission_dir in self.missions_dir.iterdir():
 95 |             if mission_dir.is_dir() and (mission_dir / "mission.yaml").exists():
 96 |                 missions.append(mission_dir.name)
 97 |         return sorted(missions)
 98 | 
 99 |     def baseline_todo_path(self, sub_mission_id: str) -> Path:
100 |         """Get path to baseline.todo.json for a sub-mission.
101 | 
102 |         Args:
103 |             sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
104 | 
105 |         Returns:
106 |             Path to baseline.todo.json file.
107 |         """
108 |         # Extract parent mission ID (e.g., "MF-001-A" -> "MF-001")
109 |         parent_id = sub_mission_id.rsplit("-", 1)[0]
110 |         return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.todo.json"
111 | 
112 |     def baseline_path(self, sub_mission_id: str) -> Path:
113 |         """Get path to baseline.json for a sub-mission.
114 | 
115 |         Args:
116 |             sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
117 | 
118 |         Returns:
119 |             Path to baseline.json file.
120 |         """
121 |         # Extract parent mission ID (e.g., "MF-001-A" -> "MF-001")
122 |         parent_id = sub_mission_id.rsplit("-", 1)[0]
123 |         return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.json"
124 | 
125 | 
126 | # Made with Bob
</content>
</file>
<file><path>src/missionforge/models/schemas.py</path>
<content lines="1-411">
  1 | """Pydantic models for mission schemas."""
  2 | 
  3 | 
  4 | from pydantic import BaseModel, Field, field_validator, model_validator
  5 | 
  6 | 
  7 | class MetricDefinition(BaseModel):
  8 |     """Definition of a metric with constraints."""
  9 | 
 10 |     min: float | None = Field(None, description="Minimum allowed value")
 11 |     max: float | None = Field(None, description="Maximum allowed value")
 12 |     target: float | None = Field(None, description="Target value")
 13 | 
 14 |     @model_validator(mode="after")
 15 |     def validate_constraints(self) -> "MetricDefinition":
 16 |         """Ensure at least one constraint is defined."""
 17 |         if self.min is None and self.max is None and self.target is None:
 18 |             raise ValueError("At least one of min, max, or target must be specified")
 19 |         if self.min is not None and self.max is not None and self.min > self.max:
 20 |             raise ValueError(f"min ({self.min}) cannot be greater than max ({self.max})")
 21 |         return self
 22 | 
 23 | 
 24 | class ParentMission(BaseModel):
 25 |     """Parent mission schema."""
 26 | 
 27 |     id: str = Field(..., description="Mission identifier (e.g., MF-001)")
 28 |     goal: str = Field(..., description="High-level mission goal")
 29 |     forbidden_paths: list[str] = Field(
 30 |         default_factory=list, description="Path patterns that sub-missions cannot modify"
 31 |     )
 32 |     aggregate_metrics: dict[str, MetricDefinition] = Field(
 33 |         default_factory=dict, description="Aggregate metrics across all sub-missions"
 34 |     )
 35 |     test_command: str | None = Field(
 36 |         None, description="Command to run tests for mission validation"
 37 |     )
 38 |     sub_missions: list[str] = Field(
 39 |         default_factory=list, description="List of sub-mission IDs"
 40 |     )
 41 | 
 42 |     @field_validator("id")
 43 |     @classmethod
 44 |     def validate_mission_id(cls, v: str) -> str:
 45 |         """Validate mission ID format."""
 46 |         import re
 47 | 
 48 |         pattern = r"^[A-Z]{2,4}-\d{3}[A-Z]?$"
 49 |         if not re.match(pattern, v):
 50 |             raise ValueError(
 51 |                 f"Invalid mission ID format: {v}. "
 52 |                 "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001, FG-042A)"
 53 |             )
 54 |         return v
 55 | 
 56 |     @field_validator("goal")
 57 |     @classmethod
 58 |     def validate_goal(cls, v: str) -> str:
 59 |         """Ensure goal is not empty."""
 60 |         if not v.strip():
 61 |             raise ValueError("Mission goal cannot be empty")
 62 |         return v
 63 | 
 64 |     @field_validator("forbidden_paths")
 65 |     @classmethod
 66 |     def validate_forbidden_paths(cls, v: list[str]) -> list[str]:
 67 |         """Validate path glob patterns."""
 68 |         import pathspec
 69 | 
 70 |         for pattern in v:
 71 |             try:
 72 |                 pathspec.PathSpec.from_lines("gitwildmatch", [pattern])
 73 |             except Exception as e:
 74 |                 raise ValueError(f"Invalid path pattern '{pattern}': {e}") from e
 75 |         return v
 76 | 
 77 | 
 78 | class SubMission(BaseModel):
 79 |     """Sub-mission schema."""
 80 | 
 81 |     id: str = Field(..., description="Sub-mission identifier (e.g., MF-001-A)")
 82 |     parent: str = Field(..., description="Parent mission ID")
 83 |     title: str = Field(..., description="Short descriptive title")
 84 |     goal: str = Field(..., description="Specific goal for this sub-mission")
 85 |     depends_on: list[str] = Field(
 86 |         default_factory=list, description="List of sub-mission IDs this depends on"
 87 |     )
 88 |     allowed_paths: list[str] = Field(
 89 |         default_factory=list, description="Path patterns this sub-mission can modify"
 90 |     )
 91 |     metrics: dict[str, MetricDefinition] = Field(
 92 |         default_factory=dict, description="Metrics for this sub-mission"
 93 |     )
 94 |     test_command: str | None = Field(
 95 |         None, description="Command to run tests for this sub-mission"
 96 |     )
 97 | 
 98 |     @field_validator("id")
 99 |     @classmethod
100 |     def validate_sub_mission_id(cls, v: str) -> str:
101 |         """Validate sub-mission ID format."""
102 |         import re
103 | 
104 |         pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
105 |         if not re.match(pattern, v):
106 |             raise ValueError(
107 |                 f"Invalid sub-mission ID format: {v}. "
108 |                 "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}-[A-Z] (e.g., MF-001-A)"
109 |             )
110 |         return v
111 | 
112 |     @field_validator("parent")
113 |     @classmethod
114 |     def validate_parent_id(cls, v: str) -> str:
115 |         """Validate parent mission ID format."""
116 |         import re
117 | 
118 |         pattern = r"^[A-Z]{2,4}-\d{3}[A-Z]?$"
119 |         if not re.match(pattern, v):
120 |             raise ValueError(
121 |                 f"Invalid parent mission ID format: {v}. "
122 |                 "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}[A-Z]? (e.g., MF-001)"
123 |             )
124 |         return v
125 | 
126 |     @field_validator("title")
127 |     @classmethod
128 |     def validate_title(cls, v: str) -> str:
129 |         """Ensure title is not empty."""
130 |         if not v.strip():
131 |             raise ValueError("Sub-mission title cannot be empty")
132 |         return v
133 | 
134 |     @field_validator("goal")
135 |     @classmethod
136 |     def validate_goal(cls, v: str) -> str:
137 |         """Ensure goal is not empty."""
138 |         if not v.strip():
139 |             raise ValueError("Sub-mission goal cannot be empty")
140 |         return v
141 | 
142 |     @field_validator("allowed_paths")
143 |     @classmethod
144 |     def validate_allowed_paths(cls, v: list[str]) -> list[str]:
145 |         """Validate path glob patterns."""
146 |         import pathspec
147 | 
148 |         for pattern in v:
149 |             try:
150 |                 pathspec.PathSpec.from_lines("gitwildmatch", [pattern])
151 |             except Exception as e:
152 |                 raise ValueError(f"Invalid path pattern '{pattern}': {e}") from e
153 |         return v
154 | 
155 |     @model_validator(mode="after")
156 |     def validate_parent_child_relationship(self) -> "SubMission":
157 |         """Ensure sub-mission ID matches parent ID."""
158 |         # Extract parent prefix from sub-mission ID
159 |         parts = self.id.rsplit("-", 1)
160 |         if len(parts) != 2:
161 |             raise ValueError(f"Invalid sub-mission ID format: {self.id}")
162 | 
163 |         expected_parent = parts[0]
164 |         if self.parent != expected_parent:
165 |             raise ValueError(
166 |                 f"Sub-mission ID '{self.id}' does not match parent ID '{self.parent}'. "
167 |                 f"Expected parent: '{expected_parent}'"
168 |             )
169 |         return self
170 | 
171 | 
172 | class BaselineMetrics(BaseModel):
173 |     """Baseline metrics captured before mission starts."""
174 | 
175 |     files_changed: int = Field(..., description="Number of files changed")
176 |     lines_added: int = Field(..., description="Number of lines added")
177 |     lines_removed: int = Field(..., description="Number of lines removed")
178 |     test_coverage: float | None = Field(None, description="Test coverage percentage")
179 |     custom_metrics: dict[str, float] = Field(
180 |         default_factory=dict, description="Custom metrics defined by mission"
181 |     )
182 | 
183 |     @field_validator("files_changed", "lines_added", "lines_removed")
184 |     @classmethod
185 |     def validate_non_negative(cls, v: int) -> int:
186 |         """Ensure counts are non-negative."""
187 |         if v < 0:
188 |             raise ValueError("Metric values cannot be negative")
189 |         return v
190 | 
191 |     @field_validator("test_coverage")
192 |     @classmethod
193 |     def validate_coverage(cls, v: float | None) -> float | None:
194 |         """Ensure coverage is between 0 and 100."""
195 |         if v is not None and (v < 0 or v > 100):
196 |             raise ValueError("Test coverage must be between 0 and 100")
197 |         return v
198 | 
199 | 
200 | class Baseline(BaseModel):
201 |     """Baseline state for a mission or sub-mission."""
202 | 
203 |     mission_id: str = Field(..., description="Mission or sub-mission ID")
204 |     timestamp: str = Field(..., description="ISO 8601 timestamp of baseline capture")
205 |     git_commit: str = Field(..., description="Git commit hash at baseline")
206 |     metrics: BaselineMetrics = Field(..., description="Captured metrics")
207 | 
208 |     @field_validator("git_commit")
209 |     @classmethod
210 |     def validate_git_commit(cls, v: str) -> str:
211 |         """Validate git commit hash format."""
212 |         import re
213 | 
214 |         if not re.match(r"^[0-9a-f]{7,40}$", v):
215 |             raise ValueError(f"Invalid git commit hash: {v}")
216 |         return v
217 | 
218 | 
219 | class ValidationMetrics(BaseModel):
220 |     """Validation metrics captured after mission completion."""
221 | 
222 |     files_changed: int = Field(..., description="Number of files changed")
223 |     lines_added: int = Field(..., description="Number of lines added")
224 |     lines_removed: int = Field(..., description="Number of lines removed")
225 |     test_coverage: float | None = Field(None, description="Test coverage percentage")
226 |     tests_passed: bool = Field(..., description="Whether all tests passed")
227 |     custom_metrics: dict[str, float] = Field(
228 |         default_factory=dict, description="Custom metrics defined by mission"
229 |     )
230 | 
231 |     @field_validator("files_changed", "lines_added", "lines_removed")
232 |     @classmethod
233 |     def validate_non_negative(cls, v: int) -> int:
234 |         """Ensure counts are non-negative."""
235 |         if v < 0:
236 |             raise ValueError("Metric values cannot be negative")
237 |         return v
238 | 
239 |     @field_validator("test_coverage")
240 |     @classmethod
241 |     def validate_coverage(cls, v: float | None) -> float | None:
242 |         """Ensure coverage is between 0 and 100."""
243 |         if v is not None and (v < 0 or v > 100):
244 |             raise ValueError("Test coverage must be between 0 and 100")
245 |         return v
246 | 
247 | 
248 | class Validation(BaseModel):
249 |     """Validation state for a mission or sub-mission."""
250 | 
251 |     mission_id: str = Field(..., description="Mission or sub-mission ID")
252 |     timestamp: str = Field(..., description="ISO 8601 timestamp of validation")
253 |     git_commit: str = Field(..., description="Git commit hash at validation")
254 |     metrics: ValidationMetrics = Field(..., description="Captured metrics")
255 |     passed: bool = Field(..., description="Whether validation passed all checks")
256 |     errors: list[str] = Field(default_factory=list, description="Validation errors if any")
257 | 
258 |     @field_validator("git_commit")
259 |     @classmethod
260 |     def validate_git_commit(cls, v: str) -> str:
261 |         """Validate git commit hash format."""
262 |         import re
263 | 
264 |         if not re.match(r"^[0-9a-f]{7,40}$", v):
265 |             raise ValueError(f"Invalid git commit hash: {v}")
266 |         return v
267 | 
268 | 
269 | class ExecutionPlan(BaseModel):
270 |     """Execution plan with dependency graph."""
271 | 
272 |     execution_order: list[str] = Field(
273 |         default_factory=list, description="Ordered list of sub-mission IDs to execute"
274 |     )
275 |     dependency_graph: dict[str, list[str]] = Field(
276 |         default_factory=dict,
277 |         description="Map of sub-mission ID to list of dependencies",
278 |     )
279 | 
280 |     @model_validator(mode="after")
281 |     def validate_dependencies(self) -> "ExecutionPlan":
282 |         """Validate dependency graph consistency."""
283 |         # Check all dependencies exist in execution order
284 |         all_missions = set(self.execution_order)
285 |         for mission_id, deps in self.dependency_graph.items():
286 |             if mission_id not in all_missions:
287 |                 raise ValueError(
288 |                     f"Mission '{mission_id}' in dependency graph "
289 |                     f"not found in execution order"
290 |                 )
291 |             for dep in deps:
292 |                 if dep not in all_missions:
293 |                     raise ValueError(
294 |                         f"Dependency '{dep}' for mission '{mission_id}' "
295 |                         f"not found in execution order"
296 |                     )
297 | 
298 |         # Check for circular dependencies
299 |         visited = set()
300 |         rec_stack = set()
301 | 
302 |         def has_cycle(node: str) -> bool:
303 |             visited.add(node)
304 |             rec_stack.add(node)
305 | 
306 |             for neighbor in self.dependency_graph.get(node, []):
307 |                 if neighbor not in visited:
308 |                     if has_cycle(neighbor):
309 |                         return True
310 |                 elif neighbor in rec_stack:
311 |                     return True
312 | 
313 |             rec_stack.remove(node)
314 |             return False
315 | 
316 |         for mission_id in self.dependency_graph:
317 |             if mission_id not in visited:
318 |                 if has_cycle(mission_id):
319 |                     raise ValueError("Circular dependency detected in execution plan")
320 | 
321 |         return self
322 | 
323 | class SubMissionBaselineMetric(BaseModel):
324 |     """A single metric in a sub-mission baseline."""
325 | 
326 |     metric_id: str = Field(..., description="Unique identifier for the metric")
327 |     description: str = Field(..., description="Human-readable description of what is measured")
328 |     baseline_target: bool | int | float | str = Field(
329 |         ..., description="Expected baseline value before implementation"
330 |     )
331 |     value: bool | int | float | str | None = Field(
332 |         None, description="Actual measured value (null until filled by Bob)"
333 |     )
334 | 
335 |     @field_validator("metric_id")
336 |     @classmethod
337 |     def validate_metric_id(cls, v: str) -> str:
338 |         """Ensure metric_id is not empty."""
339 |         if not v.strip():
340 |             raise ValueError("metric_id cannot be empty")
341 |         return v
342 | 
343 |     @field_validator("description")
344 |     @classmethod
345 |     def validate_description(cls, v: str) -> str:
346 |         """Ensure description is not empty."""
347 |         if not v.strip():
348 |             raise ValueError("description cannot be empty")
349 |         return v
350 | 
351 |     @model_validator(mode="after")
352 |     def validate_value_type(self) -> "SubMissionBaselineMetric":
353 |         """Ensure value type matches baseline_target type when value is not None."""
354 |         if self.value is not None:
355 |             target_type = type(self.baseline_target)
356 |             value_type = type(self.value)
357 |             if target_type != value_type:
358 |                 raise ValueError(
359 |                     f"Value type ({value_type.__name__}) does not match "
360 |                     f"baseline_target type ({target_type.__name__})"
361 |                 )
362 |         return self
363 | 
364 | 
365 | class SubMissionBaseline(BaseModel):
366 |     """Baseline for sub-mission custom metrics."""
367 | 
368 |     sub_mission_id: str = Field(..., description="Sub-mission identifier (e.g., MF-001-A)")
369 |     timestamp: str | None = Field(
370 |         None, description="ISO 8601 timestamp when baseline was committed"
371 |     )
372 |     status: str | None = Field(
373 |         None, description="Baseline status: 'captured' or 'committed'"
374 |     )
375 |     metrics: list[SubMissionBaselineMetric] = Field(
376 |         ..., description="List of baseline metrics"
377 |     )
378 | 
379 |     @field_validator("sub_mission_id")
380 |     @classmethod
381 |     def validate_sub_mission_id(cls, v: str) -> str:
382 |         """Validate sub-mission ID format."""
383 |         import re
384 | 
385 |         pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
386 |         if not re.match(pattern, v):
387 |             raise ValueError(
388 |                 f"Invalid sub-mission ID format: {v}. "
389 |                 "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}-[A-Z] (e.g., MF-001-A)"
390 |             )
391 |         return v
392 | 
393 |     @field_validator("status")
394 |     @classmethod
395 |     def validate_status(cls, v: str | None) -> str | None:
396 |         """Validate status is one of allowed values."""
397 |         if v is not None and v not in ("captured", "committed"):
398 |             raise ValueError(f"Invalid status: {v}. Must be 'captured' or 'committed'")
399 |         return v
400 | 
401 |     @field_validator("metrics")
402 |     @classmethod
403 |     def validate_metrics_not_empty(cls, v: list[SubMissionBaselineMetric]) -> list[SubMissionBaselineMetric]:
404 |         """Ensure at least one metric is defined."""
405 |         if not v:
406 |             raise ValueError("At least one metric must be defined")
407 |         return v
408 | 
409 | 
410 | 
411 | # Made with Bob
</content>
</file>
<file><path>src/missionforge/schemas/validators.py</path>
<content lines="1-412">
  1 | """Schema validators for mission files."""
  2 | 
  3 | # ruff: noqa: B904
  4 | 
  5 | import json
  6 | from pathlib import Path
  7 | from typing import Any
  8 | 
  9 | import yaml  # type: ignore[import-untyped]
 10 | from pydantic import ValidationError
 11 | 
 12 | from ..core.exceptions import ValidationError as MFValidationError
 13 | from ..models.schemas import (
 14 |     Baseline,
 15 |     ExecutionPlan,
 16 |     ParentMission,
 17 |     SubMission,
 18 |     Validation,
 19 | )
 20 | 
 21 | 
 22 | class SchemaValidator:
 23 |     """Validates mission schemas and files."""
 24 | 
 25 |     @staticmethod
 26 |     def validate_parent_mission_file(file_path: Path) -> ParentMission:
 27 |         """Validate parent mission YAML file.
 28 | 
 29 |         Args:
 30 |             file_path: Path to mission.yaml file.
 31 | 
 32 |         Returns:
 33 |             Validated ParentMission instance.
 34 | 
 35 |         Raises:
 36 |             MFValidationError: If validation fails.
 37 |         """
 38 |         try:
 39 |             with open(file_path) as f:
 40 |                 data = yaml.safe_load(f)
 41 | 
 42 |             if not data:
 43 |                 raise MFValidationError(
 44 |                     f"Empty or invalid YAML file: {file_path}",
 45 |                     "Ensure the file contains valid YAML content",
 46 |                 )
 47 | 
 48 |             return ParentMission(**data)
 49 | 
 50 |         except FileNotFoundError:
 51 |             raise MFValidationError(
 52 |                 f"Mission file not found: {file_path}",
 53 |                 "Create the mission file using 'missionforge workspace init'",
 54 |             )
 55 |         except yaml.YAMLError as e:
 56 |             raise MFValidationError(
 57 |                 f"Invalid YAML syntax in {file_path}: {e}",
 58 |                 "Check YAML syntax - ensure proper indentation and structure",
 59 |             )
 60 |         except ValidationError as e:
 61 |             errors = SchemaValidator._format_pydantic_errors(e)
 62 |             raise MFValidationError(
 63 |                 f"Mission validation failed for {file_path}:\n{errors}",
 64 |                 "Fix the validation errors listed above",
 65 |             )
 66 |         except Exception as e:
 67 |             raise MFValidationError(
 68 |                 f"Unexpected error validating {file_path}: {e}",
 69 |                 "Check file format and content",
 70 |             )
 71 | 
 72 |     @staticmethod
 73 |     def validate_sub_mission_file(file_path: Path) -> SubMission:
 74 |         """Validate sub-mission YAML file.
 75 | 
 76 |         Args:
 77 |             file_path: Path to sub-mission YAML file.
 78 | 
 79 |         Returns:
 80 |             Validated SubMission instance.
 81 | 
 82 |         Raises:
 83 |             MFValidationError: If validation fails.
 84 |         """
 85 |         try:
 86 |             with open(file_path) as f:
 87 |                 data = yaml.safe_load(f)
 88 | 
 89 |             if not data:
 90 |                 raise MFValidationError(
 91 |                     f"Empty or invalid YAML file: {file_path}",
 92 |                     "Ensure the file contains valid YAML content",
 93 |                 )
 94 | 
 95 |             return SubMission(**data)
 96 | 
 97 |         except FileNotFoundError:
 98 |             raise MFValidationError(
 99 |                 f"Sub-mission file not found: {file_path}",
100 |                 "Create the sub-mission file first",
101 |             )
102 |         except yaml.YAMLError as e:
103 |             raise MFValidationError(
104 |                 f"Invalid YAML syntax in {file_path}: {e}",
105 |                 "Check YAML syntax - ensure proper indentation and structure",
106 |             )
107 |         except ValidationError as e:
108 |             errors = SchemaValidator._format_pydantic_errors(e)
109 |             raise MFValidationError(
110 |                 f"Sub-mission validation failed for {file_path}:\n{errors}",
111 |                 "Fix the validation errors listed above",
112 |             )
113 |         except Exception as e:
114 |             raise MFValidationError(
115 |                 f"Unexpected error validating {file_path}: {e}",
116 |                 "Check file format and content",
117 |             )
118 | 
119 |     @staticmethod
120 |     def validate_baseline_file(file_path: Path) -> Baseline:
121 |         """Validate baseline JSON file.
122 | 
123 |         Args:
124 |             file_path: Path to baseline.json or baseline.todo.json file.
125 | 
126 |         Returns:
127 |             Validated Baseline instance.
128 | 
129 |         Raises:
130 |             MFValidationError: If validation fails.
131 |         """
132 |         try:
133 |             with open(file_path) as f:
134 |                 data = json.load(f)
135 | 
136 |             return Baseline(**data)
137 | 
138 |         except FileNotFoundError:
139 |             raise MFValidationError(
140 |                 f"Baseline file not found: {file_path}",
141 |                 "Capture baseline using 'missionforge baseline capture'",
142 |             )
143 |         except json.JSONDecodeError as e:
144 |             raise MFValidationError(
145 |                 f"Invalid JSON syntax in {file_path}: {e}",
146 |                 "Check JSON syntax - ensure proper formatting",
147 |             )
148 |         except ValidationError as e:
149 |             errors = SchemaValidator._format_pydantic_errors(e)
150 |             raise MFValidationError(
151 |                 f"Baseline validation failed for {file_path}:\n{errors}",
152 |                 "Fix the validation errors listed above",
153 |             )
154 |         except Exception as e:
155 |             raise MFValidationError(
156 |                 f"Unexpected error validating {file_path}: {e}",
157 |                 "Check file format and content",
158 |             )
159 | 
160 |     @staticmethod
161 |     def validate_validation_file(file_path: Path) -> Validation:
162 |         """Validate validation JSON file.
163 | 
164 |         Args:
165 |             file_path: Path to validation.json or validation.todo.json file.
166 | 
167 |         Returns:
168 |             Validated Validation instance.
169 | 
170 |         Raises:
171 |             MFValidationError: If validation fails.
172 |         """
173 |         try:
174 |             with open(file_path) as f:
175 |                 data = json.load(f)
176 | 
177 |             return Validation(**data)
178 | 
179 |         except FileNotFoundError:
180 |             raise MFValidationError(
181 |                 f"Validation file not found: {file_path}",
182 |                 "Run validation using 'missionforge validate'",
183 |             )
184 |         except json.JSONDecodeError as e:
185 |             raise MFValidationError(
186 |                 f"Invalid JSON syntax in {file_path}: {e}",
187 |                 "Check JSON syntax - ensure proper formatting",
188 |             )
189 |         except ValidationError as e:
190 |             errors = SchemaValidator._format_pydantic_errors(e)
191 |             raise MFValidationError(
192 |                 f"Validation file validation failed for {file_path}:\n{errors}",
193 |                 "Fix the validation errors listed above",
194 |             )
195 |         except Exception as e:
196 |             raise MFValidationError(
197 |                 f"Unexpected error validating {file_path}: {e}",
198 |                 "Check file format and content",
199 |             )
200 | 
201 |     @staticmethod
202 |     def validate_plan_file(file_path: Path) -> ExecutionPlan:
203 |         """Validate execution plan YAML file.
204 | 
205 |         Args:
206 |             file_path: Path to plan.yaml file.
207 | 
208 |         Returns:
209 |             Validated ExecutionPlan instance.
210 | 
211 |         Raises:
212 |             MFValidationError: If validation fails.
213 |         """
214 |         try:
215 |             with open(file_path) as f:
216 |                 data = yaml.safe_load(f)
217 | 
218 |             if not data:
219 |                 raise MFValidationError(
220 |                     f"Empty or invalid YAML file: {file_path}",
221 |                     "Ensure the file contains valid YAML content",
222 |                 )
223 | 
224 |             return ExecutionPlan(**data)
225 | 
226 |         except FileNotFoundError:
227 |             raise MFValidationError(
228 |                 f"Plan file not found: {file_path}",
229 |                 "Generate plan using 'missionforge plan generate'",
230 |             )
231 |         except yaml.YAMLError as e:
232 |             raise MFValidationError(
233 |                 f"Invalid YAML syntax in {file_path}: {e}",
234 |                 "Check YAML syntax - ensure proper indentation and structure",
235 |             )
236 |         except ValidationError as e:
237 |             errors = SchemaValidator._format_pydantic_errors(e)
238 |             raise MFValidationError(
239 |                 f"Plan validation failed for {file_path}:\n{errors}",
240 |                 "Fix the validation errors listed above",
241 |             )
242 |         except Exception as e:
243 |             raise MFValidationError(
244 |                 f"Unexpected error validating {file_path}: {e}",
245 |                 "Check file format and content",
246 |             )
247 | 
248 |     @staticmethod
249 |     def validate_sub_mission_dependencies(
250 |         sub_mission: SubMission, available_missions: list[str]
251 |     ) -> None:
252 |         """Validate that sub-mission dependencies exist.
253 | 
254 |         Args:
255 |             sub_mission: SubMission to validate.
256 |             available_missions: List of available sub-mission IDs.
257 | 
258 |         Raises:
259 |             MFValidationError: If dependencies are invalid.
260 |         """
261 |         missing_deps = []
262 |         for dep in sub_mission.depends_on:
263 |             if dep not in available_missions:
264 |                 missing_deps.append(dep)
265 | 
266 |         if missing_deps:
267 |             raise MFValidationError(
268 |                 f"Sub-mission '{sub_mission.id}' has missing dependencies: {', '.join(missing_deps)}",
269 |                 f"Ensure these sub-missions exist: {', '.join(missing_deps)}",
270 |             )
271 | 
272 |     @staticmethod
273 |     def validate_forbidden_paths(
274 |         parent_mission: ParentMission, sub_mission: SubMission
275 |     ) -> None:
276 |         """Validate that sub-mission paths don't conflict with forbidden paths.
277 | 
278 |         Args:
279 |             parent_mission: Parent mission with forbidden paths.
280 |             sub_mission: Sub-mission to validate.
281 | 
282 |         Raises:
283 |             MFValidationError: If paths conflict.
284 |         """
285 |         import pathspec
286 | 
287 |         if not parent_mission.forbidden_paths:
288 |             return
289 | 
290 |         forbidden_spec = pathspec.PathSpec.from_lines(
291 |             "gitwildmatch", parent_mission.forbidden_paths
292 |         )
293 | 
294 |         conflicts = []
295 |         for allowed_path in sub_mission.allowed_paths:
296 |             # Check if allowed path matches any forbidden pattern
297 |             if forbidden_spec.match_file(allowed_path):
298 |                 conflicts.append(allowed_path)
299 | 
300 |         if conflicts:
301 |             raise MFValidationError(
302 |                 f"Sub-mission '{sub_mission.id}' has paths that conflict with "
303 |                 f"forbidden paths: {', '.join(conflicts)}",
304 |                 "Remove these paths from allowed_paths or adjust forbidden_paths in parent mission",
305 |             )
306 | 
307 |     @staticmethod
308 |     def _format_pydantic_errors(error: ValidationError) -> str:
309 |         """Format Pydantic validation errors into readable message.
310 | 
311 |         Args:
312 |             error: Pydantic ValidationError.
313 | 
314 |         Returns:
315 |             Formatted error message.
316 |         """
317 |         errors = []
318 |         for err in error.errors():
319 |             loc = " -> ".join(str(x) for x in err["loc"])
320 |             msg = err["msg"]
321 |             errors.append(f"  • {loc}: {msg}")
322 | 
323 |         return "\n".join(errors)
324 | 
325 |     @staticmethod
326 |     def validate_mission_structure(mission_path: Path) -> dict[str, Any]:
327 |         """Validate complete mission directory structure.
328 | 
329 |         Args:
330 |             mission_path: Path to mission directory.
331 | 
332 |         Returns:
333 |             Dictionary with validation results.
334 | 
335 |         Raises:
336 |             MFValidationError: If critical validation fails.
337 |         """
338 |         results: dict[str, Any] = {
339 |             "mission_file": False,
340 |             "plan_file": False,
341 |             "sub_missions": [],
342 |             "errors": [],
343 |             "warnings": [],
344 |         }
345 | 
346 |         # Check mission.yaml
347 |         mission_file = mission_path / "mission.yaml"
348 |         if not mission_file.exists():
349 |             results["errors"].append(f"Missing mission.yaml in {mission_path}")
350 |             raise MFValidationError(
351 |                 f"Mission file not found: {mission_file}",
352 |                 "Create mission.yaml file",
353 |             )
354 | 
355 |         try:
356 |             parent_mission = SchemaValidator.validate_parent_mission_file(mission_file)
357 |             results["mission_file"] = True
358 |         except MFValidationError as e:
359 |             results["errors"].append(str(e))
360 |             raise
361 | 
362 |         # Check plan.yaml
363 |         plan_file = mission_path / "plan.yaml"
364 |         if plan_file.exists():
365 |             try:
366 |                 SchemaValidator.validate_plan_file(plan_file)
367 |                 results["plan_file"] = True
368 |             except MFValidationError as e:
369 |                 results["warnings"].append(f"Plan file validation failed: {e}")
370 |         else:
371 |             results["warnings"].append("No plan.yaml found")
372 | 
373 |         # Check sub-missions
374 |         sub_missions_dir = mission_path / "sub-missions"
375 |         if sub_missions_dir.exists():
376 |             available_missions = []
377 |             for sub_file in sub_missions_dir.glob("*.yaml"):
378 |                 try:
379 |                     sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
380 |                     available_missions.append(sub_mission.id)
381 |                     results["sub_missions"].append(sub_mission.id)
382 | 
383 |                     # Validate parent relationship
384 |                     if sub_mission.parent != parent_mission.id:
385 |                         results["errors"].append(
386 |                             f"Sub-mission {sub_mission.id} parent mismatch: "
387 |                             f"expected {parent_mission.id}, got {sub_mission.parent}"
388 |                         )
389 | 
390 |                     # Validate forbidden paths
391 |                     try:
392 |                         SchemaValidator.validate_forbidden_paths(parent_mission, sub_mission)
393 |                     except MFValidationError as e:
394 |                         results["errors"].append(str(e))
395 | 
396 |                 except MFValidationError as e:
397 |                     results["errors"].append(f"Sub-mission {sub_file.name}: {e}")
398 | 
399 |             # Validate dependencies
400 |             for sub_file in sub_missions_dir.glob("*.yaml"):
401 |                 try:
402 |                     sub_mission = SchemaValidator.validate_sub_mission_file(sub_file)
403 |                     SchemaValidator.validate_sub_mission_dependencies(
404 |                         sub_mission, available_missions
405 |                     )
406 |                 except MFValidationError as e:
407 |                     results["errors"].append(str(e))
408 | 
409 |         return results
410 | 
411 | 
412 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
src/missionforge/core/workspace.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:42:04.381Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.01

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I'll create the BaselineService class. Let me first check if there's a sub-mission.yaml file to understand the structure better.

<read_file>
<args>
<file>
<path>issues/baseline-flow.md</path>
<line_range>1-100</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'issues/baseline-flow.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>issues/baseline-flow.md</path>
<content lines="1-100">
 1 | # MF-008: Baseline Capture and Commit Flow
 2 | 
 3 | ## Priority
 4 | **MUST FINISH** - Required for project viability
 5 | 
 6 | ## Phase
 7 | Phase 1 - Core CLI Harness
 8 | 
 9 | ## Dependencies
10 | - MF-001 (CLI Foundation)
11 | - MF-002 (Schemas) - needs baseline + sub-mission schemas
12 | 
13 | NOT a hard dependency: decompose-command. Baseline operates on any `sub-mission.yaml` that conforms to the schema — for development and tests, hand-authored sub-mission YAML fixtures are sufficient. Decompose is just one producer of those files.
14 | 
15 | ## Parallel Work
16 | Runs in parallel with workspace-commands, decompose-command, plan-command, and next-command once schemas land. Only sub-mission-validation downstream of this is blocked on a real baseline.json.
17 | 
18 | ## Objective
19 | Implement baseline measurement workflow for sub-missions: capture baseline.todo.json and commit to immutable baseline.json.
20 | 
21 | ## Tasks
22 | - [ ] Implement `missionforge baseline <sub-mission-id> --capture` command
23 | - [ ] Read sub-mission metrics from sub-mission.yaml
24 | - [ ] Generate baseline.todo.json with:
25 |   - metric_id
26 |   - description
27 |   - baseline_target
28 |   - value (empty for Bob to fill)
29 | - [ ] Prevent capture if baseline.json already exists (unless --force)
30 | - [ ] Implement `missionforge baseline <sub-mission-id> --commit` command
31 | - [ ] Validate all baseline fields are filled
32 | - [ ] Validate field types match metric definitions
33 | - [ ] Check values are reasonable (not obviously wrong)
34 | - [ ] Write immutable baseline.json with timestamp
35 | - [ ] Prevent modification after commit
36 | - [ ] Add --reset flag to allow re-capture if needed
37 | - [ ] Display baseline summary in terminal
38 | - [ ] Add unit and integration tests
39 | 
40 | ## Acceptance Criteria
41 | - [ ] `--capture` generates correct baseline.todo.json structure
42 | - [ ] baseline.todo.json is easy for Bob to fill
43 | - [ ] Cannot capture if baseline already committed (without --force)
44 | - [ ] `--commit` validates all fields are filled
45 | - [ ] Type validation catches incorrect value types
46 | - [ ] baseline.json is immutable after commit
47 | - [ ] Timestamp is recorded in baseline.json
48 | - [ ] Terminal output shows clear summary
49 | - [ ] Integration tests cover capture → fill → commit flow
50 | 
51 | ## Example baseline.todo.json
52 | ```json
53 | {
54 |   "sub_mission_id": "MF-001-A",
55 |   "metrics": [
56 |     {
57 |       "metric_id": "rest_endpoint_exists",
58 |       "description": "A REST endpoint exists at /api/matchmaking",
59 |       "baseline_target": false,
60 |       "value": null
61 |     }
62 |   ]
63 | }
64 | ```
65 | 
66 | ## Example baseline.json
67 | ```json
68 | {
69 |   "sub_mission_id": "MF-001-A",
70 |   "timestamp": "2026-05-16T16:30:00Z",
71 |   "status": "committed",
72 |   "metrics": [
73 |     {
74 |       "metric_id": "rest_endpoint_exists",
75 |       "description": "A REST endpoint exists at /api/matchmaking",
76 |       "baseline_target": false,
77 |       "value": false
78 |     }
79 |   ]
80 | }
81 | ```
82 | 
83 | ## Technical Notes
84 | - baseline.json should be immutable (add file permissions check)
85 | - Validate metric values match expected types (bool, int, string)
86 | - Add metadata: timestamp, status, sub_mission_id
87 | - Clear error messages for validation failures
88 | 
89 | ## Estimated Effort
90 | **3-4 hours** (hackathon pace)
91 | 
92 | ## Developer Assignment
93 | Backend/CLI Developer (can work in parallel with MF-006/MF-007)
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
src/missionforge/core/workspace.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:42:08.170Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I'll create the BaselineService class with all three methods. Let me write the complete implementation:

<write_to_file>
<path>src/missionforge/core/baseline_service.py</path>
<content>"""Baseline capture and commit service."""

import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..models.schemas import SubMissionBaseline, SubMissionBaselineMetric
from ..schemas.validators import SchemaValidator
from .exceptions import (
    BaselineAlreadyExistsError,
    BaselineIncompleteError,
    BaselineNotCapturedError,
    BaselineValidationError,
)
from .workspace import Workspace


class BaselineService:
    """Service for baseline capture and commit operations."""

    def __init__(self, workspace: Workspace | None = None):
        """Initialize service with workspace.

        Args:
            workspace: Workspace instance. Defaults to current workspace.
        """
        self.workspace = workspace or Workspace()

    def capture_baseline(self, sub_mission_id: str, force: bool = False) -> Path:
        """Capture baseline metrics from sub-mission definition.

        Reads sub-mission.yaml, extracts metric definitions, and creates
        baseline.todo.json with empty values for Bob to fill.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
            force: If True, overwrite existing baseline.json.

        Returns:
            Path to created baseline.todo.json file.

        Raises:
            BaselineAlreadyExistsError: If baseline.json exists and force=False.
            ValidationError: If sub-mission.yaml is invalid.
        """
        # Check if baseline already exists
        baseline_path = self.workspace.baseline_path(sub_mission_id)
        if baseline_path.exists() and not force:
            raise BaselineAlreadyExistsError(sub_mission_id, str(baseline_path))

        # Get sub-mission file path
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        sub_mission_dir = self.workspace.sub_mission_path(parent_id, sub_mission_id)
        sub_mission_file = sub_mission_dir / "sub-mission.yaml"

        # Read and validate sub-mission
        sub_mission = SchemaValidator.validate_sub_mission_file(sub_mission_file)

        # Create baseline metrics from sub-mission metrics
        baseline_metrics: list[SubMissionBaselineMetric] = []
        for metric_id, metric_def in sub_mission.metrics.items():
            # Use target as baseline_target
            if metric_def.target is None:
                raise BaselineValidationError(
                    f"Metric '{metric_id}' in {sub_mission_id} has no target value",
                    "All metrics must have a target value for baseline capture",
                )

            baseline_metric = SubMissionBaselineMetric(
                metric_id=metric_id,
                description=f"Baseline measurement for {metric_id}",
                baseline_target=metric_def.target,
                value=None,  # Bob will fill this
            )
            baseline_metrics.append(baseline_metric)

        # Create baseline with captured status
        baseline = SubMissionBaseline(
            sub_mission_id=sub_mission_id,
            timestamp=None,  # Will be set on commit
            status="captured",
            metrics=baseline_metrics,
        )

        # Write to baseline.todo.json
        todo_path = self.workspace.baseline_todo_path(sub_mission_id)
        todo_path.parent.mkdir(parents=True, exist_ok=True)

        with open(todo_path, "w") as f:
            json.dump(baseline.model_dump(mode="json"), f, indent=2)

        return todo_path

    def commit_baseline(self, sub_mission_id: str) -> Path:
        """Commit baseline from baseline.todo.json to immutable baseline.json.

        Validates all metric values are filled and types match, then writes
        to baseline.json with timestamp and makes file read-only.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to created baseline.json file.

        Raises:
            BaselineNotCapturedError: If baseline.todo.json doesn't exist.
            BaselineIncompleteError: If any metric values are None.
            BaselineValidationError: If value types don't match baseline_target types.
        """
        # Check if baseline.todo.json exists
        todo_path = self.workspace.baseline_todo_path(sub_mission_id)
        if not todo_path.exists():
            raise BaselineNotCapturedError(sub_mission_id)

        # Read baseline.todo.json
        with open(todo_path) as f:
            data = json.load(f)

        # Parse into SubMissionBaseline model
        baseline = SubMissionBaseline(**data)

        # Validate all values are filled
        unfilled_metrics: list[str] = []
        for metric in baseline.metrics:
            if metric.value is None:
                unfilled_metrics.append(metric.metric_id)

        if unfilled_metrics:
            raise BaselineIncompleteError(sub_mission_id, unfilled_metrics)

        # Validate value types match baseline_target types
        for metric in baseline.metrics:
            if metric.value is not None:
                target_type = type(metric.baseline_target)
                value_type = type(metric.value)
                if target_type != value_type:
                    raise BaselineValidationError(
                        f"Type mismatch for metric '{metric.metric_id}' in {sub_mission_id}: "
                        f"expected {target_type.__name__}, got {value_type.__name__}",
                        f"Ensure value type matches baseline_target type for {metric.metric_id}",
                    )

        # Add timestamp and update status
        baseline.timestamp = datetime.now(timezone.utc).isoformat()
        baseline.status = "committed"

        # Write to baseline.json
        baseline_path = self.workspace.baseline_path(sub_mission_id)
        baseline_path.parent.mkdir(parents=True, exist_ok=True)

        with open(baseline_path, "w") as f:
            json.dump(baseline.model_dump(mode="json"), f, indent=2)

        # Make file read-only
        os.chmod(baseline_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

        return baseline_path

    def reset_baseline(self, sub_mission_id: str, force: bool = False) -> None:
        """Reset baseline by removing baseline files.

        Removes baseline.todo.json and baseline.json (if force=True).

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').
            force: If True, remove read-only baseline.json.

        Raises:
            BaselineValidationError: If no baseline files exist or force required.
        """
        todo_path = self.workspace.baseline_todo_path(sub_mission_id)
        baseline_path = self.workspace.baseline_path(sub_mission_id)

        files_removed = []

        # Remove baseline.todo.json if exists
        if todo_path.exists():
            todo_path.unlink()
            files_removed.append("baseline.todo.json")

        # Remove baseline.json if exists (requires force)
        if baseline_path.exists():
            if not force:
                raise BaselineValidationError(
                    f"Cannot remove committed baseline.json for {sub_mission_id} without --force",
                    "Use --force flag to remove committed baseline",
                )
            # Remove read-only protection before deleting
            os.chmod(baseline_path, stat.S_IRUSR | stat.S_IWUSR)
            baseline_path.unlink()
            files_removed.append("baseline.json")

        # Raise error if no files existed
        if not files_removed:
            raise BaselineValidationError(
                f"No baseline files found for {sub_mission_id}",
                "Baseline has not been captured yet",
            )


# Made with Bob
</content>
<line_count>203</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'src/missionforge/core/baseline_service.py'] Result:
<file_write_result>
<path>src/missionforge/core/baseline_service.py</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
src/missionforge/core/baseline_service.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:42:35.933Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.12

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Successfully implemented Phase 2 of MF-008: Core Service Layer

**Created:** `src/missionforge/core/baseline_service.py` (203 lines)

**Implementation Summary:**

1. **BaselineService Class**
   - Initialized with optional Workspace parameter
   - Three main methods for baseline workflow

2. **capture_baseline(sub_mission_id, force=False) -> Path**
   - Reads sub-mission.yaml using SchemaValidator
   - Extracts metrics dictionary from SubMission model
   - Creates SubMissionBaselineMetric for each metric with:
     - metric_id from dict key
     - description (auto-generated)
     - baseline_target from metric_def.target
     - value set to None for Bob to fill
   - Creates SubMissionBaseline with status="captured"
   - Writes to baseline.todo.json
   - Raises BaselineAlreadyExistsError if baseline.json exists (unless force=True)
   - Returns path to baseline.todo.json

3. **commit_baseline(sub_mission_id) -> Path**
   - Reads and parses baseline.todo.json
   - Validates all metric values are filled (not None)
   - Validates value types match baseline_target types using type() comparison
   - Adds ISO 8601 UTC timestamp
   - Updates status to "committed"
   - Writes to baseline.json
   - Makes file read-only using os.chmod with stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
   - Comprehensive error handling for all edge cases
   - Returns path to baseline.json

4. **reset_baseline(sub_mission_id, force=False) -> None**
   - Removes baseline.todo.json if exists
   - Removes baseline.json if exists (requires force=True)
   - Removes read-only protection before deletion
   - Raises error if no baseline files exist
   - Raises error if trying to remove committed baseline without force

**Key Features:**
- Complete error handling with all required exception types
- Type validation using exact type matching
- ISO 8601 UTC timestamp format
- File permission management for immutability
- Comprehensive docstrings for all methods
- Follows existing code style from other core modules
- Uses Workspace methods for path resolution
- Validates metric definitions have target values
</result>
</attempt_completion>

