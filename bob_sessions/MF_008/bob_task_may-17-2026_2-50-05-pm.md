**User:**

<task>
see issue 8 in gh issues?
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:24:38.593Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>


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

I'll fetch GitHub issue #8 to see what needs to be addressed.

<fetch_github_issue>
<issue_number>8</issue_number>
</fetch_github_issue>

---

**User:**

[fetch_github_issue for issue #8 with change analysis] Result:
<fetch_github_issue>
<issue_number>8</issue_number>
<title>MF-008: Baseline Capture and Commit Flow</title>
<body># MF-008: Baseline Capture and Commit Flow

## Priority
**MUST FINISH** - Required for project viability

## Phase
Phase 1 - Core CLI Harness

## Dependencies
- MF-001 (CLI Foundation)
- MF-002 (Schemas) - needs baseline + sub-mission schemas

NOT a hard dependency: decompose-command. Baseline operates on any `sub-mission.yaml` that conforms to the schema — for development and tests, hand-authored sub-mission YAML fixtures are sufficient. Decompose is just one producer of those files.

## Parallel Work
Runs in parallel with workspace-commands, decompose-command, plan-command, and next-command once schemas land. Only sub-mission-validation downstream of this is blocked on a real baseline.json.

## Objective
Implement baseline measurement workflow for sub-missions: capture baseline.todo.json and commit to immutable baseline.json.

## Tasks
- [ ] Implement `missionforge baseline &lt;sub-mission-id&gt; --capture` command
- [ ] Read sub-mission metrics from sub-mission.yaml
- [ ] Generate baseline.todo.json with:
  - metric_id
  - description
  - baseline_target
  - value (empty for Bob to fill)
- [ ] Prevent capture if baseline.json already exists (unless --force)
- [ ] Implement `missionforge baseline &lt;sub-mission-id&gt; --commit` command
- [ ] Validate all baseline fields are filled
- [ ] Validate field types match metric definitions
- [ ] Check values are reasonable (not obviously wrong)
- [ ] Write immutable baseline.json with timestamp
- [ ] Prevent modification after commit
- [ ] Add --reset flag to allow re-capture if needed
- [ ] Display baseline summary in terminal
- [ ] Add unit and integration tests

## Acceptance Criteria
- [ ] `--capture` generates correct baseline.todo.json structure
- [ ] baseline.todo.json is easy for Bob to fill
- [ ] Cannot capture if baseline already committed (without --force)
- [ ] `--commit` validates all fields are filled
- [ ] Type validation catches incorrect value types
- [ ] baseline.json is immutable after commit
- [ ] Timestamp is recorded in baseline.json
- [ ] Terminal output shows clear summary
- [ ] Integration tests cover capture → fill → commit flow

## Example baseline.todo.json
```json
{
  &quot;sub_mission_id&quot;: &quot;MF-001-A&quot;,
  &quot;metrics&quot;: [
    {
      &quot;metric_id&quot;: &quot;rest_endpoint_exists&quot;,
      &quot;description&quot;: &quot;A REST endpoint exists at /api/matchmaking&quot;,
      &quot;baseline_target&quot;: false,
      &quot;value&quot;: null
    }
  ]
}
```

## Example baseline.json
```json
{
  &quot;sub_mission_id&quot;: &quot;MF-001-A&quot;,
  &quot;timestamp&quot;: &quot;2026-05-16T16:30:00Z&quot;,
  &quot;status&quot;: &quot;committed&quot;,
  &quot;metrics&quot;: [
    {
      &quot;metric_id&quot;: &quot;rest_endpoint_exists&quot;,
      &quot;description&quot;: &quot;A REST endpoint exists at /api/matchmaking&quot;,
      &quot;baseline_target&quot;: false,
      &quot;value&quot;: false
    }
  ]
}
```

## Technical Notes
- baseline.json should be immutable (add file permissions check)
- Validate metric values match expected types (bool, int, string)
- Add metadata: timestamp, status, sub_mission_id
- Clear error messages for validation failures

## Estimated Effort
**3-4 hours** (hackathon pace)

## Developer Assignment
Backend/CLI Developer (can work in parallel with MF-006/MF-007)
</body>
<state>open</state>
<labels></labels>
<url>https://github.com/loudiman/Mission-Forge/issues/8</url>
<created_at>2026-05-16T17:01:41Z</created_at>
<updated_at>2026-05-16T17:01:41Z</updated_at>
<analysis>
<summary>Analyzed 0 file(s) with changes against issue #8: &quot;MF-008: Baseline Capture and Commit Flow&quot;</summary>
<alignment_score>Manual review required</alignment_score>
<matches_intent>false</matches_intent>
<identified_changes>
<change>Modified 0 file(s)</change>
<change>Added 0 line(s)</change>
<change>Removed 0 line(s)</change>
</identified_changes>
<gaps>

</gaps>
<out_of_scope>

</out_of_scope>
<recommendations>
<recommendation>Review the changes to ensure they address the issue requirements</recommendation>
<recommendation>Verify that all acceptance criteria from the issue are met</recommendation>
<recommendation>Check for any unintended side effects or scope creep</recommendation>
</recommendations>
</analysis>
</fetch_github_issue>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:26:28.943Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.03

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze issue #8 (MF-008: Baseline Capture and Commit Flow) and gather context to create a detailed implementation plan.

<read_file>
<args>
  <file>
    <path>issues/baseline-flow.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'issues/baseline-flow.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>issues/baseline-flow.md</path>
<content lines="1-93">
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


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:26:35.940Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>src/missionforge/models/schemas.py</path>
  </file>
  <file>
    <path>src/missionforge/schemas/json_schemas.py</path>
  </file>
  <file>
    <path>src/missionforge/cli/app.py</path>
  </file>
  <file>
    <path>src/missionforge/core/workspace.py</path>
  </file>
  <file>
    <path>docs/schemas/mission-schema-examples.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
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
<file><path>src/missionforge/cli/app.py</path>
<content lines="1-100">
  1 | """Main CLI application."""
  2 | 
  3 | from pathlib import Path
  4 | 
  5 | import typer
  6 | from rich.console import Console
  7 | 
  8 | from ..core.config import MissionForgeConfig
  9 | from ..core.exceptions import MissionForgeError
 10 | from ..core.logging import setup_logging
 11 | from ..core.workspace import Workspace
 12 | from .commands import workspace
 13 | 
 14 | app = typer.Typer(
 15 |     name="missionforge",
 16 |     help="AI-assisted mission decomposition and validation",
 17 |     add_completion=False,
 18 |     rich_markup_mode="rich",
 19 | )
 20 | 
 21 | console = Console()
 22 | 
 23 | # Global state
 24 | _workspace: Workspace | None = None
 25 | _config: MissionForgeConfig | None = None
 26 | 
 27 | 
 28 | def get_workspace() -> Workspace:
 29 |     """Get or create workspace instance.
 30 | 
 31 |     Returns:
 32 |         Workspace instance.
 33 |     """
 34 |     global _workspace
 35 |     if _workspace is None:
 36 |         _workspace = Workspace()
 37 |     return _workspace
 38 | 
 39 | 
 40 | def get_config() -> MissionForgeConfig:
 41 |     """Get or create config instance.
 42 | 
 43 |     Returns:
 44 |         Configuration instance.
 45 |     """
 46 |     global _config
 47 |     if _config is None:
 48 |         config_path = MissionForgeConfig.get_default_config_path()
 49 |         _config = MissionForgeConfig.load(config_path)
 50 |     return _config
 51 | 
 52 | 
 53 | # Register command groups
 54 | app.add_typer(workspace.app, name="workspace")
 55 | 
 56 | 
 57 | @app.callback()
 58 | def main(
 59 |     ctx: typer.Context,
 60 |     verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
 61 |     log_file: Path | None = typer.Option(None, "--log-file", help="Log to file"),  # noqa: B008
 62 | ) -> None:
 63 |     """MissionForge CLI - AI-assisted mission management."""
 64 | 
 65 |     # Setup logging
 66 |     log_level = "DEBUG" if verbose else "INFO"
 67 |     setup_logging(level=log_level, log_file=log_file)
 68 | 
 69 |     # Store in context for commands
 70 |     ctx.obj = {"workspace": get_workspace, "config": get_config, "console": console}
 71 | 
 72 | 
 73 | @app.command()
 74 | def version() -> None:
 75 |     """Show version information."""
 76 |     console.print("[bold]MissionForge[/bold] v0.1.0")
 77 |     console.print("Python 3.11+ required")
 78 | 
 79 | 
 80 | def cli_main() -> None:
 81 |     """Entry point with error handling."""
 82 |     try:
 83 |         app()
 84 |     except MissionForgeError as e:
 85 |         console.print(e.format_error(), style="bold red")
 86 |         raise typer.Exit(1) from e
 87 |     except KeyboardInterrupt as e:
 88 |         console.print("\n[yellow]Operation cancelled by user[/yellow]")
 89 |         raise typer.Exit(130) from e
 90 |     except Exception as e:
 91 |         console.print(f"[bold red]Unexpected error:[/bold red] {e}")
 92 |         if "--verbose" in str(e) or "-v" in str(e):
 93 |             raise
 94 |         raise typer.Exit(1) from e
 95 | 
 96 | 
 97 | if __name__ == "__main__":
 98 |     cli_main()
 99 | 
100 | # Made with Bob
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
<file><path>docs/schemas/mission-schema-examples.md</path>
<content lines="1-224">
  1 | # Mission Schema Examples
  2 | 
  3 | This document provides examples of all mission schema formats used in MissionForge.
  4 | 
  5 | ## Parent Mission Schema (mission.yaml)
  6 | 
  7 | ```yaml
  8 | # Mission: MF-001
  9 | id: MF-001
 10 | goal: |
 11 |   Modernize the matchmaking service from CORBA to REST API
 12 |   while maintaining backward compatibility and game stability.
 13 | 
 14 | # Paths that sub-missions cannot modify
 15 | forbidden_paths:
 16 |   - "core/**"
 17 |   - "config/production/**"
 18 |   - "tests/integration/**"
 19 | 
 20 | # Aggregate metrics to validate across all sub-missions
 21 | aggregate_metrics:
 22 |   total_files_changed:
 23 |     max: 50
 24 |   total_lines_changed:
 25 |     max: 1000
 26 |   test_coverage:
 27 |     min: 80.0
 28 | 
 29 | # Test command to validate mission completion
 30 | test_command: "pytest tests/ --cov=src"
 31 | 
 32 | # Sub-missions will be listed here after decomposition
 33 | sub_missions:
 34 |   - MF-001-A
 35 |   - MF-001-B
 36 |   - MF-001-C
 37 | ```
 38 | 
 39 | ## Sub-Mission Schema (sub-missions/MF-001-A.yaml)
 40 | 
 41 | ```yaml
 42 | # Sub-mission: MF-001-A
 43 | id: MF-001-A
 44 | parent: MF-001
 45 | title: "Extract CORBA interface definitions"
 46 | goal: |
 47 |   Extract and document all CORBA interface definitions
 48 |   from the matchmaking service for REST API design.
 49 | 
 50 | # Dependencies on other sub-missions
 51 | depends_on: []
 52 | 
 53 | # Paths this sub-mission can modify
 54 | allowed_paths:
 55 |   - "src/matchmaking/interfaces/**"
 56 |   - "docs/api/**"
 57 | 
 58 | # Metrics for this sub-mission
 59 | metrics:
 60 |   files_changed:
 61 |     max: 10
 62 |   lines_added:
 63 |     max: 500
 64 |   test_coverage:
 65 |     min: 85.0
 66 | 
 67 | # Test command for this sub-mission
 68 | test_command: "pytest tests/unit/matchmaking/interfaces/"
 69 | ```
 70 | 
 71 | ## Baseline Schema (baseline.json)
 72 | 
 73 | ```json
 74 | {
 75 |   "mission_id": "MF-001",
 76 |   "timestamp": "2024-01-15T10:30:00Z",
 77 |   "git_commit": "abc123def456789",
 78 |   "metrics": {
 79 |     "files_changed": 0,
 80 |     "lines_added": 0,
 81 |     "lines_removed": 0,
 82 |     "test_coverage": 78.5,
 83 |     "custom_metrics": {
 84 |       "cyclomatic_complexity": 42.0,
 85 |       "code_duplication": 5.2
 86 |     }
 87 |   }
 88 | }
 89 | ```
 90 | 
 91 | ## Validation Schema (validation.json)
 92 | 
 93 | ```json
 94 | {
 95 |   "mission_id": "MF-001",
 96 |   "timestamp": "2024-01-20T15:45:00Z",
 97 |   "git_commit": "def789abc123456",
 98 |   "metrics": {
 99 |     "files_changed": 15,
100 |     "lines_added": 450,
101 |     "lines_removed": 120,
102 |     "test_coverage": 85.2,
103 |     "tests_passed": true,
104 |     "custom_metrics": {
105 |       "cyclomatic_complexity": 38.0,
106 |       "code_duplication": 3.8
107 |     }
108 |   },
109 |   "passed": true,
110 |   "errors": []
111 | }
112 | ```
113 | 
114 | ## Execution Plan Schema (plan.yaml)
115 | 
116 | ```yaml
117 | # Execution plan for MF-001
118 | execution_order:
119 |   - MF-001-A
120 |   - MF-001-B
121 |   - MF-001-C
122 | 
123 | # Dependency graph
124 | dependency_graph:
125 |   MF-001-A: []
126 |   MF-001-B: [MF-001-A]
127 |   MF-001-C: [MF-001-A, MF-001-B]
128 | ```
129 | 
130 | ## Mission ID Format Rules
131 | 
132 | ### Parent Mission IDs
133 | - Pattern: `[A-Z]{2,4}-\d{3}[A-Z]?`
134 | - Examples:
135 |   - `MF-001` - Standard format
136 |   - `PROJ-123` - 4-letter prefix
137 |   - `FG-042A` - With optional suffix letter
138 | 
139 | ### Sub-Mission IDs
140 | - Pattern: `[A-Z]{2,4}-\d{3}-[A-Z]`
141 | - Examples:
142 |   - `MF-001-A` - First sub-mission
143 |   - `MF-001-B` - Second sub-mission
144 |   - `PROJ-123-Z` - Last sub-mission
145 | 
146 | ## Metric Definition Format
147 | 
148 | Metrics can have the following constraints:
149 | 
150 | ```yaml
151 | metric_name:
152 |   min: 0.0        # Minimum allowed value (optional)
153 |   max: 100.0      # Maximum allowed value (optional)
154 |   target: 85.0    # Target value (optional)
155 | ```
156 | 
157 | At least one constraint (min, max, or target) must be specified.
158 | 
159 | ## Path Pattern Format
160 | 
161 | Path patterns use gitignore-style glob patterns:
162 | 
163 | - `**` - Matches any number of directories
164 | - `*` - Matches any characters except `/`
165 | - `?` - Matches a single character
166 | - `[abc]` - Matches any character in the set
167 | 
168 | Examples:
169 | - `src/**/*.py` - All Python files in src and subdirectories
170 | - `tests/unit/**` - All files in tests/unit and subdirectories
171 | - `*.yaml` - All YAML files in current directory
172 | - `config/[!p]*` - Config files not starting with 'p'
173 | 
174 | ## Validation Rules
175 | 
176 | ### Required Fields
177 | 
178 | **Parent Mission:**
179 | - `id` - Mission identifier
180 | - `goal` - Mission goal description
181 | 
182 | **Sub-Mission:**
183 | - `id` - Sub-mission identifier
184 | - `parent` - Parent mission ID
185 | - `title` - Short descriptive title
186 | - `goal` - Sub-mission goal description
187 | 
188 | **Baseline/Validation:**
189 | - `mission_id` - Mission or sub-mission ID
190 | - `timestamp` - ISO 8601 timestamp
191 | - `git_commit` - Git commit hash
192 | - `metrics` - Metrics object
193 | 
194 | ### Validation Checks
195 | 
196 | 1. **ID Format** - Mission and sub-mission IDs must match required patterns
197 | 2. **Parent-Child Relationship** - Sub-mission ID must match parent ID
198 | 3. **Path Patterns** - All path patterns must be valid glob patterns
199 | 4. **Forbidden Paths** - Sub-mission paths cannot conflict with forbidden paths
200 | 5. **Dependencies** - All dependencies must reference existing sub-missions
201 | 6. **Circular Dependencies** - Execution plan cannot have circular dependencies
202 | 7. **Metric Constraints** - Min cannot be greater than max
203 | 
204 | ## Error Messages
205 | 
206 | The validators provide clear, actionable error messages:
207 | 
208 | ```
209 | ❌ Mission validation failed for .missionforge/missions/MF-001/mission.yaml:
210 |   • id: Invalid mission ID format: MF001. Must match pattern: [A-Z]{2,4}-\d{3}[A-Z]? (e.g., MF-001, FG-042A)
211 | 💡 Suggestion: Fix the validation errors listed above
212 | ```
213 | 
214 | ```
215 | ❌ Sub-mission 'MF-001-B' has missing dependencies: MF-001-C
216 | 💡 Suggestion: Ensure these sub-missions exist: MF-001-C
217 | ```
218 | 
219 | ```
220 | ❌ Sub-mission 'MF-001-A' has paths that conflict with forbidden paths: core/config.py
221 | 💡 Suggestion: Remove these paths from allowed_paths or adjust forbidden_paths in parent mission
222 | ```
223 | 
224 | # Made with Bob
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:26:54.423Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.11

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>src/missionforge/core/exceptions.py</path>
  </file>
  <file>
    <path>src/missionforge/cli/commands/workspace.py</path>
  </file>
  <file>
    <path>src/missionforge/schemas/validators.py</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'src/missionforge/core/exceptions.py', 'src/missionforge/cli/commands/workspace.py', 'src/missionforge/schemas/validators.py'] Result:
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
<file><path>src/missionforge/cli/commands/workspace.py</path>
<content lines="1-148">
  1 | """Workspace management commands."""
  2 | 
  3 | from pathlib import Path
  4 | 
  5 | import typer
  6 | from rich.console import Console
  7 | from rich.table import Table
  8 | 
  9 | from ...core.exceptions import InvalidMissionIDError
 10 | from ...core.workspace import Workspace
 11 | from ..utils.validation import validate_mission_id
 12 | 
 13 | app = typer.Typer(help="Workspace management commands")
 14 | console = Console()
 15 | 
 16 | 
 17 | @app.command("init")
 18 | def init_workspace(
 19 |     mission_id: str = typer.Argument(..., help="Mission ID (e.g., MF-001)"),
 20 |     force: bool = typer.Option(False, "--force", help="Overwrite existing mission"),
 21 | ) -> None:
 22 |     """Initialize a new mission workspace."""
 23 | 
 24 |     # Validate mission ID
 25 |     if not validate_mission_id(mission_id):
 26 |         raise InvalidMissionIDError(mission_id)
 27 | 
 28 |     # Create workspace if it doesn't exist
 29 |     try:
 30 |         workspace = Workspace()
 31 |     except Exception:
 32 |         # Workspace doesn't exist, create it
 33 |         workspace_root = Path.cwd()
 34 |         workspace_dir = workspace_root / ".missionforge"
 35 |         workspace_dir.mkdir(exist_ok=True)
 36 |         workspace = Workspace(start_path=workspace_root)
 37 | 
 38 |     mission_path = workspace.mission_path(mission_id)
 39 | 
 40 |     if mission_path.exists() and not force:
 41 |         console.print(f"[yellow]Mission {mission_id} already exists[/yellow]")
 42 |         console.print("Use --force to overwrite")
 43 |         raise typer.Exit(1)
 44 | 
 45 |     # Create directory structure
 46 |     mission_path.mkdir(parents=True, exist_ok=True)
 47 |     (mission_path / "sub-missions").mkdir(exist_ok=True)
 48 | 
 49 |     # Create template files
 50 |     _create_mission_template(mission_path / "mission.yaml", mission_id)
 51 |     _create_plan_template(mission_path / "plan.yaml")
 52 |     (mission_path / "report.md").touch()
 53 | 
 54 |     console.print(f"[green]✓[/green] Initialized mission {mission_id}")
 55 |     console.print("\n[bold]Next steps:[/bold]")
 56 |     console.print(f"1. Edit {mission_path / 'mission.yaml'}")
 57 |     console.print(f"2. Run: missionforge mission validate {mission_id}")
 58 | 
 59 | 
 60 | @app.command("status")
 61 | def workspace_status() -> None:
 62 |     """Show workspace status and missions."""
 63 | 
 64 |     try:
 65 |         workspace = Workspace()
 66 |     except Exception as e:
 67 |         console.print("[yellow]No workspace initialized[/yellow]")
 68 |         console.print("Run: missionforge workspace init <mission-id>")
 69 |         raise typer.Exit(1) from e
 70 | 
 71 |     if not workspace.exists():
 72 |         console.print("[yellow]No workspace initialized[/yellow]")
 73 |         console.print("Run: missionforge workspace init <mission-id>")
 74 |         raise typer.Exit(1)
 75 | 
 76 |     # List missions
 77 |     missions = workspace.list_missions()
 78 | 
 79 |     if not missions:
 80 |         console.print("[yellow]No missions found[/yellow]")
 81 |         console.print(f"\nWorkspace location: {workspace.workspace_dir}")
 82 |         return
 83 | 
 84 |     table = Table(title="Missions")
 85 |     table.add_column("Mission ID", style="cyan")
 86 |     table.add_column("Status", style="green")
 87 |     table.add_column("Sub-missions", justify="right")
 88 | 
 89 |     for mission_id in missions:
 90 |         mission_path = workspace.mission_path(mission_id)
 91 |         sub_missions_dir = mission_path / "sub-missions"
 92 |         sub_mission_count = 0
 93 |         if sub_missions_dir.exists():
 94 |             sub_mission_count = len(list(sub_missions_dir.glob("*.yaml")))
 95 |         table.add_row(mission_id, "Active", str(sub_mission_count))
 96 | 
 97 |     console.print(table)
 98 |     console.print(f"\nWorkspace location: {workspace.workspace_dir}")
 99 | 
100 | 
101 | def _create_mission_template(path: Path, mission_id: str) -> None:
102 |     """Create mission.yaml template.
103 | 
104 |     Args:
105 |         path: Path where template should be created.
106 |         mission_id: Mission identifier.
107 |     """
108 |     template = f"""# Mission: {mission_id}
109 | id: {mission_id}
110 | goal: |
111 |   Describe the high-level goal of this mission.
112 |   What should be accomplished?
113 | 
114 | # Paths that sub-missions cannot modify
115 | forbidden_paths:
116 |   - "core/**"
117 |   - "config/**"
118 | 
119 | # Aggregate metrics to validate across all sub-missions
120 | aggregate_metrics:
121 |   total_files_changed:
122 |     max: 50
123 |   total_lines_changed:
124 |     max: 1000
125 | 
126 | # Test command to validate mission completion
127 | test_command: "pytest tests/"
128 | 
129 | # Sub-missions will be listed here after decomposition
130 | sub_missions: []
131 | """
132 |     path.write_text(template)
133 | 
134 | 
135 | def _create_plan_template(path: Path) -> None:
136 |     """Create plan.yaml template.
137 | 
138 |     Args:
139 |         path: Path where template should be created.
140 |     """
141 |     template = """# Execution plan (generated by 'missionforge plan')
142 | execution_order: []
143 | dependency_graph: {}
144 | """
145 |     path.write_text(template)
146 | 
147 | 
148 | # Made with Bob
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


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:26:58.396Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.19

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Now I'll create a comprehensive implementation plan for MF-008: Baseline Capture and Commit Flow. Let me analyze the requirements and create a detailed todo list.

<update_todo_list>
<todos>
[ ] Review and understand the baseline flow architecture from issue specifications
[ ] Design baseline.todo.json and baseline.json data structures based on sub-mission metrics
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Implement baseline capture functionality (--capture flag)
[ ] Implement baseline commit functionality (--commit flag)
[ ] Add baseline-specific exceptions to core/exceptions.py
[ ] Create baseline service layer for business logic
[ ] Implement metric type validation (bool, int, string, float)
[ ] Add file immutability checks for baseline.json
[ ] Implement --reset flag for re-capture scenarios
[ ] Create comprehensive unit tests for baseline operations
[ ] Create integration tests for capture → fill → commit workflow
[ ] Add baseline command to CLI app registration
[ ] Update workspace.py with baseline path helpers
[ ] Document baseline command usage and examples
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:27:36.433Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.28

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<ask_followup_question>
<question>I've analyzed issue #8 (MF-008: Baseline Capture and Commit Flow) and created a detailed implementation plan. However, I notice a discrepancy between the issue specification and the existing codebase:

**Issue Specification** shows baseline.todo.json/baseline.json with this structure:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "A REST endpoint exists at /api/matchmaking",
      "baseline_target": false,
      "value": null
    }
  ]
}
```

**Existing Codebase** (schemas.py, json_schemas.py) defines baseline with this structure:
```json
{
  "mission_id": "MF-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "git_commit": "abc123def456789",
  "metrics": {
    "files_changed": 0,
    "lines_added": 0,
    "lines_removed": 0,
    "test_coverage": 78.5,
    "custom_metrics": {}
  }
}
```

These are fundamentally different structures. Should I:

1. **Follow the issue specification** and create new baseline models/schemas that match the issue's structure (metric-based with baseline_target)?
2. **Adapt the issue to use existing schemas** and modify the baseline flow to work with the current BaselineMetrics model?
3. **Create both structures** - one for sub-mission metrics (issue spec) and keep existing for git-based metrics?</question>
<follow_up>
<suggest>Follow the issue specification - create new baseline models for metric-based validation (this is what the hackathon spec requires)</suggest>
<suggest>Adapt to existing schemas - modify the baseline flow to use current BaselineMetrics structure</suggest>
<suggest>Create hybrid approach - extend existing schemas to support both git metrics and custom metric validation</suggest>
<suggest>Let me review the full context first - check other issues and development_roadmap.md to understand the intended architecture</suggest>
</follow_up>
</ask_followup_question>

---

**User:**

[ask_followup_question for 'I've analyzed issue #8 (MF-008: Baseline Capture and Commit Flow) and created a detailed implementation plan. However, I notice a discrepancy between the issue specification and the existing codebase:

**Issue Specification** shows baseline.todo.json/baseline.json with this structure:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "A REST endpoint exists at /api/matchmaking",
      "baseline_target": false,
      "value": null
    }
  ]
}
```

**Existing Codebase** (schemas.py, json_schemas.py) defines baseline with this structure:
```json
{
  "mission_id": "MF-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "git_commit": "abc123def456789",
  "metrics": {
    "files_changed": 0,
    "lines_added": 0,
    "lines_removed": 0,
    "test_coverage": 78.5,
    "custom_metrics": {}
  }
}
```

These are fundamentally different structures. Should I:

1. **Follow the issue specification** and create new baseline models/schemas that match the issue's structure (metric-based with baseline_target)?
2. **Adapt the issue to use existing schemas** and modify the baseline flow to work with the current BaselineMetrics model?
3. **Create both structures** - one for sub-mission metrics (issue spec) and keep existing for git-based metrics?'] Result:
<answer>
Follow the issue specification - create new baseline models for metric-based validation (this is what the hackathon spec requires)
</answer>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:28:54.224Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.38

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! I'll follow the issue specification and create new baseline models for metric-based validation. Let me now create a comprehensive implementation plan document.

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[-] Design baseline.todo.json and baseline.json data structures based on sub-mission metrics
[ ] Create new Pydantic models for metric-based baseline in models/schemas.py
[ ] Update JSON schemas in schemas/json_schemas.py for new baseline structure
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Implement baseline capture functionality (--capture flag)
[ ] Implement baseline commit functionality (--commit flag)
[ ] Add baseline-specific exceptions to core/exceptions.py
[ ] Create baseline service layer for business logic (src/missionforge/core/baseline.py)
[ ] Implement metric type validation (bool, int, string, float)
[ ] Add file immutability checks for baseline.json
[ ] Implement --reset flag for re-capture scenarios
[ ] Create comprehensive unit tests for baseline operations
[ ] Create integration tests for capture → fill → commit workflow
[ ] Add baseline command to CLI app registration
[ ] Update workspace.py with baseline path helpers
[ ] Document baseline command usage and examples
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
The user denied this operation and provided the following feedback:
<feedback>
Let me review the full context first - check other issues and development_roadmap.md to understand the intended architecture
</feedback>
[update_todo_list] Result:
User declined to update the todoList.
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:30:20.819Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.48

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Good call! Let me review the full context by checking other issues and the development roadmap to understand the intended architecture.

<list_files>
<path>issues</path>
<recursive>false</recursive>
</list_files>

---

**User:**

[list_files for 'issues'] Result:
.DS_Store
baseline-flow.md
board-backend.md
board-frontend.md
bob-skill-slash-commands.md
cli-foundation.md
cli-wrapper-endpoints.md
decompose-command.md
demo-mission-prep.md
demo-polish-submission.md
dependency-graph-view.md
git-test-utilities.md
mission-detail-panel.md
next-command.md
parent-validation.md
plan-command.md
README.md
report-generation.md
report-renderer.md
schemas-validators.md
stakeholder-translation.md
sub-mission-validation.md
watsonx-mission-chat.md
workspace-commands.md
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:30:24.911Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.58

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>issues/README.md</path>
  </file>
  <file>
    <path>issues/schemas-validators.md</path>
  </file>
  <file>
    <path>issues/sub-mission-validation.md</path>
  </file>
  <file>
    <path>issues/cli-foundation.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>issues/README.md</path>
<content lines="1-132">
  1 | # MissionForge Development Issues
  2 | 
  3 | ## Overview
  4 | This directory contains GitHub issue drafts for the MissionForge hackathon project. Issues are organized into two phases with realistic time estimates for a 24-hour hackathon.
  5 | 
  6 | ## Issue Organization
  7 | 
  8 | ### Phase 1: Core CLI Harness (Must Finish)
  9 | **Critical Path - 16-20 hours total**
 10 | 
 11 | 1. **cli-foundation.md** (4-6h) - No dependencies, start immediately
 12 | 2. **schemas-validators.md** (3-4h) - Depends on cli-foundation
 13 | 3. **git-test-utilities.md** (2-3h) - Depends on cli-foundation, parallel with schemas
 14 | 4. **workspace-commands.md** (2-3h) - Depends on cli-foundation + schemas
 15 | 5. **decompose-command.md** (3-4h) - Depends on workspace-commands
 16 | 6. **plan-command.md** (3-4h) - Depends on decompose-command
 17 | 7. **next-command.md** (2h) - Depends on plan-command
 18 | 8. **baseline-flow.md** (3-4h) - Depends on schemas, parallel with plan/next
 19 | 9. **sub-mission-validation.md** (4-5h) - Depends on baseline + git-test-utilities
 20 | 10. **parent-validation.md** (3h) - Depends on sub-mission-validation
 21 | 11. **report-generation.md** (3h) - Depends on parent-validation
 22 | 12. **bob-skill-slash-commands.md** (2-3h) - Depends on all CLI commands
 23 | 13. **demo-mission-prep.md** (4-5h) - Depends on all CLI, can overlap with Phase 2
 24 | 
 25 | ### Phase 2: Mission Board (Should Finish)
 26 | **Enhancement Path - 12-16 hours total**
 27 | 
 28 | 14. **board-backend.md** (3-4h) - Depends on Phase 1 CLI
 29 | 15. **board-frontend.md** (4-5h) - Depends on board-backend
 30 | 16. **mission-detail-panel.md** (3h) - Depends on board-frontend
 31 | 17. **report-renderer.md** (2h) - Depends on board-frontend, parallel with detail-panel
 32 | 18. **dependency-graph-view.md** (3-4h) - Nice to have, parallel with other UI
 33 | 19. **cli-wrapper-endpoints.md** (2h) - Nice to have, depends on board-backend
 34 | 20. **watsonx-mission-chat.md** (3-4h) - Nice to have, depends on board-backend + detail-panel
 35 | 21. **stakeholder-translation.md** (3h) - Nice to have, parallel with mission-chat
 36 | 22. **demo-polish-submission.md** (5-7h) - Final integration, depends on completed features
 37 | 
 38 | ## Parallel Work Streams (4 Developers)
 39 | 
 40 | | Window | Dev A — CLI Core | Dev B — CLI Validation | Dev C — Board Backend | Dev D — Board Frontend |
 41 | |---|---|---|---|---|
 42 | | **0–6h** | cli-foundation | schemas-validators (in parallel; finalize after A's foundation lands) + git-test-utilities + author 2-3 `.missionforge/` sample fixtures | Co-design API contract with Dev D; scaffold FastAPI project | Co-design API contract; Next.js scaffold + mock API server (MSW) + wireframes |
 43 | | **6–14h** | workspace-commands → decompose-command | baseline-flow (no longer waits for decompose) → start sub-mission-validation | board-backend against fixtures | board-frontend against mock API |
 44 | | **14–22h** | plan-command → next-command | sub-mission-validation → parent-validation → report-generation | cli-wrapper-endpoints, watsonx-mission-chat (if time) | mission-detail-panel + report-renderer; swap mock → real API |
 45 | | **22–24h** | demo-mission-prep | bob-skill-slash-commands | integration + endpoint hardening | demo-polish-submission |
 46 | 
 47 | **Dropped from critical plan (nice-to-haves, do only if ahead of schedule):**
 48 | - dependency-graph-view (use ASCII fallback)
 49 | - stakeholder-translation
 50 | 
 51 | ### Cross-stream sync points
 52 | 1. **Hour 0–2**: All 4 devs agree on API contract + schemas (blocking everyone).
 53 | 2. **Hour ~6**: Dev B publishes `.missionforge/` sample fixtures → unblocks Dev C and Dev D's mock swap.
 54 | 3. **Hour ~14**: Dev C's backend goes live → Dev D swaps mock → real.
 55 | 4. **Hour ~22**: Feature freeze; full team on demo-prep + polish.
 56 | 
 57 | ## Time Budget (24 hours)
 58 | 
 59 | ### Must Complete (16-20 hours)
 60 | - Phase 1 CLI: All 13 issues
 61 | - Minimum viable product for terminal-only demo
 62 | 
 63 | ### Should Complete (8-12 hours)
 64 | - Phase 2 Board: Issues 14-17 (backend + basic frontend)
 65 | - Visual demo enhancement
 66 | 
 67 | ### Nice to Have (4-8 hours)
 68 | - Issues 18-21 (advanced UI + watsonx)
 69 | - Polish and wow factors
 70 | 
 71 | ### Cut if Needed
 72 | 1. dependency-graph-view (use ASCII diagram instead)
 73 | 2. stakeholder-translation (focus on mission-chat only)
 74 | 3. cli-wrapper-endpoints (Board read-only is fine)
 75 | 4. watsonx-mission-chat (terminal-only demo still works)
 76 | 
 77 | ## Critical Path
 78 | ```
 79 | cli-foundation (4-6h)
 80 |   ↓
 81 | schemas-validators (3-4h) + git-test-utilities (2-3h)
 82 |   ↓
 83 | workspace-commands (2-3h)
 84 |   ↓
 85 | decompose-command (3-4h)
 86 |   ↓
 87 | plan-command (3-4h) + baseline-flow (3-4h)
 88 |   ↓
 89 | next-command (2h) + sub-mission-validation (4-5h)
 90 |   ↓
 91 | parent-validation (3h)
 92 |   ↓
 93 | report-generation (3h)
 94 |   ↓
 95 | bob-skill-slash-commands (2-3h)
 96 |   ↓
 97 | demo-mission-prep (4-5h)
 98 | ```
 99 | 
100 | **Total Critical Path: ~40 hours of sequential work**
101 | **With 2 parallel developers: ~20-24 hours**
102 | **With 4 parallel developers (this plan): ~22 hours wall-clock**, assuming the hour-0 API-contract sync and hour-6 fixture handoff happen on time. Slack in Dev C/D streams absorbs CLI critical-path slippage.
103 | 
104 | ## Success Criteria
105 | 
106 | ### Minimum Viable (Must Have)
107 | - ✅ CLI can initialize missions
108 | - ✅ CLI can validate parent missions
109 | - ✅ CLI can decompose into sub-missions
110 | - ✅ CLI can plan dependency graph
111 | - ✅ CLI can track baseline and validation
112 | - ✅ CLI can generate evidence reports
113 | - ✅ Bob Skill and slash commands work
114 | - ✅ Terminal-only demo is recordable
115 | 
116 | ### Enhanced (Should Have)
117 | - ✅ Mission Board displays mission state
118 | - ✅ Board shows Kanban-style progress
119 | - ✅ Board renders evidence reports
120 | - ✅ Visual demo is compelling
121 | 
122 | ### Polish (Nice to Have)
123 | - ✅ Dependency graph visualization
124 | - ✅ Watsonx.ai integration
125 | - ✅ Stakeholder translation
126 | - ✅ Board can trigger CLI commands
127 | 
128 | ## Notes
129 | - All time estimates assume experienced developers working at hackathon pace
130 | - Estimates include implementation, testing, and basic documentation
131 | - Does not include breaks, meals, or context switching overhead
132 | - Parallel work requires clear API contracts and minimal conflicts
</content>
</file>
<file><path>issues/schemas-validators.md</path>
<content lines="1-57">
 1 | # Schema Definitions and Validators
 2 | 
 3 | ## Priority
 4 | **MUST FINISH** - Required for project viability
 5 | 
 6 | ## Phase
 7 | Phase 1 - Core CLI Harness
 8 | 
 9 | ## Dependencies
10 | - cli-foundation.md - needs base CLI structure
11 | 
12 | ## Parallel Work
13 | Can work in parallel with git-test-utilities.md after cli-foundation completes
14 | 
15 | ## Objective
16 | Define and implement YAML/JSON schemas for parent missions, sub-missions, baselines, and validation files with comprehensive validation logic.
17 | 
18 | ## Tasks
19 | - [ ] Define parent mission YAML schema with fields:
20 |   - `id`, `goal`, `forbidden_paths`, `aggregate_metrics`, `test_command`, `sub_missions`
21 | - [ ] Define sub-mission YAML schema with fields:
22 |   - `id`, `parent`, `title`, `goal`, `depends_on`, `allowed_paths`, `metrics`, `test_command`
23 | - [ ] Define baseline JSON schema (baseline.todo.json and baseline.json)
24 | - [ ] Define validation JSON schema (validation.todo.json and validation.json)
25 | - [ ] Define plan YAML schema (dependency graph, execution order)
26 | - [ ] Implement schema validators using jsonschema library
27 | - [ ] Add validation for:
28 |   - YAML/JSON syntax
29 |   - Required fields presence
30 |   - Mission ID format and consistency
31 |   - Path/glob pattern format
32 |   - Metric field structure
33 |   - Dependency reference validity
34 | - [ ] Create clear, actionable error messages for validation failures
35 | - [ ] Add unit tests for all validators
36 | 
37 | ## Acceptance Criteria
38 | - [ ] All schema files are well-documented with examples
39 | - [ ] Validators catch common errors with helpful messages
40 | - [ ] Mission ID format is enforced (e.g., MF-001, MF-001-A)
41 | - [ ] Path globs are validated for correct syntax
42 | - [ ] Metric definitions are validated for required fields
43 | - [ ] Dependency references are validated against existing sub-missions
44 | - [ ] Unit test coverage > 80% for validation logic
45 | 
46 | ## Technical Notes
47 | - Use jsonschema for JSON validation
48 | - Use PyYAML or ruamel.yaml for YAML parsing
49 | - Keep schemas strict but extensible for future features
50 | - Validation should happen early (fail fast)
51 | - Consider using Pydantic models for type safety
52 | 
53 | ## Estimated Effort
54 | **3-4 hours** (hackathon pace)
55 | 
56 | ## Developer Assignment
57 | Backend/CLI Developer (can be same as cli-foundation or different)
</content>
</file>
<file><path>issues/sub-mission-validation.md</path>
<content lines="1-114">
  1 | # MF-009: Sub-Mission Validation Capture and Commit
  2 | 
  3 | ## Priority
  4 | **MUST FINISH** - Required for project viability
  5 | 
  6 | ## Phase
  7 | Phase 1 - Core CLI Harness
  8 | 
  9 | ## Dependencies
 10 | - MF-001 (CLI Foundation)
 11 | - MF-002 (Schemas) - needs validation schema
 12 | - MF-003 (Git/Test Utilities) - needs git diff and test execution
 13 | - MF-008 (Baseline Flow) - needs baseline.json to compare against
 14 | 
 15 | ## Parallel Work
 16 | Cannot start until all dependencies complete
 17 | 
 18 | ## Objective
 19 | Implement validation workflow for sub-missions: capture deterministic evidence and Bob-filled metrics, then commit final validation results.
 20 | 
 21 | ## Tasks
 22 | - [ ] Implement `missionforge validate <sub-mission-id> --capture` command
 23 | - [ ] Run git diff to identify changed files
 24 | - [ ] Compare changed files against sub-mission allowed_paths
 25 | - [ ] Compare changed files against parent forbidden_paths
 26 | - [ ] Run sub-mission test_command and capture output
 27 | - [ ] Record test exit code
 28 | - [ ] Generate validation.todo.json with:
 29 |   - Deterministic evidence (files changed, scope check, test results)
 30 |   - Empty metric value fields for Bob to fill
 31 | - [ ] Implement `missionforge validate <sub-mission-id> --commit` command
 32 | - [ ] Validate Bob-filled metric values are complete
 33 | - [ ] Compare final values against baseline values
 34 | - [ ] Compare final values against target values
 35 | - [ ] Determine pass/fail status for each metric
 36 | - [ ] Determine overall sub-mission pass/fail status
 37 | - [ ] Write validation.json with complete results
 38 | - [ ] Display clear validation summary
 39 | - [ ] Block dependent sub-missions if validation fails
 40 | - [ ] Add unit and integration tests
 41 | 
 42 | ## Acceptance Criteria
 43 | - [ ] `--capture` correctly identifies changed files via git diff
 44 | - [ ] Scope validation works (allowed paths, forbidden paths)
 45 | - [ ] Test command executes and output is captured
 46 | - [ ] validation.todo.json contains all deterministic evidence
 47 | - [ ] `--commit` validates all metric fields are filled
 48 | - [ ] Baseline vs final comparison is accurate
 49 | - [ ] Target vs final comparison is accurate
 50 | - [ ] Pass/fail logic is correct
 51 | - [ ] validation.json contains complete evidence
 52 | - [ ] Terminal output clearly shows pass/fail status
 53 | - [ ] Integration tests cover various scenarios (pass, fail, scope violation)
 54 | 
 55 | ## Example validation.todo.json
 56 | ```json
 57 | {
 58 |   "sub_mission_id": "MF-001-A",
 59 |   "deterministic_evidence": {
 60 |     "files_changed": ["server/src/rest/MatchmakingEndpoint.java"],
 61 |     "scope_check": {
 62 |       "allowed_paths_satisfied": true,
 63 |       "forbidden_paths_violated": false,
 64 |       "violations": []
 65 |     },
 66 |     "test_results": {
 67 |       "command": "./gradlew test --tests '*MatchmakingEndpointTest*'",
 68 |       "exit_code": 0,
 69 |       "output": "...",
 70 |       "passed": true
 71 |     }
 72 |   },
 73 |   "metrics": [
 74 |     {
 75 |       "metric_id": "rest_endpoint_exists",
 76 |       "baseline_value": false,
 77 |       "target_value": true,
 78 |       "final_value": null
 79 |     }
 80 |   ]
 81 | }
 82 | ```
 83 | 
 84 | ## Example validation.json
 85 | ```json
 86 | {
 87 |   "sub_mission_id": "MF-001-A",
 88 |   "timestamp": "2026-05-16T17:00:00Z",
 89 |   "status": "PASSED",
 90 |   "deterministic_evidence": { ... },
 91 |   "metrics": [
 92 |     {
 93 |       "metric_id": "rest_endpoint_exists",
 94 |       "baseline_value": false,
 95 |       "target_value": true,
 96 |       "final_value": true,
 97 |       "status": "PASSED"
 98 |     }
 99 |   ]
100 | }
101 | ```
102 | 
103 | ## Technical Notes
104 | - Use git diff utilities from MF-003
105 | - Scope check must validate against both allowed and forbidden paths
106 | - Test execution should have timeout
107 | - validation.json status: PASSED, FAILED, BLOCKED
108 | - Clear distinction between deterministic evidence (CLI) and semantic metrics (Bob)
109 | 
110 | ## Estimated Effort
111 | **4-5 hours** (hackathon pace)
112 | 
113 | ## Developer Assignment
114 | Backend/CLI Developer (depends on MF-001, MF-002, MF-003, MF-008)
</content>
</file>
<file><path>issues/cli-foundation.md</path>
<content lines="1-49">
 1 | # MF-001: CLI Foundation and Project Setup
 2 | 
 3 | ## Priority
 4 | **MUST FINISH** - Required for project viability
 5 | 
 6 | ## Phase
 7 | Phase 1 - Core CLI Harness
 8 | 
 9 | ## Dependencies
10 | None (can start immediately)
11 | 
12 | ## Parallel Work
13 | Can be worked on independently from all other issues
14 | 
15 | ## Objective
16 | Create the basic CLI application structure and establish the local MissionForge workspace format.
17 | 
18 | ## Tasks
19 | - [ ] Set up Python 3.11+ project structure with proper package layout
20 | - [ ] Choose and configure CLI framework (Click or Typer)
21 | - [ ] Implement base `missionforge` command with help text
22 | - [ ] Add command grouping for logical organization
23 | - [ ] Define `.missionforge/` workspace directory structure
24 | - [ ] Implement workspace path resolution from repository root
25 | - [ ] Add basic error handling for:
26 |   - Missing workspace
27 |   - Invalid paths
28 |   - Invalid mission IDs
29 | - [ ] Add logging configuration
30 | - [ ] Set up project dependencies (PyYAML/ruamel.yaml, jsonschema, Jinja2)
31 | 
32 | ## Acceptance Criteria
33 | - [ ] Developer can run `missionforge --help` and see available commands
34 | - [ ] CLI displays clear help text with command descriptions
35 | - [ ] Workspace path resolution works from any subdirectory in repo
36 | - [ ] Error messages are clear and actionable
37 | - [ ] Project structure follows Python best practices
38 | 
39 | ## Technical Notes
40 | - Use Click or Typer for CLI framework
41 | - No GitPython dependency - use subprocess calls to system git
42 | - Keep CLI language-agnostic (never read source code)
43 | - All file operations should be relative to repo root
44 | 
45 | ## Estimated Effort
46 | 2-3 days
47 | 
48 | ## Developer Assignment
49 | Backend/CLI Developer
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:30:28.268Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.69

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<search_files>
<path>issues</path>
<regex>baseline|metric.*definition|MetricDefinition</regex>
<file_pattern>*.md</file_pattern>
</search_files>

---

**User:**

[search_files for 'baseline|metric.*definition|MetricDefinition' in '*.md'] Result:
Found 26 results.

# issues/watsonx-mission-chat.md
 30 |   - plan.yaml
 31 |   - baseline.json files
 32 |   - validation.json files
----

# issues/bob-skill-slash-commands.md
 27 |   - Plan dependency graph
 28 |   - Capture baseline
 29 |   - Implement changes
----
 44 | - [ ] Create `/mf-next` - Show next ready sub-mission
 45 | - [ ] Create `/mf-baseline` - Baseline capture/commit workflow
 46 | - [ ] Create `/mf-validate` - Validation capture/commit workflow
----
 68 | ```markdown
 69 | # /mf-baseline
 70 | 
 71 | Captures or commits baseline measurements for a sub-mission.
 72 | 
 73 | ## Usage
 74 | /mf-baseline <sub-mission-id> [--capture|--commit]
 75 | 
 76 | ## What it does
 77 | - `--capture`: Generates baseline.todo.json for Bob to fill
 78 | - `--commit`: Validates and commits baseline.json
 79 | 
 80 | ## Next steps
 81 | After capture: Read the scoped code and fill baseline.todo.json
 82 | After commit: Begin implementation of the sub-mission
----

# issues/README.md
 17 | 7. **next-command.md** (2h) - Depends on plan-command
 18 | 8. **baseline-flow.md** (3-4h) - Depends on schemas, parallel with plan/next
 19 | 9. **sub-mission-validation.md** (4-5h) - Depends on baseline + git-test-utilities
 20 | 10. **parent-validation.md** (3h) - Depends on sub-mission-validation
----
 42 | | **0–6h** | cli-foundation | schemas-validators (in parallel; finalize after A's foundation lands) + git-test-utilities + author 2-3 `.missionforge/` sample fixtures | Co-design API contract with Dev D; scaffold FastAPI project | Co-design API contract; Next.js scaffold + mock API server (MSW) + wireframes |
 43 | | **6–14h** | workspace-commands → decompose-command | baseline-flow (no longer waits for decompose) → start sub-mission-validation | board-backend against fixtures | board-frontend against mock API |
 44 | | **14–22h** | plan-command → next-command | sub-mission-validation → parent-validation → report-generation | cli-wrapper-endpoints, watsonx-mission-chat (if time) | mission-detail-panel + report-renderer; swap mock → real API |
----
 86 |   ↓
 87 | plan-command (3-4h) + baseline-flow (3-4h)
 88 |   ↓
----
110 | - ✅ CLI can plan dependency graph
111 | - ✅ CLI can track baseline and validation
112 | - ✅ CLI can generate evidence reports
----

# issues/demo-mission-prep.md
 35 | - [ ] Define aggregate_metrics:
 36 |   - CORBA references in matchmaking (baseline: N, target: 0)
 37 |   - In-game CORBA flow still works (baseline: true, target: true)
 38 | - [ ] Define parent test_command (integration tests)
----

# issues/schemas-validators.md
 15 | ## Objective
 16 | Define and implement YAML/JSON schemas for parent missions, sub-missions, baselines, and validation files with comprehensive validation logic.
 17 | 
----
 22 |   - `id`, `parent`, `title`, `goal`, `depends_on`, `allowed_paths`, `metrics`, `test_command`
 23 | - [ ] Define baseline JSON schema (baseline.todo.json and baseline.json)
 24 | - [ ] Define validation JSON schema (validation.todo.json and validation.json)
----

# issues/sub-mission-validation.md
 12 | - MF-003 (Git/Test Utilities) - needs git diff and test execution
 13 | - MF-008 (Baseline Flow) - needs baseline.json to compare against
 14 | 
----
 32 | - [ ] Validate Bob-filled metric values are complete
 33 | - [ ] Compare final values against baseline values
 34 | - [ ] Compare final values against target values
----
 75 |       "metric_id": "rest_endpoint_exists",
 76 |       "baseline_value": false,
 77 |       "target_value": true,
----
 93 |       "metric_id": "rest_endpoint_exists",
 94 |       "baseline_value": false,
 95 |       "target_value": true,
----

# issues/mission-detail-panel.md
 42 | - [ ] Display dependencies (what it depends on, what depends on it)
 43 | - [ ] Display metrics table (baseline → target → final)
 44 | - [ ] Display git diff (files changed by this sub-mission)
----

# issues/board-backend.md
  9 | ## Dependencies
 10 | - schemas-validators.md (locked schemas for parent mission, sub-mission, baseline, validation, plan)
 11 | - Sample `.missionforge/` fixtures (2-3 representative missions in varied states) — Dev B produces these as a side-output of schema work around hour ~6
----

# issues/parent-validation.md
 66 |       "metric_id": "corba_refs_in_matchmaking",
 67 |       "baseline_value": 7,
 68 |       "target_value": 0,
----

# issues/baseline-flow.md
 10 | - MF-001 (CLI Foundation)
 11 | - MF-002 (Schemas) - needs baseline + sub-mission schemas
 12 | 
----
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
----
 40 | ## Acceptance Criteria
 41 | - [ ] `--capture` generates correct baseline.todo.json structure
 42 | - [ ] baseline.todo.json is easy for Bob to fill
 43 | - [ ] Cannot capture if baseline already committed (without --force)
 44 | - [ ] `--commit` validates all fields are filled
 45 | - [ ] Type validation catches incorrect value types
 46 | - [ ] baseline.json is immutable after commit
 47 | - [ ] Timestamp is recorded in baseline.json
 48 | - [ ] Terminal output shows clear summary
----
 50 | 
 51 | ## Example baseline.todo.json
 52 | ```json
----
 58 |       "description": "A REST endpoint exists at /api/matchmaking",
 59 |       "baseline_target": false,
 60 |       "value": null
----
 65 | 
 66 | ## Example baseline.json
 67 | ```json
----
 75 |       "description": "A REST endpoint exists at /api/matchmaking",
 76 |       "baseline_target": false,
 77 |       "value": false
----
 83 | ## Technical Notes
 84 | - baseline.json should be immutable (add file permissions check)
 85 | - Validate metric values match expected types (bool, int, string)
----
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:30:31.943Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.81

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me check if there's a development roadmap file to understand the overall architecture better:

<list_files>
<path>.</path>
<recursive>false</recursive>
</list_files>

---

**User:**

[list_files for '.'] Result:
.coverage
.DS_Store
.gitignore
pyproject.toml
README.md
.claude/
.github/
bob_sessions/
docs/
src/
tests/
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:30:35.382Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$0.94

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
  <file>
    <path>README.md</path>
    <line_range>1-100</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'README.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>README.md</path>
<content lines="1-100">
  1 | # MissionForge CLI
  2 | 
  3 | AI-assisted mission decomposition and validation CLI tool for managing complex software development missions.
  4 | 
  5 | ## Installation
  6 | 
  7 | ### Requirements
  8 | - Python 3.11 or higher
  9 | - pip
 10 | 
 11 | ### Install from source
 12 | 
 13 | ```bash
 14 | # Clone the repository
 15 | git clone <repository-url>
 16 | cd Mission-Forge
 17 | 
 18 | # Install in development mode with all dependencies
 19 | pip install -e ".[dev]"
 20 | ```
 21 | 
 22 | ## Quick Start
 23 | 
 24 | ### 1. Initialize a Mission Workspace
 25 | 
 26 | ```bash
 27 | # Create a new mission
 28 | missionforge workspace init MF-001
 29 | 
 30 | # This creates:
 31 | # .missionforge/
 32 | # └── missions/
 33 | #     └── MF-001/
 34 | #         ├── mission.yaml      # Mission definition
 35 | #         ├── plan.yaml         # Execution plan
 36 | #         ├── report.md         # Generated report
 37 | #         └── sub-missions/     # Sub-mission directory
 38 | ```
 39 | 
 40 | ### 2. Check Workspace Status
 41 | 
 42 | ```bash
 43 | missionforge workspace status
 44 | ```
 45 | 
 46 | This displays a table of all missions with their status and sub-mission count.
 47 | 
 48 | ### 3. View Help
 49 | 
 50 | ```bash
 51 | # General help
 52 | missionforge --help
 53 | 
 54 | # Command-specific help
 55 | missionforge workspace --help
 56 | missionforge workspace init --help
 57 | ```
 58 | 
 59 | ## CLI Commands
 60 | 
 61 | ### Global Options
 62 | 
 63 | - `--verbose, -v`: Enable verbose output (DEBUG level logging)
 64 | - `--log-file PATH`: Write logs to specified file
 65 | 
 66 | ### Workspace Commands
 67 | 
 68 | #### `missionforge workspace init <MISSION_ID>`
 69 | 
 70 | Initialize a new mission workspace.
 71 | 
 72 | **Arguments:**
 73 | - `MISSION_ID`: Mission identifier (format: `[A-Z]{2,4}-\d{3}[A-Z]?`, e.g., `MF-001`, `PROJ-042A`)
 74 | 
 75 | **Options:**
 76 | - `--force`: Overwrite existing mission
 77 | 
 78 | **Example:**
 79 | ```bash
 80 | missionforge workspace init MF-001
 81 | missionforge workspace init PROJ-123 --force
 82 | ```
 83 | 
 84 | #### `missionforge workspace status`
 85 | 
 86 | Show workspace status and list all missions.
 87 | 
 88 | **Example:**
 89 | ```bash
 90 | missionforge workspace status
 91 | ```
 92 | 
 93 | ### Version Command
 94 | 
 95 | #### `missionforge version`
 96 | 
 97 | Display version information.
 98 | 
 99 | ## Project Structure
100 | 
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:30:38.645Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Pending |
| 2 | Design baseline.todo.json and baseline.json data structures based on sub-mission metrics | Pending |
| 3 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 4 | Implement baseline capture functionality (--capture flag) | Pending |
| 5 | Implement baseline commit functionality (--commit flag) | Pending |
| 6 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 7 | Create baseline service layer for business logic | Pending |
| 8 | Implement metric type validation (bool, int, string, float) | Pending |
| 9 | Add file immutability checks for baseline.json | Pending |
| 10 | Implement --reset flag for re-capture scenarios | Pending |
| 11 | Create comprehensive unit tests for baseline operations | Pending |
| 12 | Create integration tests for capture → fill → commit workflow | Pending |
| 13 | Add baseline command to CLI app registration | Pending |
| 14 | Update workspace.py with baseline path helpers | Pending |
| 15 | Document baseline command usage and examples | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! Now I have the full context. Let me create a comprehensive implementation plan based on my analysis:

## Key Findings from Context Review:

1. **Two Different Baseline Concepts Exist:**
   - **Existing codebase**: Git-based metrics (files_changed, lines_added, test_coverage) - used for general tracking
   - **Issue #8 specification**: Metric-based validation (custom metrics from sub-mission.yaml with baseline_target values) - used for Bob's semantic validation

2. **Architecture Clarity:**
   - The issue spec's baseline is for **sub-mission custom metrics** defined in `sub-mission.yaml`
   - These metrics are semantic (e.g., "REST endpoint exists") not git-based
   - Bob fills these values by analyzing code
   - This is separate from the git diff metrics in existing schemas

3. **Validation Flow (from sub-mission-validation.md):**
   - Baseline captures initial state of custom metrics
   - Validation compares: `baseline_value` → `target_value` → `final_value`
   - This confirms the issue spec structure is correct

Now I'll create the detailed implementation plan:

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[-] Create comprehensive implementation plan document
[ ] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[ ] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[ ] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[ ] Update JSON schemas for baseline.todo.json and baseline.json validation
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json
[ ] Implement baseline commit: validate filled values and write immutable baseline.json
[ ] Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.)
[ ] Create baseline service layer at src/missionforge/core/baseline_service.py
[ ] Implement metric type inference and validation (bool, int, float, string)
[ ] Add file immutability checks using file permissions
[ ] Implement --reset flag to allow re-capture with safety checks
[ ] Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path)
[ ] Create unit tests for baseline models and validation
[ ] Create unit tests for baseline service operations
[ ] Create integration tests for full capture → fill → commit workflow
[ ] Register baseline command in CLI app.py
[ ] Update README.md with baseline command documentation
[ ] Create example fixtures for testing
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
issues/baseline-flow.md

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:31:54.398Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.21

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | In Progress |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Pending |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Pending |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Pending |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Pending |
| 8 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 9 | Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json | Pending |
| 10 | Implement baseline commit: validate filled values and write immutable baseline.json | Pending |
| 11 | Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.) | Pending |
| 12 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 13 | Implement metric type inference and validation (bool, int, float, string) | Pending |
| 14 | Add file immutability checks using file permissions | Pending |
| 15 | Implement --reset flag to allow re-capture with safety checks | Pending |
| 16 | Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path) | Pending |
| 17 | Create unit tests for baseline models and validation | Pending |
| 18 | Create unit tests for baseline service operations | Pending |
| 19 | Create integration tests for full capture → fill → commit workflow | Pending |
| 20 | Register baseline command in CLI app.py | Pending |
| 21 | Update README.md with baseline command documentation | Pending |
| 22 | Create example fixtures for testing | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me create a comprehensive implementation plan document:

<write_to_file>
<path>issues/MF-008-implementation-plan.md</path>
<content>
# MF-008: Baseline Capture and Commit Flow - Implementation Plan

## Executive Summary

This document provides a detailed implementation plan for MF-008, which implements the baseline measurement workflow for sub-missions. After analyzing the codebase and issue specifications, I've identified that this feature requires **new data models** separate from the existing git-based baseline schemas.

## Architecture Analysis

### Two Baseline Concepts

The codebase currently has two distinct baseline concepts:

1. **Git-based Baseline** (existing in `models/schemas.py`):
   - Tracks: `files_changed`, `lines_added`, `lines_removed`, `test_coverage`
   - Purpose: General code change metrics
   - Used for: Overall mission tracking

2. **Sub-Mission Metric Baseline** (required by issue #8):
   - Tracks: Custom semantic metrics from `sub-mission.yaml`
   - Purpose: Bob-filled validation of specific goals
   - Used for: Sub-mission pass/fail determination
   - Example: "REST endpoint exists" (bool), "CORBA references" (int)

### Key Insight

The issue specification is correct - we need **new models** for sub-mission metric baselines. These are fundamentally different from git metrics:

- **Git metrics**: Deterministic, CLI-captured (files changed, lines added)
- **Metric baselines**: Semantic, Bob-filled (endpoint exists, feature works)

## Data Structure Design

### baseline.todo.json (Bob fills this)

```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "A REST endpoint exists at /api/matchmaking",
      "baseline_target": false,
      "value": null
    },
    {
      "metric_id": "corba_references_count",
      "description": "Number of CORBA references in matchmaking code",
      "baseline_target": 7,
      "value": null
    }
  ]
}
```

### baseline.json (Immutable after commit)

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
    },
    {
      "metric_id": "corba_references_count",
      "description": "Number of CORBA references in matchmaking code",
      "baseline_target": 7,
      "value": 7
    }
  ]
}
```

## Implementation Plan

### Phase 1: Data Models (1 hour)

#### 1.1 Create New Pydantic Models in `models/schemas.py`

```python
class SubMissionBaselineMetric(BaseModel):
    """A single metric in a sub-mission baseline."""
    metric_id: str
    description: str
    baseline_target: bool | int | float | str
    value: bool | int | float | str | None = None

class SubMissionBaseline(BaseModel):
    """Baseline for sub-mission custom metrics."""
    sub_mission_id: str
    timestamp: str | None = None
    status: str | None = None  # "captured", "committed"
    metrics: list[SubMissionBaselineMetric]
```

#### 1.2 Update JSON Schemas in `schemas/json_schemas.py`

Add new schemas:
- `SUB_MISSION_BASELINE_TODO_SCHEMA`
- `SUB_MISSION_BASELINE_SCHEMA`

### Phase 2: Core Service Layer (1.5 hours)

#### 2.1 Create `core/baseline_service.py`

```python
class BaselineService:
    """Service for baseline capture and commit operations."""
    
    def capture_baseline(
        self, 
        sub_mission_id: str,
        force: bool = False
    ) -> Path:
        """Generate baseline.todo.json from sub-mission.yaml metrics."""
        
    def commit_baseline(
        self, 
        sub_mission_id: str
    ) -> Path:
        """Validate and commit baseline.json from baseline.todo.json."""
        
    def reset_baseline(
        self, 
        sub_mission_id: str
    ) -> None:
        """Remove baseline files to allow re-capture."""
```

**Key Operations:**

1. **Capture**:
   - Read `sub-mission.yaml`
   - Extract `metrics` dictionary
   - For each metric, create entry with `baseline_target` from metric definition
   - Set `value: null` for Bob to fill
   - Write `baseline.todo.json`
   - Prevent if `baseline.json` exists (unless `--force`)

2. **Commit**:
   - Read `baseline.todo.json`
   - Validate all `value` fields are filled (not null)
   - Validate types match `baseline_target` types
   - Add `timestamp` and `status: "committed"`
   - Write `baseline.json`
   - Make file read-only (chmod 444)

3. **Reset**:
   - Remove both `baseline.todo.json` and `baseline.json`
   - Require confirmation or `--force` flag

### Phase 3: CLI Commands (1 hour)

#### 3.1 Create `cli/commands/baseline.py`

```python
@app.command("capture")
def capture_baseline(
    sub_mission_id: str,
    force: bool = False
) -> None:
    """Capture baseline metrics for a sub-mission."""

@app.command("commit")
def commit_baseline(
    sub_mission_id: str
) -> None:
    """Commit baseline after Bob fills values."""

@app.command("reset")
def reset_baseline(
    sub_mission_id: str,
    force: bool = False
) -> None:
    """Reset baseline to allow re-capture."""
```

#### 3.2 Register in `cli/app.py`

```python
from .commands import baseline
app.add_typer(baseline.app, name="baseline")
```

### Phase 4: Supporting Infrastructure (30 minutes)

#### 4.1 Add Exceptions to `core/exceptions.py`

```python
class BaselineAlreadyExistsError(MissionForgeError):
    """Raised when baseline already committed."""

class BaselineNotCapturedError(MissionForgeError):
    """Raised when trying to commit without capture."""

class BaselineValidationError(MissionForgeError):
    """Raised when baseline validation fails."""

class BaselineIncompleteError(MissionForgeError):
    """Raised when baseline has unfilled values."""
```

#### 4.2 Update `core/workspace.py`

```python
def baseline_todo_path(self, sub_mission_id: str) -> Path:
    """Get path to baseline.todo.json."""
    return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.todo.json"

def baseline_path(self, sub_mission_id: str) -> Path:
    """Get path to baseline.json."""
    return self.sub_mission_path(parent_id, sub_mission_id) / "baseline.json"
```

### Phase 5: Testing (1 hour)

#### 5.1 Unit Tests

- `tests/unit/test_baseline_models.py`: Test Pydantic models
- `tests/unit/test_baseline_service.py`: Test service operations
- `tests/unit/commands/test_baseline.py`: Test CLI commands

#### 5.2 Integration Tests

- `tests/integration/test_baseline_flow.py`: Test full workflow
  - Capture → Fill → Commit
  - Error cases (already exists, incomplete, etc.)
  - Reset functionality

#### 5.3 Test Fixtures

Create in `tests/fixtures/`:
- `sub-mission-with-metrics.yaml`
- `baseline.todo.json` (filled and unfilled versions)
- `baseline.json` (committed version)

## Type Inference Strategy

The baseline system needs to infer metric types from `baseline_target` values:

```python
def infer_metric_type(baseline_target: Any) -> type:
    """Infer expected type from baseline_target value."""
    if isinstance(baseline_target, bool):
        return bool
    elif isinstance(baseline_target, int):
        return int
    elif isinstance(baseline_target, float):
        return float
    else:
        return str
```

When validating `value` during commit:
1. Get type from `baseline_target`
2. Ensure `value` matches that type
3. Reject if types don't match

## File Immutability Implementation

```python
import os
import stat

def make_readonly(file_path: Path) -> None:
    """Make file read-only."""
    os.chmod(file_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

def is_readonly(file_path: Path) -> bool:
    """Check if file is read-only."""
    return not os.access(file_path, os.W_OK)
```

## Error Handling Strategy

### Capture Errors

1. **Sub-mission not found**: Clear message with path
2. **No metrics defined**: Suggest adding metrics to sub-mission.yaml
3. **Baseline already exists**: Show path, suggest `--force` or `reset`

### Commit Errors

1. **baseline.todo.json not found**: Suggest running `capture` first
2. **Incomplete values**: List which metrics need values
3. **Type mismatch**: Show expected vs actual type
4. **baseline.json already exists**: Cannot overwrite committed baseline

### Reset Errors

1. **No baseline files**: Nothing to reset
2. **Confirmation required**: Require `--force` flag

## Terminal Output Design

### Capture Success

```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • matchmaking_latency_ms (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

### Commit Success

```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
│ matchmaking_latency_ms  │ 150.0    │ 145.2 │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

## Integration with Validation Flow

The baseline.json will be consumed by MF-009 (Sub-Mission Validation):

```json
// validation.todo.json uses baseline values
{
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "baseline_value": false,  // from baseline.json
      "target_value": true,     // from sub-mission.yaml
      "final_value": null       // Bob fills after implementation
    }
  ]
}
```

## Dependencies and Blockers

### Dependencies (Must Complete First)
- ✅ MF-001: CLI Foundation (complete)
- ✅ MF-002: Schemas (complete - but needs extension)

### Blocks (Waiting on This)
- MF-009: Sub-Mission Validation (needs baseline.json)

### Parallel Work (Can Work Simultaneously)
- MF-006: Workspace Commands
- MF-007: Decompose Command
- MF-010: Plan Command
- MF-011: Next Command

## Time Estimates (Hackathon Pace)

| Phase | Task | Time |
|-------|------|------|
| 1 | Data Models | 1h |
| 2 | Core Service | 1.5h |
| 3 | CLI Commands | 1h |
| 4 | Infrastructure | 0.5h |
| 5 | Testing | 1h |
| **Total** | | **5h** |

With buffer: **3-4 hours** as specified in issue

## Success Criteria Checklist

- [ ] `missionforge baseline capture <id>` generates baseline.todo.json
- [ ] baseline.todo.json structure matches specification
- [ ] Bob can easily fill metric values
- [ ] `missionforge baseline commit <id>` validates and commits
- [ ] Type validation catches mismatches
- [ ] baseline.json is immutable after commit
- [ ] `--reset` flag allows re-capture
- [ ] Clear terminal output at each step
- [ ] Comprehensive test coverage
- [ ] Integration with validation flow works

## Risk Mitigation

### Risk: Type inference ambiguity
**Mitigation**: Use explicit type from baseline_target, document in sub-mission.yaml

### Risk: File permission issues on Windows
**Mitigation**: Graceful fallback, warn if cannot make read-only

### Risk: Incomplete baseline.todo.json
**Mitigation**: Clear validation errors listing missing fields

### Risk: Confusion with git-based Baseline
**Mitigation**: Clear naming (SubMissionBaseline), separate files, documentation

## Next Steps

1. Review this plan with team
2. Confirm data structure design
3. Begin Phase 1 implementation
4. Create test fixtures early
5. Iterate based on testing feedback

## Questions for Review

1. Should we support metric value ranges (min/max) in baseline?
2. Should baseline.json include git commit hash for traceability?
3. Should we validate metric_id matches sub-mission.yaml keys?
4. Should reset require explicit confirmation prompt?

---

**Document Status**: Draft for Review  
**Created**: 2026-05-17  
**Author**: Bob (Planning Mode)  
**Issue**: MF-008
</content>
<line_count>449</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'issues/MF-008-implementation-plan.md'] Result:
<file_write_result>
<path>issues/MF-008-implementation-plan.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
issues/MF-008-implementation-plan.md

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:32:52.055Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.35

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | In Progress |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Pending |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Pending |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Pending |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Pending |
| 8 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 9 | Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json | Pending |
| 10 | Implement baseline commit: validate filled values and write immutable baseline.json | Pending |
| 11 | Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.) | Pending |
| 12 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 13 | Implement metric type inference and validation (bool, int, float, string) | Pending |
| 14 | Add file immutability checks using file permissions | Pending |
| 15 | Implement --reset flag to allow re-capture with safety checks | Pending |
| 16 | Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path) | Pending |
| 17 | Create unit tests for baseline models and validation | Pending |
| 18 | Create unit tests for baseline service operations | Pending |
| 19 | Create integration tests for full capture → fill → commit workflow | Pending |
| 20 | Register baseline command in CLI app.py | Pending |
| 21 | Update README.md with baseline command documentation | Pending |
| 22 | Create example fixtures for testing | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[x] Create comprehensive implementation plan document
[ ] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[ ] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[ ] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[ ] Update JSON schemas for baseline.todo.json and baseline.json validation
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json
[ ] Implement baseline commit: validate filled values and write immutable baseline.json
[ ] Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.)
[ ] Create baseline service layer at src/missionforge/core/baseline_service.py
[ ] Implement metric type inference and validation (bool, int, float, string)
[ ] Add file immutability checks using file permissions
[ ] Implement --reset flag to allow re-capture with safety checks
[ ] Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path)
[ ] Create unit tests for baseline models and validation
[ ] Create unit tests for baseline service operations
[ ] Create integration tests for full capture → fill → commit workflow
[ ] Register baseline command in CLI app.py
[ ] Update README.md with baseline command documentation
[ ] Create example fixtures for testing
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
Current time in ISO 8601 UTC format: 2026-05-17T06:36:37.148Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.51

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>plan</slug>
<name>📝 Plan</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Pending |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Pending |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Pending |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Pending |
| 8 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 9 | Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json | Pending |
| 10 | Implement baseline commit: validate filled values and write immutable baseline.json | Pending |
| 11 | Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.) | Pending |
| 12 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 13 | Implement metric type inference and validation (bool, int, float, string) | Pending |
| 14 | Add file immutability checks using file permissions | Pending |
| 15 | Implement --reset flag to allow re-capture with safety checks | Pending |
| 16 | Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path) | Pending |
| 17 | Create unit tests for baseline models and validation | Pending |
| 18 | Create unit tests for baseline service operations | Pending |
| 19 | Create integration tests for full capture → fill → commit workflow | Pending |
| 20 | Register baseline command in CLI app.py | Pending |
| 21 | Update README.md with baseline command documentation | Pending |
| 22 | Create example fixtures for testing | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Created comprehensive implementation plan for MF-008: Baseline Capture and Commit Flow

**Key Findings:**
- Identified two distinct baseline concepts in the codebase (git-based vs metric-based)
- Confirmed issue specification requires NEW data models for sub-mission metric baselines
- These are separate from existing git-based baseline schemas

**Deliverable:**
Created detailed implementation plan at [`issues/MF-008-implementation-plan.md`](issues/MF-008-implementation-plan.md) including:

**Architecture Analysis:**
- Two baseline concepts: git-based (existing) vs sub-mission metrics (new)
- Sub-mission metrics are semantic (Bob-filled) not deterministic (CLI-captured)
- Clear separation of concerns between git tracking and goal validation

**Implementation Phases:**
1. Data Models (1h) - New Pydantic models for SubMissionBaseline
2. Core Service (1.5h) - BaselineService with capture/commit/reset operations
3. CLI Commands (1h) - baseline capture/commit/reset commands
4. Infrastructure (0.5h) - Exceptions, workspace helpers, file immutability
5. Testing (1h) - Unit and integration tests

**Data Structures:**
- baseline.todo.json: Bob fills metric values
- baseline.json: Immutable committed baseline with timestamp

**Key Features:**
- Type inference from baseline_target values
- File immutability using permissions
- Clear error handling and terminal output
- Integration with validation flow (MF-009)

**Total Estimate:** 3-4 hours (matches issue specification)

Ready for team review and implementation in Code mode.
</result>
</attempt_completion>

---

**User:**



New instructions for task continuation:
<user_message>
implement 'issues/MF-008-implementation-plan.md' (see below for file content)
</user_message>

<file_content path="issues/MF-008-implementation-plan.md">
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

</file_content>
<environment_details>
# VSCode Visible Files
issues/MF-008-implementation-plan.md

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:38:46.820Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.66

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>


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
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Pending |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Pending |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Pending |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Pending |
| 8 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 9 | Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json | Pending |
| 10 | Implement baseline commit: validate filled values and write immutable baseline.json | Pending |
| 11 | Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.) | Pending |
| 12 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 13 | Implement metric type inference and validation (bool, int, float, string) | Pending |
| 14 | Add file immutability checks using file permissions | Pending |
| 15 | Implement --reset flag to allow re-capture with safety checks | Pending |
| 16 | Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path) | Pending |
| 17 | Create unit tests for baseline models and validation | Pending |
| 18 | Create unit tests for baseline service operations | Pending |
| 19 | Create integration tests for full capture → fill → commit workflow | Pending |
| 20 | Register baseline command in CLI app.py | Pending |
| 21 | Update README.md with baseline command documentation | Pending |
| 22 | Create example fixtures for testing | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I'll implement the MF-008 baseline flow by breaking it down into logical subtasks and delegating them to Code mode. Let me start by creating the foundational components.

<new_task>
<mode>code</mode>
<message>
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
</message>
</new_task>

---

**User:**

[new_task completed] Result: Phase 1 of MF-008 implementation is complete. I have successfully added the data models and JSON schemas for the baseline capture and commit flow.

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

---

**User:**

[new_task in 💻 Code mode: 'Implement Phase 1 of MF-008: Data Models and Schemas

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

When complete, use `attempt_completion` with a summary of what was added.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 1 of MF-008: Data Models and Schemas

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

When complete, use `attempt_completion` with a summary of what was added. and 0 todo items
[new_task in 💻 Code mode: 'Implement Phase 1 of MF-008: Data Models and Schemas

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

When complete, use `attempt_completion` with a summary of what was added.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 1 of MF-008: Data Models and Schemas

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

When complete, use `attempt_completion` with a summary of what was added. and 0 todo items
<environment_details>
# VSCode Visible Files
src/missionforge/schemas/json_schemas.py

# VSCode Open Tabs
issues/baseline-flow.md,issues/MF-008-implementation-plan.md,src/missionforge/models/schemas.py,src/missionforge/schemas/json_schemas.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:40:26.948Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.82

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Pending |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Pending |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Pending |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Pending |
| 8 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 9 | Implement baseline capture: read sub-mission.yaml metrics and generate baseline.todo.json | Pending |
| 10 | Implement baseline commit: validate filled values and write immutable baseline.json | Pending |
| 11 | Add baseline-specific exceptions (BaselineAlreadyExistsError, BaselineNotCapturedError, etc.) | Pending |
| 12 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 13 | Implement metric type inference and validation (bool, int, float, string) | Pending |
| 14 | Add file immutability checks using file permissions | Pending |
| 15 | Implement --reset flag to allow re-capture with safety checks | Pending |
| 16 | Add baseline path helpers to workspace.py (baseline_todo_path, baseline_path) | Pending |
| 17 | Create unit tests for baseline models and validation | Pending |
| 18 | Create unit tests for baseline service operations | Pending |
| 19 | Create integration tests for full capture → fill → commit workflow | Pending |
| 20 | Register baseline command in CLI app.py | Pending |
| 21 | Update README.md with baseline command documentation | Pending |
| 22 | Create example fixtures for testing | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Excellent! Phase 1 is complete. Let me update the todo list and proceed with Phase 2.

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[x] Create comprehensive implementation plan document
[x] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[x] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[x] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[x] Update JSON schemas for baseline.todo.json and baseline.json validation
[ ] Add baseline-specific exceptions to core/exceptions.py
[ ] Add baseline path helpers to workspace.py
[ ] Create baseline service layer at src/missionforge/core/baseline_service.py
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Register baseline command in CLI app.py
[ ] Create unit tests for baseline models and validation
[ ] Create unit tests for baseline service operations
[ ] Create integration tests for full capture → fill → commit workflow
[ ] Create example fixtures for testing
[ ] Update README.md with baseline command documentation
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
Current time in ISO 8601 UTC format: 2026-05-17T06:40:32.946Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$1.99

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 9 | Add baseline path helpers to workspace.py | Pending |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 12 | Register baseline command in CLI app.py | Pending |
| 13 | Create unit tests for baseline models and validation | Pending |
| 14 | Create unit tests for baseline service operations | Pending |
| 15 | Create integration tests for full capture → fill → commit workflow | Pending |
| 16 | Create example fixtures for testing | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me proceed with Phase 4 (infrastructure) before Phase 2, as the service layer will need these components.

<new_task>
<mode>code</mode>
<message>
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
</message>
</new_task>

---

**User:**

[new_task completed] Result: Phase 4 of MF-008 (Supporting Infrastructure) has been successfully implemented:

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

---

**User:**

[new_task in 💻 Code mode: 'Implement Phase 4 of MF-008: Supporting Infrastructure

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

When complete, use `attempt_completion` with a summary of what was added.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 4 of MF-008: Supporting Infrastructure

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

When complete, use `attempt_completion` with a summary of what was added. and 0 todo items
[new_task in 💻 Code mode: 'Implement Phase 4 of MF-008: Supporting Infrastructure

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

When complete, use `attempt_completion` with a summary of what was added.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 4 of MF-008: Supporting Infrastructure

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

When complete, use `attempt_completion` with a summary of what was added. and 0 todo items
<environment_details>
# VSCode Visible Files
src/missionforge/core/workspace.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:41:20.422Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$2.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Pending |
| 9 | Add baseline path helpers to workspace.py | Pending |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 12 | Register baseline command in CLI app.py | Pending |
| 13 | Create unit tests for baseline models and validation | Pending |
| 14 | Create unit tests for baseline service operations | Pending |
| 15 | Create integration tests for full capture → fill → commit workflow | Pending |
| 16 | Create example fixtures for testing | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! Let me update the todo list and proceed with Phase 2 (Core Service Layer).

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[x] Create comprehensive implementation plan document
[x] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[x] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[x] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[x] Update JSON schemas for baseline.todo.json and baseline.json validation
[x] Add baseline-specific exceptions to core/exceptions.py
[x] Add baseline path helpers to workspace.py
[ ] Create baseline service layer at src/missionforge/core/baseline_service.py
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Register baseline command in CLI app.py
[ ] Create unit tests for baseline models and validation
[ ] Create unit tests for baseline service operations
[ ] Create integration tests for full capture → fill → commit workflow
[ ] Create example fixtures for testing
[ ] Update README.md with baseline command documentation
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
src/missionforge/core/workspace.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:41:30.502Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$2.35

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 12 | Register baseline command in CLI app.py | Pending |
| 13 | Create unit tests for baseline models and validation | Pending |
| 14 | Create unit tests for baseline service operations | Pending |
| 15 | Create integration tests for full capture → fill → commit workflow | Pending |
| 16 | Create example fixtures for testing | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let's implement Phase 2: Core Service Layer.

<new_task>
<mode>code</mode>
<message>
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
</message>
</new_task>

---

**User:**

[new_task completed] Result: Successfully implemented Phase 2 of MF-008: Core Service Layer

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

---

**User:**

[new_task in 💻 Code mode: 'Implement Phase 2 of MF-008: Core Service Layer

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

When complete, use `attempt_completion` with a summary of the implementation.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 2 of MF-008: Core Service Layer

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

When complete, use `attempt_completion` with a summary of the implementation. and 0 todo items
[new_task in 💻 Code mode: 'Implement Phase 2 of MF-008: Core Service Layer

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

When complete, use `attempt_completion` with a summary of the implementation.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 2 of MF-008: Core Service Layer

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

When complete, use `attempt_completion` with a summary of the implementation. and 0 todo items
<environment_details>
# VSCode Visible Files
src/missionforge/core/baseline_service.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:42:47.243Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$2.54

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Pending |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 12 | Register baseline command in CLI app.py | Pending |
| 13 | Create unit tests for baseline models and validation | Pending |
| 14 | Create unit tests for baseline service operations | Pending |
| 15 | Create integration tests for full capture → fill → commit workflow | Pending |
| 16 | Create example fixtures for testing | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Excellent! Let me update the todo list and proceed with Phase 3: CLI Commands.

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[x] Create comprehensive implementation plan document
[x] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[x] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[x] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[x] Update JSON schemas for baseline.todo.json and baseline.json validation
[x] Add baseline-specific exceptions to core/exceptions.py
[x] Add baseline path helpers to workspace.py
[x] Create baseline service layer at src/missionforge/core/baseline_service.py
[ ] Create baseline command module at src/missionforge/cli/commands/baseline.py
[ ] Register baseline command in CLI app.py
[ ] Create unit tests for baseline models and validation
[ ] Create unit tests for baseline service operations
[ ] Create integration tests for full capture → fill → commit workflow
[ ] Create example fixtures for testing
[ ] Update README.md with baseline command documentation
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
src/missionforge/core/baseline_service.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/cli/app.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:42:52.813Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$2.74

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Completed |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 12 | Register baseline command in CLI app.py | Pending |
| 13 | Create unit tests for baseline models and validation | Pending |
| 14 | Create unit tests for baseline service operations | Pending |
| 15 | Create integration tests for full capture → fill → commit workflow | Pending |
| 16 | Create example fixtures for testing | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let's implement Phase 3: CLI Commands and register them.

<new_task>
<mode>code</mode>
<message>
Implement Phase 3 of MF-008: CLI Commands

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. The core service layer is complete. Now we need to create the CLI commands that users will interact with.

**Your Task:**
1. Create a new file `src/missionforge/cli/commands/baseline.py` with three commands
2. Register the baseline command group in `src/missionforge/cli/app.py`

**CLI Commands to Implement:**

```python
"""Baseline management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ...core.baseline_service import BaselineService
from ...core.exceptions import MissionForgeError

app = typer.Typer(help="Baseline capture and commit commands")
console = Console()
```

**1. capture command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().capture_baseline()
- Display success message with:
  - Generated file path
  - List of metrics to fill (metric_id and type)
  - Next steps instructions
- Handle MissionForgeError and display formatted error

**2. commit command:**
- Arguments: `sub_mission_id: str`
- Call BaselineService().commit_baseline()
- Display success message with:
  - Committed file path
  - Table showing metrics (metric_id, baseline_target, value)
  - Warning that baseline.json is now immutable
- Handle MissionForgeError and display formatted error

**3. reset command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().reset_baseline()
- Display success message
- Handle MissionForgeError and display formatted error

**Terminal Output Format (from implementation plan):**

Capture success:
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • matchmaking_latency_ms (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

Commit success with table:
```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

**Registration in app.py:**
Add after the workspace command registration:
```python
from .commands import baseline
app.add_typer(baseline.app, name="baseline")
```

**Requirements:**
- Follow existing command patterns from workspace.py
- Use rich Console for output
- Use rich Table for commit summary
- Handle all MissionForgeError exceptions
- Display errors using console.print with red styling
- Read baseline.json to display metrics in commit command

**Scope:**
- Create NEW file `src/missionforge/cli/commands/baseline.py`
- Modify `src/missionforge/cli/app.py` to register baseline commands
- Follow existing code style from workspace.py

When complete, use `attempt_completion` with a summary of the implementation.
</message>
</new_task>

---

**User:**

[new_task completed] Result: Successfully implemented Phase 3 of MF-008: CLI Commands for baseline management.

## Implementation Summary

### 1. Created `src/missionforge/cli/commands/baseline.py`
Implemented three CLI commands following the existing patterns from workspace.py:

**capture command:**
- Takes `sub_mission_id` argument and optional `--force` flag
- Calls `BaselineService().capture_baseline()`
- Displays success message with:
  - Generated file path
  - List of metrics with their types (bool, int, float)
  - Next steps instructions
- Handles MissionForgeError with formatted error output

**commit command:**
- Takes `sub_mission_id` argument
- Calls `BaselineService().commit_baseline()`
- Displays success message with:
  - Committed file path
  - Rich Table showing metrics (metric_id, baseline_target, value)
  - Warning that baseline.json is now immutable
- Handles MissionForgeError with formatted error output

**reset command:**
- Takes `sub_mission_id` argument and optional `--force` flag
- Calls `BaselineService().reset_baseline()`
- Displays success message with list of removed files
- Handles MissionForgeError with formatted error output

### 2. Registered baseline commands in `src/missionforge/cli/app.py`
- Added import: `from .commands import baseline, workspace`
- Registered command group: `app.add_typer(baseline.app, name="baseline")`

### 3. Verification
All commands are working correctly:
- `missionforge baseline --help` shows all three commands
- `missionforge baseline capture --help` shows proper arguments and options
- `missionforge baseline commit --help` shows proper arguments
- `missionforge baseline reset --help` shows proper arguments and options
- Main CLI (`missionforge --help`) shows baseline command group

### Key Features
- Follows existing code style from workspace.py
- Uses rich Console for colored output
- Uses rich Table for commit summary display
- Proper error handling with MissionForgeError
- Reads baseline files to display metrics information
- Consistent with terminal output format from implementation plan

---

**User:**

[new_task in 💻 Code mode: 'Implement Phase 3 of MF-008: CLI Commands

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. The core service layer is complete. Now we need to create the CLI commands that users will interact with.

**Your Task:**
1. Create a new file `src/missionforge/cli/commands/baseline.py` with three commands
2. Register the baseline command group in `src/missionforge/cli/app.py`

**CLI Commands to Implement:**

```python
"""Baseline management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ...core.baseline_service import BaselineService
from ...core.exceptions import MissionForgeError

app = typer.Typer(help="Baseline capture and commit commands")
console = Console()
```

**1. capture command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().capture_baseline()
- Display success message with:
  - Generated file path
  - List of metrics to fill (metric_id and type)
  - Next steps instructions
- Handle MissionForgeError and display formatted error

**2. commit command:**
- Arguments: `sub_mission_id: str`
- Call BaselineService().commit_baseline()
- Display success message with:
  - Committed file path
  - Table showing metrics (metric_id, baseline_target, value)
  - Warning that baseline.json is now immutable
- Handle MissionForgeError and display formatted error

**3. reset command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().reset_baseline()
- Display success message
- Handle MissionForgeError and display formatted error

**Terminal Output Format (from implementation plan):**

Capture success:
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • matchmaking_latency_ms (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

Commit success with table:
```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

**Registration in app.py:**
Add after the workspace command registration:
```python
from .commands import baseline
app.add_typer(baseline.app, name="baseline")
```

**Requirements:**
- Follow existing command patterns from workspace.py
- Use rich Console for output
- Use rich Table for commit summary
- Handle all MissionForgeError exceptions
- Display errors using console.print with red styling
- Read baseline.json to display metrics in commit command

**Scope:**
- Create NEW file `src/missionforge/cli/commands/baseline.py`
- Modify `src/missionforge/cli/app.py` to register baseline commands
- Follow existing code style from workspace.py

When complete, use `attempt_completion` with a summary of the implementation.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 3 of MF-008: CLI Commands

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. The core service layer is complete. Now we need to create the CLI commands that users will interact with.

**Your Task:**
1. Create a new file `src/missionforge/cli/commands/baseline.py` with three commands
2. Register the baseline command group in `src/missionforge/cli/app.py`

**CLI Commands to Implement:**

```python
"""Baseline management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ...core.baseline_service import BaselineService
from ...core.exceptions import MissionForgeError

app = typer.Typer(help="Baseline capture and commit commands")
console = Console()
```

**1. capture command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().capture_baseline()
- Display success message with:
  - Generated file path
  - List of metrics to fill (metric_id and type)
  - Next steps instructions
- Handle MissionForgeError and display formatted error

**2. commit command:**
- Arguments: `sub_mission_id: str`
- Call BaselineService().commit_baseline()
- Display success message with:
  - Committed file path
  - Table showing metrics (metric_id, baseline_target, value)
  - Warning that baseline.json is now immutable
- Handle MissionForgeError and display formatted error

**3. reset command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().reset_baseline()
- Display success message
- Handle MissionForgeError and display formatted error

**Terminal Output Format (from implementation plan):**

Capture success:
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • matchmaking_latency_ms (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

Commit success with table:
```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

**Registration in app.py:**
Add after the workspace command registration:
```python
from .commands import baseline
app.add_typer(baseline.app, name="baseline")
```

**Requirements:**
- Follow existing command patterns from workspace.py
- Use rich Console for output
- Use rich Table for commit summary
- Handle all MissionForgeError exceptions
- Display errors using console.print with red styling
- Read baseline.json to display metrics in commit command

**Scope:**
- Create NEW file `src/missionforge/cli/commands/baseline.py`
- Modify `src/missionforge/cli/app.py` to register baseline commands
- Follow existing code style from workspace.py

When complete, use `attempt_completion` with a summary of the implementation. and 0 todo items
[new_task in 💻 Code mode: 'Implement Phase 3 of MF-008: CLI Commands

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. The core service layer is complete. Now we need to create the CLI commands that users will interact with.

**Your Task:**
1. Create a new file `src/missionforge/cli/commands/baseline.py` with three commands
2. Register the baseline command group in `src/missionforge/cli/app.py`

**CLI Commands to Implement:**

```python
"""Baseline management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ...core.baseline_service import BaselineService
from ...core.exceptions import MissionForgeError

app = typer.Typer(help="Baseline capture and commit commands")
console = Console()
```

**1. capture command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().capture_baseline()
- Display success message with:
  - Generated file path
  - List of metrics to fill (metric_id and type)
  - Next steps instructions
- Handle MissionForgeError and display formatted error

**2. commit command:**
- Arguments: `sub_mission_id: str`
- Call BaselineService().commit_baseline()
- Display success message with:
  - Committed file path
  - Table showing metrics (metric_id, baseline_target, value)
  - Warning that baseline.json is now immutable
- Handle MissionForgeError and display formatted error

**3. reset command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().reset_baseline()
- Display success message
- Handle MissionForgeError and display formatted error

**Terminal Output Format (from implementation plan):**

Capture success:
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • matchmaking_latency_ms (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

Commit success with table:
```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

**Registration in app.py:**
Add after the workspace command registration:
```python
from .commands import baseline
app.add_typer(baseline.app, name="baseline")
```

**Requirements:**
- Follow existing command patterns from workspace.py
- Use rich Console for output
- Use rich Table for commit summary
- Handle all MissionForgeError exceptions
- Display errors using console.print with red styling
- Read baseline.json to display metrics in commit command

**Scope:**
- Create NEW file `src/missionforge/cli/commands/baseline.py`
- Modify `src/missionforge/cli/app.py` to register baseline commands
- Follow existing code style from workspace.py

When complete, use `attempt_completion` with a summary of the implementation.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 3 of MF-008: CLI Commands

**Context:**
You are implementing the baseline capture and commit flow for MissionForge. The core service layer is complete. Now we need to create the CLI commands that users will interact with.

**Your Task:**
1. Create a new file `src/missionforge/cli/commands/baseline.py` with three commands
2. Register the baseline command group in `src/missionforge/cli/app.py`

**CLI Commands to Implement:**

```python
"""Baseline management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ...core.baseline_service import BaselineService
from ...core.exceptions import MissionForgeError

app = typer.Typer(help="Baseline capture and commit commands")
console = Console()
```

**1. capture command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().capture_baseline()
- Display success message with:
  - Generated file path
  - List of metrics to fill (metric_id and type)
  - Next steps instructions
- Handle MissionForgeError and display formatted error

**2. commit command:**
- Arguments: `sub_mission_id: str`
- Call BaselineService().commit_baseline()
- Display success message with:
  - Committed file path
  - Table showing metrics (metric_id, baseline_target, value)
  - Warning that baseline.json is now immutable
- Handle MissionForgeError and display formatted error

**3. reset command:**
- Arguments: `sub_mission_id: str`
- Options: `--force: bool` (default False)
- Call BaselineService().reset_baseline()
- Display success message
- Handle MissionForgeError and display formatted error

**Terminal Output Format (from implementation plan):**

Capture success:
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • matchmaking_latency_ms (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

Commit success with table:
```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

**Registration in app.py:**
Add after the workspace command registration:
```python
from .commands import baseline
app.add_typer(baseline.app, name="baseline")
```

**Requirements:**
- Follow existing command patterns from workspace.py
- Use rich Console for output
- Use rich Table for commit summary
- Handle all MissionForgeError exceptions
- Display errors using console.print with red styling
- Read baseline.json to display metrics in commit command

**Scope:**
- Create NEW file `src/missionforge/cli/commands/baseline.py`
- Modify `src/missionforge/cli/app.py` to register baseline commands
- Follow existing code style from workspace.py

When complete, use `attempt_completion` with a summary of the implementation. and 0 todo items
<environment_details>
# VSCode Visible Files
src/missionforge/cli/app.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/cli/commands/baseline.py,src/missionforge/cli/app.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:45:19.024Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$2.95

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Completed |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Pending |
| 12 | Register baseline command in CLI app.py | Pending |
| 13 | Create unit tests for baseline models and validation | Pending |
| 14 | Create unit tests for baseline service operations | Pending |
| 15 | Create integration tests for full capture → fill → commit workflow | Pending |
| 16 | Create example fixtures for testing | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! Let me update the todo list and proceed with testing and documentation.

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[x] Create comprehensive implementation plan document
[x] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[x] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[x] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[x] Update JSON schemas for baseline.todo.json and baseline.json validation
[x] Add baseline-specific exceptions to core/exceptions.py
[x] Add baseline path helpers to workspace.py
[x] Create baseline service layer at src/missionforge/core/baseline_service.py
[x] Create baseline command module at src/missionforge/cli/commands/baseline.py
[x] Register baseline command in CLI app.py
[ ] Create test fixtures for baseline testing
[ ] Create unit tests for baseline models and validation
[ ] Create unit tests for baseline service operations
[ ] Create integration tests for full capture → fill → commit workflow
[ ] Update README.md with baseline command documentation
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
src/missionforge/cli/app.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/cli/commands/baseline.py,src/missionforge/cli/app.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml,src/missionforge/cli/utils/validation.py,src/missionforge/cli/commands/workspace.py,src/missionforge/__main__.py,src/missionforge/core/config.py,src/missionforge/core/logging.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:45:25.303Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$3.17

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Completed |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Completed |
| 12 | Register baseline command in CLI app.py | Completed |
| 13 | Create test fixtures for baseline testing | Pending |
| 14 | Create unit tests for baseline models and validation | Pending |
| 15 | Create unit tests for baseline service operations | Pending |
| 16 | Create integration tests for full capture → fill → commit workflow | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let's create comprehensive tests and documentation. I'll start with test fixtures and tests.

<new_task>
<mode>code</mode>
<message>
Implement Phase 5 of MF-008: Testing Infrastructure

**Context:**
You are implementing tests for the baseline capture and commit flow. The core implementation is complete. Now we need comprehensive tests to ensure everything works correctly.

**Your Task:**
Create test fixtures and comprehensive unit tests for the baseline functionality.

**1. Create Test Fixtures Directory and Files:**

Create `tests/fixtures/baseline/` directory with:

**a) `tests/fixtures/baseline/sub-mission-with-metrics.yaml`:**
```yaml
id: MF-001-A
parent: MF-001
title: "Test Sub-Mission with Metrics"
goal: |
  Test sub-mission for baseline testing
depends_on: []
allowed_paths:
  - "src/test/**"
metrics:
  rest_endpoint_exists:
    target: true
  corba_references_count:
    target: 0
  test_coverage:
    target: 85.0
test_command: "pytest tests/"
```

**b) `tests/fixtures/baseline/baseline.todo.json`:**
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": null
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": null
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": null
    }
  ]
}
```

**c) `tests/fixtures/baseline/baseline.todo.filled.json`:**
Same as above but with values filled:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": false
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": 5
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": 78.5
    }
  ]
}
```

**2. Create Unit Tests:**

**a) `tests/unit/test_baseline_models.py`:**
Test the Pydantic models:
- Test SubMissionBaselineMetric validation
- Test SubMissionBaseline validation
- Test type validation for metrics
- Test sub_mission_id format validation
- Test status validation

**b) `tests/unit/test_baseline_service.py`:**
Test the BaselineService:
- Test capture_baseline success
- Test capture_baseline with existing baseline (should fail)
- Test capture_baseline with force flag
- Test commit_baseline success
- Test commit_baseline without capture (should fail)
- Test commit_baseline with incomplete values (should fail)
- Test commit_baseline with type mismatch (should fail)
- Test reset_baseline
- Test file immutability after commit

**Requirements:**
- Use pytest fixtures for setup/teardown
- Use tmp_path for temporary test directories
- Mock Workspace and file operations where appropriate
- Test both success and error cases
- Verify file permissions after commit
- Verify JSON structure matches schemas

**Scope:**
- Create fixtures directory and files
- Create unit test files
- Follow existing test patterns from tests/unit/
- Use pytest and standard testing practices

When complete, use `attempt_completion` with a summary of tests created.
</message>
</new_task>

---

**User:**

[new_task completed] Result: Successfully implemented Phase 5 of MF-008: Testing Infrastructure for baseline functionality.

## Summary of Work Completed:

### 1. Test Fixtures Created (tests/fixtures/baseline/)
- **sub-mission-with-metrics.yaml**: Sample sub-mission with 3 metrics (bool, int, float)
- **baseline.todo.json**: Baseline template with null values
- **baseline.todo.filled.json**: Baseline with filled metric values

### 2. Unit Tests for Models (tests/unit/test_baseline_models.py)
**21 tests covering:**
- SubMissionBaselineMetric validation (bool, int, float, string types)
- Type matching between baseline_target and value
- Type mismatch detection (bool/int, int/float, float/int)
- Empty/whitespace validation for metric_id and description
- SubMissionBaseline validation (status, sub_mission_id format)
- Multiple metrics handling
- Empty metrics list validation

### 3. Unit Tests for Service (tests/unit/test_baseline_service.py)
**16 tests covering:**
- **Capture baseline**: Success, existing baseline error, force flag, missing target error
- **Commit baseline**: Success, no capture error, incomplete values error, type mismatch errors
- **Reset baseline**: Remove todo file, force flag for committed baseline, both files removal, no files error
- **File immutability**: Read-only verification, permission checks

### 4. Test Results
- ✅ All 37 tests passing (21 model + 16 service)
- ✅ 99% code coverage for baseline_service.py
- ✅ 71% code coverage for models/schemas.py (baseline models)
- ✅ Comprehensive error case testing
- ✅ File permission and immutability verification

### Key Testing Patterns Used:
- pytest fixtures for setup/teardown
- tmp_path for isolated test environments
- Pydantic ValidationError testing
- Custom exception testing
- File permission verification
- Type safety validation

The baseline functionality is now fully tested and ready for integration testing in the next phase.

---

**User:**

[new_task in 💻 Code mode: 'Implement Phase 5 of MF-008: Testing Infrastructure

**Context:**
You are implementing tests for the baseline capture and commit flow. The core implementation is complete. Now we need comprehensive tests to ensure everything works correctly.

**Your Task:**
Create test fixtures and comprehensive unit tests for the baseline functionality.

**1. Create Test Fixtures Directory and Files:**

Create `tests/fixtures/baseline/` directory with:

**a) `tests/fixtures/baseline/sub-mission-with-metrics.yaml`:**
```yaml
id: MF-001-A
parent: MF-001
title: "Test Sub-Mission with Metrics"
goal: |
  Test sub-mission for baseline testing
depends_on: []
allowed_paths:
  - "src/test/**"
metrics:
  rest_endpoint_exists:
    target: true
  corba_references_count:
    target: 0
  test_coverage:
    target: 85.0
test_command: "pytest tests/"
```

**b) `tests/fixtures/baseline/baseline.todo.json`:**
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": null
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": null
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": null
    }
  ]
}
```

**c) `tests/fixtures/baseline/baseline.todo.filled.json`:**
Same as above but with values filled:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": false
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": 5
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": 78.5
    }
  ]
}
```

**2. Create Unit Tests:**

**a) `tests/unit/test_baseline_models.py`:**
Test the Pydantic models:
- Test SubMissionBaselineMetric validation
- Test SubMissionBaseline validation
- Test type validation for metrics
- Test sub_mission_id format validation
- Test status validation

**b) `tests/unit/test_baseline_service.py`:**
Test the BaselineService:
- Test capture_baseline success
- Test capture_baseline with existing baseline (should fail)
- Test capture_baseline with force flag
- Test commit_baseline success
- Test commit_baseline without capture (should fail)
- Test commit_baseline with incomplete values (should fail)
- Test commit_baseline with type mismatch (should fail)
- Test reset_baseline
- Test file immutability after commit

**Requirements:**
- Use pytest fixtures for setup/teardown
- Use tmp_path for temporary test directories
- Mock Workspace and file operations where appropriate
- Test both success and error cases
- Verify file permissions after commit
- Verify JSON structure matches schemas

**Scope:**
- Create fixtures directory and files
- Create unit test files
- Follow existing test patterns from tests/unit/
- Use pytest and standard testing practices

When complete, use `attempt_completion` with a summary of tests created.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 5 of MF-008: Testing Infrastructure

**Context:**
You are implementing tests for the baseline capture and commit flow. The core implementation is complete. Now we need comprehensive tests to ensure everything works correctly.

**Your Task:**
Create test fixtures and comprehensive unit tests for the baseline functionality.

**1. Create Test Fixtures Directory and Files:**

Create `tests/fixtures/baseline/` directory with:

**a) `tests/fixtures/baseline/sub-mission-with-metrics.yaml`:**
```yaml
id: MF-001-A
parent: MF-001
title: "Test Sub-Mission with Metrics"
goal: |
  Test sub-mission for baseline testing
depends_on: []
allowed_paths:
  - "src/test/**"
metrics:
  rest_endpoint_exists:
    target: true
  corba_references_count:
    target: 0
  test_coverage:
    target: 85.0
test_command: "pytest tests/"
```

**b) `tests/fixtures/baseline/baseline.todo.json`:**
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": null
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": null
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": null
    }
  ]
}
```

**c) `tests/fixtures/baseline/baseline.todo.filled.json`:**
Same as above but with values filled:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": false
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": 5
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": 78.5
    }
  ]
}
```

**2. Create Unit Tests:**

**a) `tests/unit/test_baseline_models.py`:**
Test the Pydantic models:
- Test SubMissionBaselineMetric validation
- Test SubMissionBaseline validation
- Test type validation for metrics
- Test sub_mission_id format validation
- Test status validation

**b) `tests/unit/test_baseline_service.py`:**
Test the BaselineService:
- Test capture_baseline success
- Test capture_baseline with existing baseline (should fail)
- Test capture_baseline with force flag
- Test commit_baseline success
- Test commit_baseline without capture (should fail)
- Test commit_baseline with incomplete values (should fail)
- Test commit_baseline with type mismatch (should fail)
- Test reset_baseline
- Test file immutability after commit

**Requirements:**
- Use pytest fixtures for setup/teardown
- Use tmp_path for temporary test directories
- Mock Workspace and file operations where appropriate
- Test both success and error cases
- Verify file permissions after commit
- Verify JSON structure matches schemas

**Scope:**
- Create fixtures directory and files
- Create unit test files
- Follow existing test patterns from tests/unit/
- Use pytest and standard testing practices

When complete, use `attempt_completion` with a summary of tests created. and 0 todo items
[new_task in 💻 Code mode: 'Implement Phase 5 of MF-008: Testing Infrastructure

**Context:**
You are implementing tests for the baseline capture and commit flow. The core implementation is complete. Now we need comprehensive tests to ensure everything works correctly.

**Your Task:**
Create test fixtures and comprehensive unit tests for the baseline functionality.

**1. Create Test Fixtures Directory and Files:**

Create `tests/fixtures/baseline/` directory with:

**a) `tests/fixtures/baseline/sub-mission-with-metrics.yaml`:**
```yaml
id: MF-001-A
parent: MF-001
title: "Test Sub-Mission with Metrics"
goal: |
  Test sub-mission for baseline testing
depends_on: []
allowed_paths:
  - "src/test/**"
metrics:
  rest_endpoint_exists:
    target: true
  corba_references_count:
    target: 0
  test_coverage:
    target: 85.0
test_command: "pytest tests/"
```

**b) `tests/fixtures/baseline/baseline.todo.json`:**
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": null
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": null
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": null
    }
  ]
}
```

**c) `tests/fixtures/baseline/baseline.todo.filled.json`:**
Same as above but with values filled:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": false
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": 5
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": 78.5
    }
  ]
}
```

**2. Create Unit Tests:**

**a) `tests/unit/test_baseline_models.py`:**
Test the Pydantic models:
- Test SubMissionBaselineMetric validation
- Test SubMissionBaseline validation
- Test type validation for metrics
- Test sub_mission_id format validation
- Test status validation

**b) `tests/unit/test_baseline_service.py`:**
Test the BaselineService:
- Test capture_baseline success
- Test capture_baseline with existing baseline (should fail)
- Test capture_baseline with force flag
- Test commit_baseline success
- Test commit_baseline without capture (should fail)
- Test commit_baseline with incomplete values (should fail)
- Test commit_baseline with type mismatch (should fail)
- Test reset_baseline
- Test file immutability after commit

**Requirements:**
- Use pytest fixtures for setup/teardown
- Use tmp_path for temporary test directories
- Mock Workspace and file operations where appropriate
- Test both success and error cases
- Verify file permissions after commit
- Verify JSON structure matches schemas

**Scope:**
- Create fixtures directory and files
- Create unit test files
- Follow existing test patterns from tests/unit/
- Use pytest and standard testing practices

When complete, use `attempt_completion` with a summary of tests created.'] Result:
Successfully created new task in 💻 Code mode with message: Implement Phase 5 of MF-008: Testing Infrastructure

**Context:**
You are implementing tests for the baseline capture and commit flow. The core implementation is complete. Now we need comprehensive tests to ensure everything works correctly.

**Your Task:**
Create test fixtures and comprehensive unit tests for the baseline functionality.

**1. Create Test Fixtures Directory and Files:**

Create `tests/fixtures/baseline/` directory with:

**a) `tests/fixtures/baseline/sub-mission-with-metrics.yaml`:**
```yaml
id: MF-001-A
parent: MF-001
title: "Test Sub-Mission with Metrics"
goal: |
  Test sub-mission for baseline testing
depends_on: []
allowed_paths:
  - "src/test/**"
metrics:
  rest_endpoint_exists:
    target: true
  corba_references_count:
    target: 0
  test_coverage:
    target: 85.0
test_command: "pytest tests/"
```

**b) `tests/fixtures/baseline/baseline.todo.json`:**
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": null
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": null
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": null
    }
  ]
}
```

**c) `tests/fixtures/baseline/baseline.todo.filled.json`:**
Same as above but with values filled:
```json
{
  "sub_mission_id": "MF-001-A",
  "metrics": [
    {
      "metric_id": "rest_endpoint_exists",
      "description": "Metric: rest_endpoint_exists",
      "baseline_target": true,
      "value": false
    },
    {
      "metric_id": "corba_references_count",
      "description": "Metric: corba_references_count",
      "baseline_target": 0,
      "value": 5
    },
    {
      "metric_id": "test_coverage",
      "description": "Metric: test_coverage",
      "baseline_target": 85.0,
      "value": 78.5
    }
  ]
}
```

**2. Create Unit Tests:**

**a) `tests/unit/test_baseline_models.py`:**
Test the Pydantic models:
- Test SubMissionBaselineMetric validation
- Test SubMissionBaseline validation
- Test type validation for metrics
- Test sub_mission_id format validation
- Test status validation

**b) `tests/unit/test_baseline_service.py`:**
Test the BaselineService:
- Test capture_baseline success
- Test capture_baseline with existing baseline (should fail)
- Test capture_baseline with force flag
- Test commit_baseline success
- Test commit_baseline without capture (should fail)
- Test commit_baseline with incomplete values (should fail)
- Test commit_baseline with type mismatch (should fail)
- Test reset_baseline
- Test file immutability after commit

**Requirements:**
- Use pytest fixtures for setup/teardown
- Use tmp_path for temporary test directories
- Mock Workspace and file operations where appropriate
- Test both success and error cases
- Verify file permissions after commit
- Verify JSON structure matches schemas

**Scope:**
- Create fixtures directory and files
- Create unit test files
- Follow existing test patterns from tests/unit/
- Use pytest and standard testing practices

When complete, use `attempt_completion` with a summary of tests created. and 0 todo items
<environment_details>
# VSCode Visible Files
tests/unit/test_baseline_service.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/cli/commands/baseline.py,src/missionforge/cli/app.py,tests/fixtures/baseline/sub-mission-with-metrics.yaml,tests/fixtures/baseline/baseline.todo.json,tests/fixtures/baseline/baseline.todo.filled.json,tests/unit/test_baseline_models.py,tests/unit/test_baseline_service.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:49:38.699Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$3.39

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Completed |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Completed |
| 12 | Register baseline command in CLI app.py | Completed |
| 13 | Create test fixtures for baseline testing | Pending |
| 14 | Create unit tests for baseline models and validation | Pending |
| 15 | Create unit tests for baseline service operations | Pending |
| 16 | Create integration tests for full capture → fill → commit workflow | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Excellent! Let me update the todo list and create the final documentation.

<update_todo_list>
<todos>
[x] Review and understand the baseline flow architecture from issue specifications
[x] Analyze relationship between existing schemas and issue requirements
[x] Create comprehensive implementation plan document
[x] Design new Pydantic models for sub-mission baseline (separate from git-based Baseline)
[x] Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value
[x] Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list
[x] Update JSON schemas for baseline.todo.json and baseline.json validation
[x] Add baseline-specific exceptions to core/exceptions.py
[x] Add baseline path helpers to workspace.py
[x] Create baseline service layer at src/missionforge/core/baseline_service.py
[x] Create baseline command module at src/missionforge/cli/commands/baseline.py
[x] Register baseline command in CLI app.py
[x] Create test fixtures for baseline testing
[x] Create unit tests for baseline models and validation
[x] Create unit tests for baseline service operations
[ ] Create integration test for full capture → fill → commit workflow
[ ] Update README.md with baseline command documentation
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
tests/unit/test_baseline_service.py

# VSCode Open Tabs
issues/baseline-flow.md,src/missionforge/core/exceptions.py,src/missionforge/core/workspace.py,src/missionforge/core/baseline_service.py,src/missionforge/cli/commands/baseline.py,src/missionforge/cli/app.py,tests/fixtures/baseline/sub-mission-with-metrics.yaml,tests/fixtures/baseline/baseline.todo.json,tests/fixtures/baseline/baseline.todo.filled.json,tests/unit/test_baseline_models.py,tests/unit/test_baseline_service.py,src/missionforge/git/operations.py,src/missionforge/plugins/base.py,src/missionforge/plugins/registry.py,tests/conftest.py,tests/unit/test_workspace.py,tests/unit/test_config.py,README.md,src/missionforge/utils/subprocess_utils.py,pyproject.toml

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T06:49:45.206Z
User time zone: Asia/Manila, UTC+8:00

# Current Cost
$3.63

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Review and understand the baseline flow architecture from issue specifications | Completed |
| 2 | Analyze relationship between existing schemas and issue requirements | Completed |
| 3 | Create comprehensive implementation plan document | Completed |
| 4 | Design new Pydantic models for sub-mission baseline (separate from git-based Baseline) | Completed |
| 5 | Create SubMissionBaselineMetric model with metric_id, description, baseline_target, value | Completed |
| 6 | Create SubMissionBaseline model with sub_mission_id, timestamp, status, metrics list | Completed |
| 7 | Update JSON schemas for baseline.todo.json and baseline.json validation | Completed |
| 8 | Add baseline-specific exceptions to core/exceptions.py | Completed |
| 9 | Add baseline path helpers to workspace.py | Completed |
| 10 | Create baseline service layer at src/missionforge/core/baseline_service.py | Completed |
| 11 | Create baseline command module at src/missionforge/cli/commands/baseline.py | Completed |
| 12 | Register baseline command in CLI app.py | Completed |
| 13 | Create test fixtures for baseline testing | Completed |
| 14 | Create unit tests for baseline models and validation | Completed |
| 15 | Create unit tests for baseline service operations | Completed |
| 16 | Create integration test for full capture → fill → commit workflow | Pending |
| 17 | Update README.md with baseline command documentation | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let's create the integration test and update the README documentation.

<new_task>
<mode>code</mode>
<message>
Implement Final Phase of MF-008: Integration Test and Documentation

**Context:**
You are completing the baseline capture and commit flow implementation. All unit tests pass. Now we need an integration test for the full workflow and updated documentation.

**Your Task:**

**1. Create Integration Test: `tests/integration/test_baseline_flow.py`**

Create a comprehensive integration test that tests the complete workflow:

```python
"""Integration tests for baseline capture and commit flow."""

import json
from pathlib import Path

import pytest

from missionforge.core.baseline_service import BaselineService
from missionforge.core.exceptions import (
    BaselineAlreadyExistsError,
    BaselineIncompleteError,
    BaselineNotCapturedError,
)
from missionforge.core.workspace import Workspace
```

**Test the complete workflow:**
1. Setup: Create workspace with mission and sub-mission structure
2. Capture: Generate baseline.todo.json from sub-mission.yaml
3. Fill: Simulate Bob filling the values
4. Commit: Commit to baseline.json
5. Verify: Check file immutability and content
6. Reset: Test reset functionality

**Test scenarios:**
- Happy path: capture → fill → commit
- Error: Try to capture when baseline exists
- Error: Try to commit without filling values
- Error: Try to commit with wrong types
- Reset: Remove baseline files

**2. Update README.md**

Add baseline commands documentation after the workspace commands section. Include:

**Section to add:**
```markdown
### Baseline Commands

Baseline commands manage metric measurements for sub-missions before implementation begins.

#### `missionforge baseline capture <SUB_MISSION_ID>`

Capture baseline metrics for a sub-mission.

**Arguments:**
- `SUB_MISSION_ID`: Sub-mission identifier (e.g., `MF-001-A`)

**Options:**
- `--force`: Overwrite existing baseline capture

**Example:**
```bash
missionforge baseline capture MF-001-A
```

**Output:**
```
✓ Baseline captured for MF-001-A

Generated: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.todo.json

Metrics to fill (3):
  • rest_endpoint_exists (bool)
  • corba_references_count (int)
  • test_coverage (float)

Next steps:
1. Analyze the code in allowed paths
2. Fill metric values in baseline.todo.json
3. Run: missionforge baseline commit MF-001-A
```

#### `missionforge baseline commit <SUB_MISSION_ID>`

Commit baseline after filling metric values.

**Arguments:**
- `SUB_MISSION_ID`: Sub-mission identifier (e.g., `MF-001-A`)

**Example:**
```bash
missionforge baseline commit MF-001-A
```

**Output:**
```
✓ Baseline committed for MF-001-A

Committed: .missionforge/missions/MF-001/sub-missions/MF-001-A/baseline.json

Baseline Summary:
┌─────────────────────────┬──────────┬───────┐
│ Metric                  │ Target   │ Value │
├─────────────────────────┼──────────┼───────┤
│ rest_endpoint_exists    │ false    │ false │
│ corba_references_count  │ 7        │ 7     │
│ test_coverage           │ 78.5     │ 78.5  │
└─────────────────────────┴──────────┴───────┘

⚠️  baseline.json is now immutable
```

#### `missionforge baseline reset <SUB_MISSION_ID>`

Reset baseline to allow re-capture.

**Arguments:**
- `SUB_MISSION_ID`: Sub-mission identifier (e.g., `MF-001-A`)

**Options:**
- `--force`: Remove committed baseline (required for committed baselines)

**Example:**
```bash
missionforge baseline reset MF-001-A --force
```
```

**Requirements:**
- Integration test should use real file operations (not mocked)
- Test should create actual workspace structure
- Use tmp_path for isolation
- Verify all files are created correctly
- Test file permissions
- Add README section after workspace commands, before version command
- Follow existing README formatting style

**Scope:**
- Create `tests/integration/test_baseline_flow.py`
- Update `README.md` with baseline commands section
- Ensure integration test covers full workflow

When complete, use `attempt_completion` with a summary of what was added.
</message>
</new_task>

