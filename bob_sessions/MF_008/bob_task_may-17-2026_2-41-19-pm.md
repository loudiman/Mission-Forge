**User:**

<task>
Implement Phase 4 of MF-008: Supporting Infrastructure

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. Phase 1 (data models) is complete. Now we need to add supporting infrastructure before building the service layer.

**Your Task:**
Implement Phase 4 from the implementation plan at `issues/MF-008-implementation-plan.md`:

1. **Add baseline-specific exceptions to `src/missionforge/core/exceptions.py`:**
   - `BaselineAlreadyExistsError`: Raised when baseline already committed
   - `BaselineNotCapturedError`: Raised when trying to commit without capture
   - `BaselineValidationError`: Raised when baseline validation fails
   - `BaselineIncompleteError`: Raised when baseline has unfilled values

2. **Add baseline path helpers to `src/missionforge/core/workspace.py`:**
   - `baseline_todo_path(self, sub_mission_id: str) -> Path`: Returns path to baseline.todo.json
   - `baseline_path(self, sub_mission_id: str) -> Path`: Returns path to baseline.json

**Requirements for Exceptions:**
- Follow existing exception pattern (inherit from MissionForgeError)
- Include helpful error messages and suggestions
- Use the format: `super().__init__(message, suggestion)`

**Requirements for Workspace Methods:**
- Extract parent_id from sub_mission_id (e.g., "MF-001-A" → "MF-001")
- Use existing `sub_mission_path()` method as base
- Return Path objects for the JSON files

**Example Usage:**
```python
# Exceptions
raise BaselineAlreadyExistsError(sub_mission_id, baseline_path)

# Workspace paths
workspace = Workspace()
todo_path = workspace.baseline_todo_path("MF-001-A")
# Returns: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json
```

**Scope:**
- ONLY modify `src/missionforge/core/exceptions.py` and `src/missionforge/core/workspace.py`
- Add exceptions before the "# Made with Bob" comment
- Add workspace methods after existing methods, before "# Made with Bob"
- Follow existing code style and patterns

When complete, use `attempt_completion` with a summary of what was added.
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:40:45.583Z
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

I'll implement Phase 4 of MF-008 by adding baseline-specific exceptions and workspace path helpers. Let me start by reading the relevant files to understand the existing patterns.

<read_file>
<args>
<file>
<path>src/missionforge/core/exceptions.py</path>
</file>
<file>
<path>src/missionforge/core/workspace.py</path>
</file>
<file>
<path>issues/MF-008-implementation-plan.md</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'src/missionforge/core/exceptions.py', 'src/missionforge/core/workspace.py', 'issues/MF-008-implementation-plan.md'] Result:
<files>
<file><path>src/missionforge/core/exceptions.py</path>
<content lines="1-70">
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
70 | # Made with Bob
</content>
</file>
<file><path>src/missionforge/core/workspace.py</path>
<content lines="1-100">
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
 99 | 
100 | # Made with Bob
</content>
</file>
<file><path>issues/MF-008-implementation-plan.md</path>
<content lines="1-431">
  1 | # MF-008: Baseline Capture and Commit Flow - Implementation Plan
  2 | 
  3 | ## Executive Summary
  4 | 
  5 | This document provides a detailed implementation plan for MF-008, which implements the baseline measurement workflow for sub-missions. After analyzing the codebase and issue specifications, I've identified that this feature requires **new data models** separate from the existing git-based baseline schemas.
  6 | 
  7 | ## Architecture Analysis
  8 | 
  9 | ### Two Baseline Concepts
 10 | 
 11 | The codebase currently has two distinct baseline concepts:
 12 | 
 13 | 1. **Git-based Baseline** (existing in `models/schemas.py`):
 14 |    - Tracks: `files_changed`, `lines_added`, `lines_removed`, `test_coverage`
 15 |    - Purpose: General code change metrics
 16 |    - Used for: Overall mission tracking
 17 | 
 18 | 2. **Sub-Mission Metric Baseline** (required by issue #8):
 19 |    - Tracks: Custom semantic metrics from `sub-mission.yaml`
 20 |    - Purpose: Bob-filled validation of specific goals
 21 |    - Used for: Sub-mission pass/fail determination
 22 |    - Example: "REST endpoint exists" (bool), "CORBA references" (int)
 23 | 
 24 | ### Key Insight
 25 | 
 26 | The issue specification is correct - we need **new models** for sub-mission metric baselines. These are fundamentally different from git metrics:
 27 | 
 28 | - **Git metrics**: Deterministic, CLI-captured (files changed, lines added)
 29 | - **Metric baselines**: Semantic, Bob-filled (endpoint exists, feature works)
 30 | 
 31 | ## Data Structure Design
 32 | 
 33 | ### baseline.todo.json (Bob fills this)
 34 | 
 35 | ```json
 36 | {
 37 |   "sub_mission_id": "MF-001-A",
 38 |   "metrics": [
 39 |     {
 40 |       "metric_id": "rest_endpoint_exists",
 41 |       "description": "A REST endpoint exists at /api/matchmaking",
 42 |       "baseline_target": false,
 43 |       "value": null
 44 |     },
 45 |     {
 46 |       "metric_id": "corba_references_count",
 47 |       "description": "Number of CORBA references in matchmaking code",
 48 |       "baseline_target": 7,
 49 |       "value": null
 50 |     }
 51 |   ]
 52 | }
 53 | ```
 54 | 
 55 | ### baseline.json (Immutable after commit)
 56 | 
 57 | ```json
 58 | {
 59 |   "sub_mission_id": "MF-001-A",
 60 |   "timestamp": "2026-05-16T16:30:00Z",
 61 |   "status": "committed",
 62 |   "metrics": [
 63 |     {
 64 |       "metric_id": "rest_endpoint_exists",
 65 |       "description": "A REST endpoint exists at /api/matchmaking",
 66 |       "baseline_target": false,
 67 |       "value": false
 68 |     },
 69 |     {
 70 |       "metric_id": "corba_references_count",
 71 |       "description": "Number of CORBA references in matchmaking code",
 72 |       "baseline_target": 7,
 73 |       "value": 7
 74 |     }
 75 |   ]
 76 | }
 77 | ```
 78 | 
 79 | ## Implementation Plan
 80 | 
 81 | ### Phase 1: Data Models (1 hour)
 82 | 
 83 | #### 1.1 Create New Pydantic Models in `models/schemas.py`
 84 | 
 85 | ```python
 86 | class SubMissionBaselineMetric(BaseModel):
 87 |     """A single metric in a sub-mission baseline."""
 88 |     metric_id: str
 89 |     description: str
 90 |     baseline_target: bool | int | float | str
 91 |     value: bool | int | float | str | None = None
 92 | 
 93 | class SubMissionBaseline(BaseModel):
 94 |     """Baseline for sub-mission custom metrics."""
 95 |     sub_mission_id: str
 96 |     timestamp: str | None = None
 97 |     status: str | None = None  # "captured", "committed"
 98 |     metrics: list[SubMissionBaselineMetric]
 99 | ```
100 | 
101 | #### 1.2 Update JSON Schemas in `schemas/json_schemas.py`
102 | 
103 | Add new schemas:
104 | - `SUB_MISSION_BASELINE_TODO_SCHEMA`
105 | - `SUB_MISSION_BASELINE_SCHEMA`
106 | 
107 | ### Phase 2: Core Service Layer (1.5 hours)
108 | 
109 | #### 2.1 Create `core/baseline_service.py`
110 | 
111 | ```python
112 | class BaselineService:
113 |     """Service for baseline capture and commit operations."""
114 |     
115 |     def capture_baseline(
116 |         self, 
117 |         sub_mission_id: str,
118 |         force: bool = False
119 |     ) -> Path:
120 |         """Generate baseline.todo.json from sub-mission.yaml metrics."""
121 |         
122 |     def commit_baseline(
123 |         self, 
124 |         sub_mission_id: str
125 |     ) -> Path:
126 |         """Validate and commit baseline.json from baseline.todo.json."""
127 |         
128 |     def reset_baseline(
129 |         self, 
130 |         sub_mission_id: str
131 |     ) -> None:
132 |         """Remove baseline files to allow re-capture."""
133 | ```
134 | 
135 | **Key Operations:**
136 | 
137 | 1. **Capture**:
138 |    - Read `sub-mission.yaml`
139 |    - Extract `metrics` dictionary
140 |    - For each metric, create entry with `baseline_target` from metric definition
141 |    - Set `value: null` for Bob to fill
142 |    - Write `baseline.todo.json`
143 |    - Prevent if `baseline.json` exists (unless `--force`)
144 | 
145 | 2. **Commit**:
146 |    - Read `baseline.todo.json`
147 |    - Validate all `value` fields are filled (not null)
148 |    - Validate types match `baseline_target` types
149 |    - Add `timestamp` and `status: "committed"`
150 |    - Write `baseline.json`
151 |    - Make file read-only (chmod 444)
152 | 
153 | 3. **Reset**:
154 |    - Remove both `baseline.todo.json` and `baseline.json`
155 |    - Require confirmation or `--force` flag
156 | 
157 | ### Phase 3: CLI Commands (1 hour)
158 | 
159 | #### 3.1 Create `cli/commands/baseline.py`
160 | 
161 | ```python
162 | @app.command("capture")
163 | def capture_baseline(
164 |     sub_mission_id: str,
165 |     force: bool = False
166 | ) -> None:
167 |     """Capture baseline metrics for a sub-mission."""
168 | 
169 | @app.command("commit")
170 | def commit_baseline(
171 |     sub_mission_id: str
172 | ) -> None:
173 |     """Commit baseline after Bob fills values."""
174 | 
175 | @app.command("reset")
176 | def reset_baseline(
177 |     sub_mission_id: str,
178 |     force: bool = False
179 | ) -> None:
180 |     """Reset baseline to allow re-capture."""
181 | ```
182 | 
183 | #### 3.2 Register in `cli/app.py`
184 | 
185 | ```python
186 | from .commands import baseline
187 | app.add_typer(baseline.app, name="baseline")
188 | ```
189 | 
190 | ### Phase 4: Supporting Infrastructure (30 minutes)
191 | 
192 | #### 4.1 Add Exceptions to `core/exceptions.py`
193 | 
194 | ```python
195 | class BaselineAlreadyExistsError(MissionForgeError):
196 |     """Raised when baseline already committed."""
197 | 
198 | class BaselineNotCapturedError(MissionForgeError):
199 |     """Raised when trying to commit without capture."""
200 | 
201 | class BaselineValidationError(MissionForgeError):
202 |     """Raised when baseline validation fails."""
203 | 
204 | class BaselineIncompleteError(MissionForgeError):
205 |     """Raised when baseline has unfilled values."""
206 | ```
207 | 
208 | #### 4.2 Update `core/workspace.py`
209 | 
210 | ```python
211 | def baseline_todo_path(self, sub_mission_id: str) -> Path:
212 |     """Get path to baseline.todo.json."""
213 |     return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.todo.json"
214 | 
215 | def baseline_path(self, sub_mission_id: str) -> Path:
216 |     """Get path to baseline.json."""
217 |     return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.json"
218 | ```
219 | 
220 | ### Phase 5: Testing (1 hour)
221 | 
222 | #### 5.1 Unit Tests
223 | 
224 | - `tests/unit/test_baseline_models.py`: Test Pydantic models
225 | - `tests/unit/test_baseline_service.py`: Test service operations
226 | - `tests/unit/commands/test_baseline.py`: Test CLI commands
227 | 
228 | #### 5.2 Integration Tests
229 | 
230 | - `tests/integration/test_baseline_flow.py`: Test full workflow
231 |   - Capture → Fill → Commit
232 |   - Error cases (already exists, incomplete, etc.)
233 |   - Reset functionality
234 | 
235 | #### 5.3 Test Fixtures
236 | 
237 | Create in `tests/fixtures/`:
238 | - `sub-mission-with-metrics.yaml`
239 | - `baseline.todo.json` (filled and unfilled versions)
240 | - `baseline.json` (committed version)
241 | 
242 | ## Type Inference Strategy
243 | 
244 | The baseline system needs to infer metric types from `baseline_target` values:
245 | 
246 | ```python
247 | def infer_metric_type(baseline_target: Any) -> type:
248 |     """Infer expected type from baseline_target value."""
249 |     if isinstance(baseline_target, bool):
250 |         return bool
251 |     elif isinstance(baseline_target, int):
252 |         return int
253 |     elif isinstance(baseline_target, float):
254 |         return float
255 |     else:
256 |         return str
257 | ```
258 | 
259 | When validating `value` during commit:
260 | 1. Get type from `baseline_target`
261 | 2. Ensure `value` matches that type
262 | 3. Reject if types don't match
263 | 
264 | ## File Immutability Implementation
265 | 
266 | ```python
267 | import os
268 | import stat
269 | 
270 | def make_readonly(file_path: Path) -> None:
271 |     """Make file read-only."""
272 |     os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
273 | 
274 | def is_readonly(file_path: Path) -> bool:
275 |     """Check if file is read-only."""
276 |     return not os.access(file_path, os.W_OK)
277 | ```
278 | 
279 | ## Error Handling Strategy
280 | 
281 | ### Capture Errors
282 | 
283 | 1. **Sub-mission not found**: Clear message with path
284 | 2. **No metrics defined**: Suggest adding metrics to sub-mission.yaml
285 | 3. **Baseline already exists**: Show path, suggest `--force` or `reset`
286 | 
287 | ### Commit Errors
288 | 
289 | 1. **baseline.todo.json not found**: Suggest running `capture` first
290 | 2. **Incomplete values**: List which metrics need values
291 | 3. **Type mismatch**: Show expected vs actual type
292 | 4. **baseline.json already exists**: Cannot overwrite committed baseline
293 | 
294 | ### Reset Errors
295 | 
296 | 1. **No baseline files**: Nothing to reset
297 | 2. **Confirmation required**: Require `--force` flag
298 | 
299 | ## Terminal Output Design
300 | 
301 | ### Capture Success
302 | 
303 | ```
304 | ✓ Baseline captured for MF-001-A
305 | 
306 | Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json
307 | 
308 | Metrics to fill (3):
309 |   • rest_endpoint_exists (bool)
310 |   • corba_references_count (int)
311 |   • matchmaking_latency_ms (float)
312 | 
313 | Next steps:
314 | 1. Analyze the code in allowed paths
315 | 2. Fill metric values in baseline.todo.json
316 | 3. Run: missionforge baseline commit MF-001-A
317 | ```
318 | 
319 | ### Commit Success
320 | 
321 | ```
322 | ✓ Baseline committed for MF-001-A
323 | 
324 | Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json
325 | 
326 | Baseline Summary:
327 | ┌─────────────────────────┬──────────┬───────┐
328 | │ Metric                  │ Target   │ Value │
329 | ├─────────────────────────┼──────────┼───────┤
330 | │ rest_endpoint_exists    │ false    │ false │
331 | │ corba_references_count  │ 7        │ 7     │
332 | │ matchmaking_latency_ms  │ 150.0    │ 145.2 │
333 | └─────────────────────────┴──────────┴───────┘
334 | 
335 | ⚠️  baseline.json is now immutable
336 | ```
337 | 
338 | ## Integration with Validation Flow
339 | 
340 | The baseline.json will be consumed by MF-009 (Sub-Mission Validation):
341 | 
342 | ```json
343 | // validation.todo.json uses baseline values
344 | {
345 |   "metrics": [
346 |     {
347 |       "metric_id": "rest_endpoint_exists",
348 |       "baseline_value": false,  // from baseline.json
349 |       "target_value": true,     // from sub-mission.yaml
350 |       "final_value": null       // Bob fills after implementation
351 |     }
352 |   ]
353 | }
354 | ```
355 | 
356 | ## Dependencies and Blockers
357 | 
358 | ### Dependencies (Must Complete First)
359 | - ✅ MF-001: CLI Foundation (complete)
360 | - ✅ MF-002: Schemas (complete - but needs extension)
361 | 
362 | ### Blocks (Waiting on This)
363 | - MF-009: Sub-Mission Validation (needs baseline.json)
364 | 
365 | ### Parallel Work (Can Work Simultaneously)
366 | - MF-006: Workspace Commands
367 | - MF-007: Decompose Command
368 | - MF-010: Plan Command
369 | - MF-011: Next Command
370 | 
371 | ## Time Estimates (Hackathon Pace)
372 | 
373 | | Phase | Task | Time |
374 | |-------|------|------|
375 | | 1 | Data Models | 1h |
376 | | 2 | Core Service | 1.5h |
377 | | 3 | CLI Commands | 1h |
378 | | 4 | Infrastructure | 0.5h |
379 | | 5 | Testing | 1h |
380 | | **Total** | | **5h** |
381 | 
382 | With buffer: **3-4 hours** as specified in issue
383 | 
384 | ## Success Criteria Checklist
385 | 
386 | - [ ] `missionforge baseline capture <id>` generates baseline.todo.json
387 | - [ ] baseline.todo.json structure matches specification
388 | - [ ] Bob can easily fill metric values
389 | - [ ] `missionforge baseline commit <id>` validates and commits
390 | - [ ] Type validation catches mismatches
391 | - [ ] baseline.json is immutable after commit
392 | - [ ] `--reset` flag allows re-capture
393 | - [ ] Clear terminal output at each step
394 | - [ ] Comprehensive test coverage
395 | - [ ] Integration with validation flow works
396 | 
397 | ## Risk Mitigation
398 | 
399 | ### Risk: Type inference ambiguity
400 | **Mitigation**: Use explicit type from baseline_target, document in sub-mission.yaml
401 | 
402 | ### Risk: File permission issues on Windows
403 | **Mitigation**: Graceful fallback, warn if cannot make read-only
404 | 
405 | ### Risk: Incomplete baseline.todo.json
406 | **Mitigation**: Clear validation errors listing missing fields
407 | 
408 | ### Risk: Confusion with git-based Baseline
409 | **Mitigation**: Clear naming (SubMissionBaseline), separate files, documentation
410 | 
411 | ## Next Steps
412 | 
413 | 1. Review this plan with team
414 | 2. Confirm data structure design
415 | 3. Begin Phase 1 implementation
416 | 4. Create test fixtures early
417 | 5. Iterate based on testing feedback
418 | 
419 | ## Questions for Review
420 | 
421 | 1. Should we support metric value ranges (min/max) in baseline?
422 | 2. Should baseline.json include git commit hash for traceability?
423 | 3. Should we validate metric_id matches sub-mission.yaml keys?
424 | 4. Should reset require explicit confirmation prompt?
425 | 
426 | ---
427 | 
428 | **Document Status**: Draft for Review  
429 | **Created**: 2026-05-17  
430 | **Author**: Bob (Planning Mode)  
431 | **Issue**: MF-008
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
issues/MF-008-implementation-plan.md

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:40:48.885Z
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

Now I'll implement Phase 4 by adding the baseline-specific exceptions and workspace path helpers. Let me start with the exceptions.

<apply_diff>
<path>src/missionforge/core/exceptions.py</path>
<diff>
<<<<<<< SEARCH
:start_line:64
-------
class PluginError(MissionForgeError):
    """Raised when plugin operation fails."""

    pass


# Made with Bob
=======
class PluginError(MissionForgeError):
    """Raised when plugin operation fails."""

    pass


class BaselineAlreadyExistsError(MissionForgeError):
    """Raised when baseline already committed."""

    def __init__(self, sub_mission_id: str, baseline_path: str):
        super().__init__(
            f"Baseline already exists for {sub_mission_id} at {baseline_path}",
            "Use 'missionforge baseline reset <id> --force' to remove and re-capture",
        )


class BaselineNotCapturedError(MissionForgeError):
    """Raised when trying to commit without capture."""

    def __init__(self, sub_mission_id: str):
        super().__init__(
            f"No baseline.todo.json found for {sub_mission_id}",
            "Run 'missionforge baseline capture <id>' first to generate baseline.todo.json",
        )


class BaselineValidationError(MissionForgeError):
    """Raised when baseline validation fails."""

    pass


class BaselineIncompleteError(MissionForgeError):
    """Raised when baseline has unfilled values."""

    def __init__(self, sub_mission_id: str, unfilled_metrics: list[str]):
        metrics_list = "\n  • ".join(unfilled_metrics)
        super().__init__(
            f"Baseline for {sub_mission_id} has unfilled metric values:\n  • {metrics_list}",
            "Fill all metric values in baseline.todo.json before committing",
        )


# Made with Bob
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'src/missionforge/core/exceptions.py'] Result:
<file_write_result>
<path>src/missionforge/core/exceptions.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
src/missionforge/core/exceptions.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
src/missionforge/core/exceptions.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:40:59.735Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.05

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

Now I'll add the baseline path helper methods to the Workspace class. I need to extract the parent ID from the sub-mission ID and use the existing `sub_mission_path()` method.

<apply_diff>
<path>src/missionforge/core/workspace.py</path>
<diff>
<<<<<<< SEARCH
:start_line:84
-------
    def list_missions(self) -> list[str]:
        """List all mission IDs in workspace.

        Returns:
            List of mission IDs.
        """
        if not self.missions_dir.exists():
            return []

        missions = []
        for mission_dir in self.missions_dir.iterdir():
            if mission_dir.is_dir() and (mission_dir / "mission.yaml").exists():
                missions.append(mission_dir.name)
        return sorted(missions)


# Made with Bob
=======
    def list_missions(self) -> list[str]:
        """List all mission IDs in workspace.

        Returns:
            List of mission IDs.
        """
        if not self.missions_dir.exists():
            return []

        missions = []
        for mission_dir in self.missions_dir.iterdir():
            if mission_dir.is_dir() and (mission_dir / "mission.yaml").exists():
                missions.append(mission_dir.name)
        return sorted(missions)

    def baseline_todo_path(self, sub_mission_id: str) -> Path:
        """Get path to baseline.todo.json for a sub-mission.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to baseline.todo.json file.
        """
        # Extract parent mission ID (e.g., "MF-001-A" -> "MF-001")
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.todo.json"

    def baseline_path(self, sub_mission_id: str) -> Path:
        """Get path to baseline.json for a sub-mission.

        Args:
            sub_mission_id: Sub-mission identifier (e.g., 'MF-001-A').

        Returns:
            Path to baseline.json file.
        """
        # Extract parent mission ID (e.g., "MF-001-A" -> "MF-001")
        parent_id = sub_mission_id.rsplit("-", 1)[0]
        return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.json"


# Made with Bob
>>>>>>> REPLACE
</diff>
</apply_diff>

---

**User:**

[apply_diff for 'src/missionforge/core/workspace.py'] Result:
<file_write_result>
<path>src/missionforge/core/workspace.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<notice>Making multiple related changes in a single apply_diff is more efficient. If other changes are needed in this file, please include them as additional SEARCH/REPLACE blocks.</notice>
<environment_details>
# VSCode Visible Files
src/missionforge/core/workspace.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
src/missionforge/core/workspace.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:41:09.362Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.08

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

Perfect! I've successfully implemented Phase 4 of MF-008. Let me present the completion summary.

<attempt_completion>
<result>
Phase 4 of MF-008 (Supporting Infrastructure) has been successfully implemented:

## Changes Made

### 1. Added Baseline-Specific Exceptions to `src/missionforge/core/exceptions.py`:

- **BaselineAlreadyExistsError**: Raised when baseline.json already exists for a sub-mission
  - Includes sub_mission_id and baseline_path in error message
  - Suggests using `missionforge baseline reset <id> --force` to re-capture

- **BaselineNotCapturedError**: Raised when trying to commit without capturing first
  - Includes sub_mission_id in error message
  - Suggests running `missionforge baseline capture <id>` first

- **BaselineValidationError**: Generic exception for baseline validation failures
  - Follows existing pattern for flexible error messages

- **BaselineIncompleteError**: Raised when baseline.todo.json has unfilled metric values
  - Lists all unfilled metrics in a formatted list
  - Suggests filling all values before committing

### 2. Added Baseline Path Helpers to `src/missionforge/core/workspace.py`:

- **baseline_todo_path(sub_mission_id)**: Returns Path to baseline.todo.json
  - Extracts parent mission ID from sub-mission ID (e.g., "MF-001-A" → "MF-001")
  - Uses existing `sub_mission_path()` method for consistency
  - Returns: `.missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json`

- **baseline_path(sub_mission_id)**: Returns Path to baseline.json
  - Same parent ID extraction logic
  - Returns: `.missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json`

## Implementation Details

All code follows existing patterns:
- Exceptions inherit from MissionForgeError with helpful messages and suggestions
- Workspace methods use consistent Path handling and documentation style
- Parent ID extraction uses `rsplit("-", 1)[0]` to handle mission IDs correctly
- All additions placed before "# Made with Bob" comments as required

The infrastructure is now ready for Phase 2 (Core Service Layer) implementation.
</result>
</attempt_completion>

