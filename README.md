<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Pydantic-v2-e92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic v2">
  <img src="https://img.shields.io/badge/CLI-Typer-009688?style=for-the-badge" alt="Typer">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

# ⚒️ MissionForge

> **A deterministic mission-management CLI that lets AI coding agents decompose, plan, execute, and validate complex software development tasks — with guardrails.**

MissionForge solves a critical problem in AI-assisted software development: **how do you break a large, ambiguous coding task into verifiable, scoped sub-tasks that an AI agent can execute safely?**

Instead of giving an AI agent free rein over an entire codebase, MissionForge enforces **structured decomposition** — every sub-mission has scoped file paths, dependency ordering, measurable metrics, and deterministic validation — so that AI-generated code changes are auditable, bounded, and reproducible.

---

## 🎯 The Problem

AI coding agents (like GitHub Copilot Workspace, Devin, or custom LLM pipelines) struggle with:

| Challenge | What Goes Wrong |
|---|---|
| **Scope creep** | Agents modify files they shouldn't touch |
| **No dependency order** | Agents try to build features before their prerequisites exist |
| **Unverifiable work** | No deterministic proof that the agent's output is correct |
| **Monolithic prompts** | A single large task leads to hallucinated or incomplete implementations |

## 💡 The Solution

MissionForge introduces a **mission → sub-mission → validate** pipeline:

```
┌─────────────────────────────────────────────────────────────┐
│                     Parent Mission                          │
│  goal: "Migrate REST API from Flask to FastAPI"             │
│  forbidden_paths: [".env", "docker-compose.yml"]            │
├──────────┬──────────┬──────────┬───────────────┬────────────┤
│ MF-001-A │ MF-001-B │ MF-001-C │   MF-001-D   │  MF-001-E  │
│ Models   │ Routes   │ Auth     │   Tests       │  Docs      │
│          │ needs: A │ needs: A │ needs: A,B,C  │ needs: ALL │
│ src/     │ src/     │ src/     │   tests/      │  docs/     │
│ models/* │ routes/* │ auth/*   │   **/*        │  **/*      │
└──────────┴──────────┴──────────┴───────────────┴────────────┘
        ↓ topological sort → execution_order → validate each
```

Each sub-mission is **sandboxed** to specific file paths, has explicit **dependency ordering**, and is **validated deterministically** before moving on.

---

## 📦 Installation

Choose the method that fits your use case:

### Option 1 · Install from GitHub (Recommended)

The fastest way to get started. Installs MissionForge as a global CLI tool:

```bash
pip install git+https://github.com/loudiman/Mission-Forge.git
```

After installation, the `missionforge` command is available globally:

```bash
missionforge --help
```

### Option 2 · Clone & Install for Development

If you want to contribute, run tests, or modify the source code:

```bash
# Clone the repository
git clone https://github.com/loudiman/Mission-Forge.git
cd Mission-Forge

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

Or if you use **uv** (recommended for faster dependency resolution):

```bash
git clone https://github.com/loudiman/Mission-Forge.git
cd Mission-Forge

# Sync all dependencies including dev extras
uv sync --all-extras

# Run commands via uv
uv run missionforge --help

# Run tests
uv run pytest tests/ -v
```

### Option 3 · Install Skills for AI Coding Agents

MissionForge ships with **skill files** that teach AI coding agents (e.g., Gemini CLI, Claude Code) the full workflow. After installing the CLI (Option 1 or 2), copy the skills into your project:

```bash
# Clone the repo to get the skills
git clone https://github.com/loudiman/Mission-Forge.git

# Copy the skills directory into your project
cp -r Mission-Forge/skills ./skills
```

Available skills:

| Skill | Trigger Phrases | Description |
|---|---|---|
| `missionforge-workflow` | "missionforge workflow", "start a mission" | End-to-end lifecycle reference |
| `mission-init` | "missionforge init", "new mission" | Workspace initialization |
| `mission-decompose` | "missionforge decompose" | Guided decomposition workflow |
| `mission-validate` | "missionforge validate" | Schema & structural validation |
| `baseline-capture` | "missionforge baseline" | Pre-implementation metric capture |

Your AI agent can then reference these skills to follow the MissionForge workflow autonomously.

### ⚠️ Windows Users

If you're running MissionForge in **Command Prompt** (`cmd.exe`), enable UTF-8 encoding first to avoid Unicode errors:

```cmd
chcp 65001
```

PowerShell and Windows Terminal (the default on Windows 11) handle Unicode natively — no extra step needed.

---

## 🚀 Quick Start

### Your First Mission in 60 Seconds

```bash
# 1. Initialize a mission workspace
missionforge init MF-001

# 2. Edit .missionforge/missions/MF-001/mission.yaml with your goal

# 3. Decompose into sub-missions (guided wizard)
missionforge decompose MF-001

# 4. Create sub-mission files, then validate each one
missionforge validate-submission MF-001 MF-001-A

# 5. Generate a dependency-resolved execution plan
missionforge plan MF-001

# 6. Find what to work on next
missionforge next MF-001

# 7. Generate a PR-ready evidence report
missionforge report MF-001
```

---

## 📋 Core Workflow

### Step 1 · Initialize

```bash
missionforge init MF-001
```

Creates the workspace structure:

```
.missionforge/
└── missions/
    └── MF-001/
        ├── mission.yaml         ← Parent mission definition
        ├── plan.yaml            ← Auto-generated execution plan
        ├── report.md            ← Generated evidence report
        └── sub-missions/        ← Sub-mission definitions
            ├── MF-001-A.yaml
            └── MF-001-B.yaml
```

### Step 2 · Define the Parent Mission

```yaml
# .missionforge/missions/MF-001/mission.yaml
id: MF-001
goal: "Migrate REST API from Flask to FastAPI"
test_command: "pytest tests/ -v"
forbidden_paths:
  - ".env"
  - "docker-compose.yml"
  - "*.secret"
```

### Step 3 · Decompose

```bash
missionforge decompose MF-001
```

The decompose command provides a **guided workflow**: it validates the parent mission, creates the `sub-missions/` directory, displays YAML templates, shows validation instructions, and prints the current status of all sub-missions in a rich table.

### Step 4 · Define Sub-Missions

```yaml
# .missionforge/missions/MF-001/sub-missions/MF-001-A.yaml
id: MF-001-A
parent: MF-001
title: "Create Pydantic models"
goal: "Define all API request/response models with Pydantic v2"
allowed_paths:
  - "src/models/**"
  - "tests/test_models.py"
test_command: "pytest tests/test_models.py -v"
metrics:
  test_coverage:
    min: 80.0
    target: 95.0
```

### Step 5 · Validate

```bash
missionforge validate-submission MF-001 MF-001-A
```

**Validation checks:**
- ✅ Sub-mission ID format (`MF-001-[A-Z]`)
- ✅ Parent reference matches
- ✅ `allowed_paths` don't conflict with parent's `forbidden_paths`
- ✅ No overlapping paths with sibling sub-missions (warnings)
- ✅ All `depends_on` references exist
- ✅ YAML schema compliance via Pydantic v2

### Step 6 · Plan

```bash
missionforge plan MF-001
```

Automatically resolves the dependency graph using **topological sort (Kahn's algorithm)**, detects circular dependencies, computes parallelism levels, and writes a fully resolved `plan.yaml`.

### Step 7 · Execute & Report

```bash
# Find the next sub-mission ready for execution
missionforge next MF-001

# Capture baseline metrics before starting
missionforge baseline capture MF-001-A

# After completing work, commit baseline and generate a PR-ready report
missionforge baseline commit MF-001-A
missionforge report MF-001
```

---

## 🔧 Full CLI Reference

| Command | Description |
|---|---|
| `missionforge init <ID>` | Initialize a new mission workspace |
| `missionforge mission <ID> --validate` | Validate a parent mission file |
| `missionforge decompose <ID>` | Guided decomposition wizard |
| `missionforge validate-submission <ID> <SUB_ID>` | Validate a specific sub-mission |
| `missionforge plan <ID>` | Generate dependency-resolved execution plan |
| `missionforge next <ID>` | Identify next actionable sub-mission(s) |
| `missionforge baseline capture <SUB_ID>` | Capture pre-implementation metrics |
| `missionforge baseline commit <SUB_ID>` | Commit (freeze) baseline metrics |
| `missionforge baseline reset <SUB_ID>` | Reset baseline for re-capture |
| `missionforge validate capture <SUB_ID>` | Capture post-implementation validation |
| `missionforge validate commit <SUB_ID>` | Commit final validation results |
| `missionforge report <ID>` | Generate PR-ready Markdown report |
| `missionforge workspace status` | Show all missions and their status |
| `missionforge version` | Show version information |

**Global Options:** `--verbose / -v` for debug output, `--log-file PATH` to write logs to a file.

---

## 🏗️ Architecture

```
src/missionforge/
├── cli/                         # Typer CLI application
│   ├── app.py                   # Main entrypoint & command registration
│   ├── commands/                # Command implementations
│   │   ├── workspace.py         #   init, status
│   │   ├── mission.py           #   validate parent mission
│   │   ├── decompose.py         #   decompose + validate-submission
│   │   ├── plan.py              #   dependency graph resolution
│   │   ├── next.py              #   next-ready identification
│   │   ├── baseline.py          #   capture / commit / reset
│   │   ├── validate.py          #   post-implementation validation
│   │   └── report.py            #   PR-ready report generation
│   └── utils/validation.py      # Input validation helpers
├── core/                        # Business logic
│   ├── workspace.py             # Path resolution & discovery
│   ├── mission_validator.py     # Schema + structural validation
│   ├── report_generator.py      # Markdown report engine
│   ├── config.py                # User-level configuration
│   ├── exceptions.py            # Structured error hierarchy
│   └── logging.py               # Logging setup
├── models/schemas.py            # 20+ Pydantic v2 models
├── schemas/validators.py        # Cross-schema validation
├── plugins/                     # Extensible plugin system
│   ├── base.py                  # Abstract base classes
│   └── registry.py              # Plugin discovery & loading
├── git/operations.py            # Safe git subprocess wrappers
├── templates/                   # Jinja2 report templates
└── utils/subprocess_utils.py    # Safe subprocess execution
```

### Design Principles

| Principle | Implementation |
|---|---|
| **Language Agnostic** | CLI handles only deterministic operations (git, file paths, tests). AI reasoning happens externally. |
| **Zero Shell Injection** | All subprocess calls use `list` arguments, never `shell=True`. |
| **Type-Safe Everything** | Full type hints with 20+ Pydantic v2 models and strict validation. |
| **Plugin Architecture** | Extensible via `ValidatorPlugin`, `MetricCollectorPlugin`, `FormatterPlugin`, and `CommandPlugin` base classes. |
| **Deterministic Validation** | Every check is reproducible — no LLM calls, no non-determinism. |

---

## 🔒 Security

- **No `shell=True`** — All subprocess calls use list arguments to prevent shell injection.
- **No GitPython** — Uses system `git` via subprocess for better security and auditability.
- **Path traversal protection** — Report output paths are validated against workspace boundaries.
- **Scoped file access** — Sub-missions can only modify files matching their `allowed_paths` glob patterns.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=missionforge --cov-report=html

# Run specific test suites
pytest tests/unit/ -v
pytest tests/integration/ -v
```

The test suite includes:
- **Unit tests** for schema validation, workspace resolution, and mission validation
- **Integration tests** for the full CLI command lifecycle (init → decompose → validate → plan)

---

## 📝 Mission ID Format

| Type | Pattern | Examples |
|---|---|---|
| **Parent Mission** | `[A-Z]{2,4}-\d{3}[A-Z]?` | `MF-001`, `PROJ-042`, `FG-123A` |
| **Sub-Mission** | `[A-Z]{2,4}-\d{3}-[A-Z]` | `MF-001-A`, `PROJ-042-B` |

Each parent mission supports up to **26 sub-missions** (A–Z) — an intentional design constraint to keep decompositions focused and reviewable.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass: `pytest tests/`
5. Format code: `black src/ tests/` · Lint: `ruff check src/ tests/`
6. Submit a pull request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Built with ❤️ for AI-assisted software development</strong><br>
  <em>Made with Bob</em>
</p>
