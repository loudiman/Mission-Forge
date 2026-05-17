**User:**

<task>
Implement Phase 1 of MF-008: Data Models and Schemas

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. This is a new feature that tracks custom semantic metrics for sub-missions (separate from existing git-based metrics).

**Your Task:**
Implement Phase 1 from the implementation plan at `issues/MF-008-implementation-plan.md`:

1. **Add new Pydantic models to `src/missionforge/models/schemas.py`:**
   - `SubMissionBaselineMetric`: Single metric with metric_id, description, baseline_target, value
   - `SubMissionBaseline`: Container with sub_mission_id, timestamp, status, metrics list

2. **Add new JSON schemas to `src/missionforge/schemas/json_schemas.py`:**
   - `SUB_MISSION_BASELINE_TODO_SCHEMA`: For baseline.todo.json (value can be null)
   - `SUB_MISSION_BASELINE_SCHEMA`: For baseline.json (value must be filled)

**Data Structure Reference:**
```json
{
  "sub_mission_id": "MF-001-A",
  "timestamp": "2026-05-16T16:30:00Z",
  "status": "committed",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "A REST endpoint exists at /api/matchmaking",
      "baseline_target": false,
      "value": false
    }
  ]
}
```

**Requirements:**
- baseline_target and value can be: bool, int, float, or str
- For baseline.todo.json: value can be null (Bob fills it)
- For baseline.json: value must be filled, timestamp and status required
- Add proper field validators and descriptions
- Follow existing code style in schemas.py

**Scope:**
- ONLY modify `src/missionforge/models/schemas.py` and `src/missionforge/schemas/json_schemas.py`
- Do NOT create CLI commands, services, or tests yet
- Add models at the end of schemas.py before the "# Made with Bob" comment

When complete, use `attempt_completion` with a summary of what was added.
</task>
<environment_details>
# VSCode Visible Files
issues/MF-008-implementation-plan.md

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:00.538Z
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

I'll start by reading the existing schema files to understand the current structure and code style.

<read_file>
<args>
<file>
<path>src/missionforge/models/schemas.py</path>
</file>
<file>
<path>src/missionforge/schemas/json_schemas.py</path>
</file>
<file>
<path>issues/MF-008-implementation-plan.md</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'src/missionforge/models/schemas.py', 'src/missionforge/schemas/json_schemas.py', 'issues/MF-008-implementation-plan.md'] Result:
<files>
<file><path>src/missionforge/models/schemas.py</path>
<content lines="1-324">
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
323 | 
324 | # Made with Bob
</content>
</file>
<file><path>src/missionforge/schemas/json_schemas.py</path>
<content lines="1-170">
  1 | """JSON Schema definitions for validation files."""
  2 | 
  3 | from typing import Any
  4 | 
  5 | # JSON Schema for baseline.json and baseline.todo.json
  6 | BASELINE_SCHEMA: dict[str, Any] = {
  7 |     "$schema": "http://json-schema.org/draft-07/schema#",
  8 |     "title": "Mission Baseline",
  9 |     "description": "Baseline metrics captured before mission execution",
 10 |     "type": "object",
 11 |     "required": ["mission_id", "timestamp", "git_commit", "metrics"],
 12 |     "properties": {
 13 |         "mission_id": {
 14 |             "type": "string",
 15 |             "pattern": "^[A-Z]{2,4}-\\d{3}(-[A-Z])?$",
 16 |             "description": "Mission or sub-mission identifier",
 17 |             "examples": ["MF-001", "MF-001-A"],
 18 |         },
 19 |         "timestamp": {
 20 |             "type": "string",
 21 |             "format": "date-time",
 22 |             "description": "ISO 8601 timestamp of baseline capture",
 23 |         },
 24 |         "git_commit": {
 25 |             "type": "string",
 26 |             "pattern": "^[0-9a-f]{7,40}$",
 27 |             "description": "Git commit hash at baseline",
 28 |         },
 29 |         "metrics": {
 30 |             "type": "object",
 31 |             "required": ["files_changed", "lines_added", "lines_removed"],
 32 |             "properties": {
 33 |                 "files_changed": {
 34 |                     "type": "integer",
 35 |                     "minimum": 0,
 36 |                     "description": "Number of files changed",
 37 |                 },
 38 |                 "lines_added": {
 39 |                     "type": "integer",
 40 |                     "minimum": 0,
 41 |                     "description": "Number of lines added",
 42 |                 },
 43 |                 "lines_removed": {
 44 |                     "type": "integer",
 45 |                     "minimum": 0,
 46 |                     "description": "Number of lines removed",
 47 |                 },
 48 |                 "test_coverage": {
 49 |                     "type": "number",
 50 |                     "minimum": 0,
 51 |                     "maximum": 100,
 52 |                     "description": "Test coverage percentage",
 53 |                 },
 54 |                 "custom_metrics": {
 55 |                     "type": "object",
 56 |                     "additionalProperties": {"type": "number"},
 57 |                     "description": "Custom metrics defined by mission",
 58 |                 },
 59 |             },
 60 |         },
 61 |     },
 62 | }
 63 | 
 64 | # JSON Schema for validation.json and validation.todo.json
 65 | VALIDATION_SCHEMA: dict[str, Any] = {
 66 |     "$schema": "http://json-schema.org/draft-07/schema#",
 67 |     "title": "Mission Validation",
 68 |     "description": "Validation results after mission execution",
 69 |     "type": "object",
 70 |     "required": ["mission_id", "timestamp", "git_commit", "metrics", "passed"],
 71 |     "properties": {
 72 |         "mission_id": {
 73 |             "type": "string",
 74 |             "pattern": "^[A-Z]{2,4}-\\d{3}(-[A-Z])?$",
 75 |             "description": "Mission or sub-mission identifier",
 76 |             "examples": ["MF-001", "MF-001-A"],
 77 |         },
 78 |         "timestamp": {
 79 |             "type": "string",
 80 |             "format": "date-time",
 81 |             "description": "ISO 8601 timestamp of validation",
 82 |         },
 83 |         "git_commit": {
 84 |             "type": "string",
 85 |             "pattern": "^[0-9a-f]{7,40}$",
 86 |             "description": "Git commit hash at validation",
 87 |         },
 88 |         "metrics": {
 89 |             "type": "object",
 90 |             "required": ["files_changed", "lines_added", "lines_removed", "tests_passed"],
 91 |             "properties": {
 92 |                 "files_changed": {
 93 |                     "type": "integer",
 94 |                     "minimum": 0,
 95 |                     "description": "Number of files changed",
 96 |                 },
 97 |                 "lines_added": {
 98 |                     "type": "integer",
 99 |                     "minimum": 0,
100 |                     "description": "Number of lines added",
101 |                 },
102 |                 "lines_removed": {
103 |                     "type": "integer",
104 |                     "minimum": 0,
105 |                     "description": "Number of lines removed",
106 |                 },
107 |                 "test_coverage": {
108 |                     "type": "number",
109 |                     "minimum": 0,
110 |                     "maximum": 100,
111 |                     "description": "Test coverage percentage",
112 |                 },
113 |                 "tests_passed": {
114 |                     "type": "boolean",
115 |                     "description": "Whether all tests passed",
116 |                 },
117 |                 "custom_metrics": {
118 |                     "type": "object",
119 |                     "additionalProperties": {"type": "number"},
120 |                     "description": "Custom metrics defined by mission",
121 |                 },
122 |             },
123 |         },
124 |         "passed": {
125 |             "type": "boolean",
126 |             "description": "Whether validation passed all checks",
127 |         },
128 |         "errors": {
129 |             "type": "array",
130 |             "items": {"type": "string"},
131 |             "description": "Validation errors if any",
132 |         },
133 |     },
134 | }
135 | 
136 | 
137 | def validate_json_against_schema(data: dict[str, Any], schema: dict[str, Any]) -> None:
138 |     """Validate JSON data against a schema.
139 | 
140 |     Args:
141 |         data: JSON data to validate.
142 |         schema: JSON schema to validate against.
143 | 
144 |     Raises:
145 |         jsonschema.ValidationError: If validation fails.
146 |     """
147 |     import jsonschema  # type: ignore[import-untyped]
148 | 
149 |     jsonschema.validate(instance=data, schema=schema)
150 | 
151 | 
152 | def get_baseline_schema() -> dict[str, Any]:
153 |     """Get baseline JSON schema.
154 | 
155 |     Returns:
156 |         JSON schema for baseline files.
157 |     """
158 |     return BASELINE_SCHEMA
159 | 
160 | 
161 | def get_validation_schema() -> dict[str, Any]:
162 |     """Get validation JSON schema.
163 | 
164 |     Returns:
165 |         JSON schema for validation files.
166 |     """
167 |     return VALIDATION_SCHEMA
168 | 
169 | 
170 | # Made with Bob
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
Current time in ISO 8601 UTC format: 2026-05-17T06:39:04.213Z
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

I'll implement Phase 1 of MF-008 by adding the new Pydantic models and JSON schemas. Let me start by creating a todo list for tracking progress.

<update_todo_list>
<todos>
[ ] Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py
[ ] Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py
[ ] Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py
[ ] Verify all changes follow existing code style
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
issues/MF-008-implementation-plan.md

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:17.661Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.06

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Pending |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | Pending |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Pending |
| 4 | Verify all changes follow existing code style | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll add the new Pydantic models to `schemas.py`. I'll insert them before the "# Made with Bob" comment at the end of the file.

<insert_content>
<path>src/missionforge/models/schemas.py</path>
<line>323</line>
<content>
class SubMissionBaselineMetric(BaseModel):
    """A single metric in a sub-mission baseline."""

    metric_id: str = Field(..., description="Unique identifier for the metric")
    description: str = Field(..., description="Human-readable description of what is measured")
    baseline_target: bool | int | float | str = Field(
        ..., description="Expected baseline value before implementation"
    )
    value: bool | int | float | str | None = Field(
        None, description="Actual measured value (null until filled by Bob)"
    )

    @field_validator("metric_id")
    @classmethod
    def validate_metric_id(cls, v: str) -> str:
        """Ensure metric_id is not empty."""
        if not v.strip():
            raise ValueError("metric_id cannot be empty")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Ensure description is not empty."""
        if not v.strip():
            raise ValueError("description cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_value_type(self) -> "SubMissionBaselineMetric":
        """Ensure value type matches baseline_target type when value is not None."""
        if self.value is not None:
            target_type = type(self.baseline_target)
            value_type = type(self.value)
            if target_type != value_type:
                raise ValueError(
                    f"Value type ({value_type.__name__}) does not match "
                    f"baseline_target type ({target_type.__name__})"
                )
        return self


class SubMissionBaseline(BaseModel):
    """Baseline for sub-mission custom metrics."""

    sub_mission_id: str = Field(..., description="Sub-mission identifier (e.g., MF-001-A)")
    timestamp: str | None = Field(
        None, description="ISO 8601 timestamp when baseline was committed"
    )
    status: str | None = Field(
        None, description="Baseline status: 'captured' or 'committed'"
    )
    metrics: list[SubMissionBaselineMetric] = Field(
        ..., description="List of baseline metrics"
    )

    @field_validator("sub_mission_id")
    @classmethod
    def validate_sub_mission_id(cls, v: str) -> str:
        """Validate sub-mission ID format."""
        import re

        pattern = r"^[A-Z]{2,4}-\d{3}-[A-Z]$"
        if not re.match(pattern, v):
            raise ValueError(
                f"Invalid sub-mission ID format: {v}. "
                "Must match pattern: [A-Z]{{2,4}}-\\d{{3}}-[A-Z] (e.g., MF-001-A)"
            )
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Validate status is one of allowed values."""
        if v is not None and v not in ("captured", "committed"):
            raise ValueError(f"Invalid status: {v}. Must be 'captured' or 'committed'")
        return v

    @field_validator("metrics")
    @classmethod
    def validate_metrics_not_empty(cls, v: list[SubMissionBaselineMetric]) -> list[SubMissionBaselineMetric]:
        """Ensure at least one metric is defined."""
        if not v:
            raise ValueError("At least one metric must be defined")
        return v


</content>
</insert_content>

---

**User:**

[insert_content for 'src/missionforge/models/schemas.py'] Result:
<file_write_result>
<path>src/missionforge/models/schemas.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
src/missionforge/models/schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
src/missionforge/models/schemas.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:34.431Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.11

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Pending |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | Pending |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Pending |
| 4 | Verify all changes follow existing code style | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py
[-] Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py
[ ] Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py
[ ] Verify all changes follow existing code style
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
src/missionforge/models/schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:37.479Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.16

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Completed |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | In Progress |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Pending |
| 4 | Verify all changes follow existing code style | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll add the JSON schemas to `json_schemas.py`. I'll insert them before the "# Made with Bob" comment.

<insert_content>
<path>src/missionforge/schemas/json_schemas.py</path>
<line>169</line>
<content>
# JSON Schema for sub-mission baseline.todo.json (value can be null)
SUB_MISSION_BASELINE_TODO_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sub-Mission Baseline TODO",
    "description": "Baseline metrics template for Bob to fill",
    "type": "object",
    "required": ["sub_mission_id", "metrics"],
    "properties": {
        "sub_mission_id": {
            "type": "string",
            "pattern": "^[A-Z]{2,4}-\\d{3}-[A-Z]$",
            "description": "Sub-mission identifier",
            "examples": ["MF-001-A", "FG-042-B"],
        },
        "metrics": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["metric_id", "description", "baseline_target", "value"],
                "properties": {
                    "metric_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Unique identifier for the metric",
                    },
                    "description": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Human-readable description of what is measured",
                    },
                    "baseline_target": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "Expected baseline value before implementation",
                    },
                    "value": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                            {"type": "null"},
                        ],
                        "description": "Actual measured value (null until filled by Bob)",
                    },
                },
            },
        },
    },
}

# JSON Schema for sub-mission baseline.json (value must be filled)
SUB_MISSION_BASELINE_SCHEMA: dict[str, Any] = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sub-Mission Baseline",
    "description": "Committed baseline metrics for sub-mission",
    "type": "object",
    "required": ["sub_mission_id", "timestamp", "status", "metrics"],
    "properties": {
        "sub_mission_id": {
            "type": "string",
            "pattern": "^[A-Z]{2,4}-\\d{3}-[A-Z]$",
            "description": "Sub-mission identifier",
            "examples": ["MF-001-A", "FG-042-B"],
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO 8601 timestamp when baseline was committed",
        },
        "status": {
            "type": "string",
            "enum": ["captured", "committed"],
            "description": "Baseline status",
        },
        "metrics": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["metric_id", "description", "baseline_target", "value"],
                "properties": {
                    "metric_id": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Unique identifier for the metric",
                    },
                    "description": {
                        "type": "string",
                        "minLength": 1,
                        "description": "Human-readable description of what is measured",
                    },
                    "baseline_target": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "Expected baseline value before implementation",
                    },
                    "value": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "string"},
                        ],
                        "description": "Actual measured value (must be filled)",
                    },
                },
            },
        },
    },
}


def get_sub_mission_baseline_todo_schema() -> dict[str, Any]:
    """Get sub-mission baseline TODO JSON schema.

    Returns:
        JSON schema for baseline.todo.json files.
    """
    return SUB_MISSION_BASELINE_TODO_SCHEMA


def get_sub_mission_baseline_schema() -> dict[str, Any]:
    """Get sub-mission baseline JSON schema.

    Returns:
        JSON schema for baseline.json files.
    """
    return SUB_MISSION_BASELINE_SCHEMA


</content>
</insert_content>

---

**User:**

[insert_content for 'src/missionforge/schemas/json_schemas.py'] Result:
<file_write_result>
<path>src/missionforge/schemas/json_schemas.py</path>
<operation>modified</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
src/missionforge/schemas/json_schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py

# Recently Modified Files
These files have been modified since you last accessed them (file was just edited so you may need to re-read it before editing):
src/missionforge/schemas/json_schemas.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:52.868Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.21

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Completed |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | In Progress |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Pending |
| 4 | Verify all changes follow existing code style | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py
[x] Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py
[x] Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py
[-] Verify all changes follow existing code style
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
src/missionforge/schemas/json_schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:55.645Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.27

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Completed |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | Completed |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Completed |
| 4 | Verify all changes follow existing code style | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me verify the changes by reading both modified files to ensure they follow the existing code style and are correct.

<read_file>
<args>
<file>
<path>src/missionforge/models/schemas.py</path>
<line_range>320-410</line_range>
</file>
<file>
<path>src/missionforge/schemas/json_schemas.py</path>
<line_range>165-300</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'src/missionforge/models/schemas.py', 'src/missionforge/schemas/json_schemas.py'] Result:
<files>
<file><path>src/missionforge/models/schemas.py</path>
<content lines="320-410">
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
</content>
</file>
<file><path>src/missionforge/schemas/json_schemas.py</path>
<content lines="165-300">
165 |         JSON schema for validation files.
166 |     """
167 |     return VALIDATION_SCHEMA
168 | 
169 | # JSON Schema for sub-mission baseline.todo.json (value can be null)
170 | SUB_MISSION_BASELINE_TODO_SCHEMA: dict[str, Any] = {
171 |     "$schema": "http://json-schema.org/draft-07/schema#",
172 |     "title": "Sub-Mission Baseline TODO",
173 |     "description": "Baseline metrics template for Bob to fill",
174 |     "type": "object",
175 |     "required": ["sub_mission_id", "metrics"],
176 |     "properties": {
177 |         "sub_mission_id": {
178 |             "type": "string",
179 |             "pattern": "^[A-Z]{2,4}-\\d{3}-[A-Z]$",
180 |             "description": "Sub-mission identifier",
181 |             "examples": ["MF-001-A", "FG-042-B"],
182 |         },
183 |         "metrics": {
184 |             "type": "array",
185 |             "minItems": 1,
186 |             "items": {
187 |                 "type": "object",
188 |                 "required": ["metric_id", "description", "baseline_target", "value"],
189 |                 "properties": {
190 |                     "metric_id": {
191 |                         "type": "string",
192 |                         "minLength": 1,
193 |                         "description": "Unique identifier for the metric",
194 |                     },
195 |                     "description": {
196 |                         "type": "string",
197 |                         "minLength": 1,
198 |                         "description": "Human-readable description of what is measured",
199 |                     },
200 |                     "baseline_target": {
201 |                         "oneOf": [
202 |                             {"type": "boolean"},
203 |                             {"type": "integer"},
204 |                             {"type": "number"},
205 |                             {"type": "string"},
206 |                         ],
207 |                         "description": "Expected baseline value before implementation",
208 |                     },
209 |                     "value": {
210 |                         "oneOf": [
211 |                             {"type": "boolean"},
212 |                             {"type": "integer"},
213 |                             {"type": "number"},
214 |                             {"type": "string"},
215 |                             {"type": "null"},
216 |                         ],
217 |                         "description": "Actual measured value (null until filled by Bob)",
218 |                     },
219 |                 },
220 |             },
221 |         },
222 |     },
223 | }
224 | 
225 | # JSON Schema for sub-mission baseline.json (value must be filled)
226 | SUB_MISSION_BASELINE_SCHEMA: dict[str, Any] = {
227 |     "$schema": "http://json-schema.org/draft-07/schema#",
228 |     "title": "Sub-Mission Baseline",
229 |     "description": "Committed baseline metrics for sub-mission",
230 |     "type": "object",
231 |     "required": ["sub_mission_id", "timestamp", "status", "metrics"],
232 |     "properties": {
233 |         "sub_mission_id": {
234 |             "type": "string",
235 |             "pattern": "^[A-Z]{2,4}-\\d{3}-[A-Z]$",
236 |             "description": "Sub-mission identifier",
237 |             "examples": ["MF-001-A", "FG-042-B"],
238 |         },
239 |         "timestamp": {
240 |             "type": "string",
241 |             "format": "date-time",
242 |             "description": "ISO 8601 timestamp when baseline was committed",
243 |         },
244 |         "status": {
245 |             "type": "string",
246 |             "enum": ["captured", "committed"],
247 |             "description": "Baseline status",
248 |         },
249 |         "metrics": {
250 |             "type": "array",
251 |             "minItems": 1,
252 |             "items": {
253 |                 "type": "object",
254 |                 "required": ["metric_id", "description", "baseline_target", "value"],
255 |                 "properties": {
256 |                     "metric_id": {
257 |                         "type": "string",
258 |                         "minLength": 1,
259 |                         "description": "Unique identifier for the metric",
260 |                     },
261 |                     "description": {
262 |                         "type": "string",
263 |                         "minLength": 1,
264 |                         "description": "Human-readable description of what is measured",
265 |                     },
266 |                     "baseline_target": {
267 |                         "oneOf": [
268 |                             {"type": "boolean"},
269 |                             {"type": "integer"},
270 |                             {"type": "number"},
271 |                             {"type": "string"},
272 |                         ],
273 |                         "description": "Expected baseline value before implementation",
274 |                     },
275 |                     "value": {
276 |                         "oneOf": [
277 |                             {"type": "boolean"},
278 |                             {"type": "integer"},
279 |                             {"type": "number"},
280 |                             {"type": "string"},
281 |                         ],
282 |                         "description": "Actual measured value (must be filled)",
283 |                     },
284 |                 },
285 |             },
286 |         },
287 |     },
288 | }
289 | 
290 | 
291 | def get_sub_mission_baseline_todo_schema() -> dict[str, Any]:
292 |     """Get sub-mission baseline TODO JSON schema.
293 | 
294 |     Returns:
295 |         JSON schema for baseline.todo.json files.
296 |     """
297 |     return SUB_MISSION_BASELINE_TODO_SCHEMA
298 | 
299 | 
300 | def get_sub_mission_baseline_schema() -> dict[str, Any]:
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
src/missionforge/schemas/json_schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:39:59.538Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.33

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Completed |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | Completed |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Completed |
| 4 | Verify all changes follow existing code style | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! Let me verify the changes are complete by checking the end of the json_schemas.py file to ensure the helper functions are complete.

<read_file>
<args>
<file>
<path>src/missionforge/schemas/json_schemas.py</path>
<line_range>300-310</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'src/missionforge/schemas/json_schemas.py'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>src/missionforge/schemas/json_schemas.py</path>
<content lines="300-310">
300 | def get_sub_mission_baseline_schema() -> dict[str, Any]:
301 |     """Get sub-mission baseline JSON schema.
302 | 
303 |     Returns:
304 |         JSON schema for baseline.json files.
305 |     """
306 |     return SUB_MISSION_BASELINE_SCHEMA
307 | 
308 | 
309 | 
310 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
src/missionforge/schemas/json_schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:40:03.232Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.39

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Completed |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | Completed |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Completed |
| 4 | Verify all changes follow existing code style | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py
[x] Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py
[x] Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py
[x] Verify all changes follow existing code style
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
src/missionforge/schemas/json_schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:40:13.281Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.46

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Add SubMissionBaselineMetric and SubMissionBaseline models to schemas.py | Completed |
| 2 | Add SUB_MISSION_BASELINE_TODO_SCHEMA to json_schemas.py | Completed |
| 3 | Add SUB_MISSION_BASELINE_SCHEMA to json_schemas.py | Completed |
| 4 | Verify all changes follow existing code style | Completed |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Phase 1 of MF-008 implementation is complete. I have successfully added the data models and JSON schemas for the baseline capture and commit flow.

## Changes Made:

### 1. Added Pydantic Models to `src/missionforge/models/schemas.py`:

**SubMissionBaselineMetric** (lines 323-362):
- Fields: `metric_id`, `description`, `baseline_target`, `value`
- Supports bool, int, float, or str types for baseline_target and value
- Value can be null (for baseline.todo.json)
- Validators ensure metric_id and description are not empty
- Type validation ensures value type matches baseline_target type when filled

**SubMissionBaseline** (lines 365-407):
- Fields: `sub_mission_id`, `timestamp`, `status`, `metrics`
- Contains list of SubMissionBaselineMetric objects
- Validates sub-mission ID format (e.g., MF-001-A)
- Validates status is either "captured" or "committed"
- Ensures at least one metric is defined

### 2. Added JSON Schemas to `src/missionforge/schemas/json_schemas.py`:

**SUB_MISSION_BASELINE_TODO_SCHEMA** (lines 169-223):
- For baseline.todo.json files
- Value field can be null (Bob fills this)
- Only requires sub_mission_id and metrics
- Timestamp and status are optional

**SUB_MISSION_BASELINE_SCHEMA** (lines 225-288):
- For baseline.json files (committed baseline)
- Value field must be filled (cannot be null)
- Requires sub_mission_id, timestamp, status, and metrics
- Status must be "captured" or "committed"

**Helper Functions** (lines 291-306):
- `get_sub_mission_baseline_todo_schema()`: Returns TODO schema
- `get_sub_mission_baseline_schema()`: Returns committed schema

## Code Style Compliance:
✓ Follows existing Pydantic model patterns with Field descriptors
✓ Uses proper type hints (bool | int | float | str | None)
✓ Includes comprehensive field validators
✓ Matches JSON schema structure from existing BASELINE_SCHEMA
✓ Added before "# Made with Bob" comments in both files
✓ Includes proper docstrings and descriptions

## Ready for Next Phase:
These models and schemas are now ready to be used by the BaselineService in Phase 2 for implementing the capture, commit, and reset operations.
</result>
</attempt_completion>

