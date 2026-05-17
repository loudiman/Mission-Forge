# Multi-Agent Support Plan

## Overview

Extend MissionForge skill system to support all major AI coding agents with agent-specific command directories and installation methods.

---

## Supported Agents

| Agent | Directory | Installation Method | Status |
|-------|-----------|---------------------|--------|
| **Claude Code** | `.claude/commands/` | Built-in (project-local) | ✅ Planned |
| **OpenCode** | `.opencode/commands/` | Project-local commands | ✅ Planned |
| **Antigravity** | `.antigravity/commands/` | Project-local commands | ✅ Planned |
| **GitHub Copilot** | `.copilot/commands/` | Workspace commands | ✅ Planned |
| **Cursor** | `.cursor/commands/` | Project-local commands | ✅ Planned |
| **Any Agent** | `skills/missionforge/SKILL.md` | skills.sh (`npx skills add`) | ✅ Planned |

---

## File Structure

```
Mission-Forge/
├── CLAUDE.md                          # Claude Code skill pointer
├── skills/
│   └── missionforge/
│       └── SKILL.md                   # Universal skill (skills.sh)
├── .bob/
│   └── commands/                      # Canonical source (agent-agnostic)
│       ├── mf-init.md
│       ├── mf-mission.md
│       ├── mf-decompose.md
│       ├── mf-plan.md
│       ├── mf-next.md
│       ├── mf-baseline.md
│       ├── mf-validate.md
│       └── mf-report.md
├── .claude/
│   └── commands/                      # Claude Code slash commands
│       └── [8 mf-*.md files]
├── .opencode/
│   └── commands/                      # OpenCode commands
│       └── [8 mf-*.md files]
├── .antigravity/
│   └── commands/                      # Antigravity commands
│       └── [8 mf-*.md files]
├── .copilot/
│   └── commands/                      # GitHub Copilot workspace commands
│       └── [8 mf-*.md files]
└── .cursor/
    └── commands/                      # Cursor commands
        └── [8 mf-*.md files]
```

**Total Files:** 2 + (8 × 6) = **50 files**
- 1 × CLAUDE.md
- 1 × skills/missionforge/SKILL.md
- 8 × .bob/commands/ (canonical)
- 8 × .claude/commands/
- 8 × .opencode/commands/
- 8 × .antigravity/commands/
- 8 × .copilot/commands/
- 8 × .cursor/commands/

---

## Agent-Specific Installation

### 1. Claude Code

**Installation:**
```bash
# Automatic (project-local)
# Commands available when opening project in Claude Code
```

**Configuration File:** `CLAUDE.md`
```markdown
# missionforge
- **missionforge** (`skills/missionforge/SKILL.md`) — MissionForge workflow skill.
Use when running any MissionForge mission workflow.
```

**Command Location:** `.claude/commands/mf-*.md`

**Usage:**
```
/mf-init MF-001
/mf-baseline MF-001-A --capture
```

---

### 2. OpenCode

**Installation:**
```bash
# Project-local (automatic)
# Commands discovered from .opencode/commands/
```

**Configuration:** None required (auto-discovery)

**Command Location:** `.opencode/commands/mf-*.md`

**Usage:**
```
/mf-init MF-001
/mf-baseline MF-001-A --capture
```

**Notes:**
- OpenCode auto-discovers commands in `.opencode/commands/`
- Markdown format with command metadata
- Same structure as Claude Code commands

---

### 3. Antigravity

**Installation:**
```bash
# Project-local (automatic)
# Commands discovered from .antigravity/commands/
```

**Configuration:** None required (auto-discovery)

**Command Location:** `.antigravity/commands/mf-*.md`

**Usage:**
```
/mf-init MF-001
/mf-baseline MF-001-A --capture
```

**Notes:**
- Antigravity uses similar command discovery to OpenCode
- Supports markdown-based command definitions
- Project-local commands take precedence

---

### 4. GitHub Copilot

**Installation:**
```bash
# Workspace commands (automatic)
# Commands discovered from .copilot/commands/
```

**Configuration:** Optional `.copilot/config.json`
```json
{
  "commands": {
    "directory": ".copilot/commands",
    "prefix": "mf-"
  }
}
```

**Command Location:** `.copilot/commands/mf-*.md`

**Usage:**
```
/mf-init MF-001
/mf-baseline MF-001-A --capture
```

**Notes:**
- GitHub Copilot Workspace supports custom commands
- Markdown format with YAML frontmatter
- Commands available in chat interface

---

### 5. Cursor

**Installation:**
```bash
# Project-local (automatic)
# Commands discovered from .cursor/commands/
```

**Configuration:** Optional `.cursor/config.json`
```json
{
  "commands": {
    "enabled": true,
    "directory": ".cursor/commands"
  }
}
```

**Command Location:** `.cursor/commands/mf-*.md`

**Usage:**
```
/mf-init MF-001
/mf-baseline MF-001-A --capture
```

**Notes:**
- Cursor supports project-local commands
- Similar structure to Claude Code
- Auto-discovery from `.cursor/commands/`

---

### 6. Universal (skills.sh)

**Installation:**
```bash
# One-command install for any agent
npx skills add <owner>/Mission-Forge
```

**Configuration:** Frontmatter in `skills/missionforge/SKILL.md`
```yaml
---
name: missionforge
description: "MissionForge mission workflow for AI agents..."
---
```

**Command Location:** `skills/missionforge/SKILL.md`

**Usage:**
- Agent reads skill documentation
- Follows workflow instructions
- Runs CLI commands as documented

**Notes:**
- Works with any agent that supports skills.sh
- No slash commands (documentation-based)
- Agent interprets and executes workflow

---

## Command File Format

All agent-specific command files use the same format:

```markdown
# /mf-{command}

{One-sentence description}

## Usage
/mf-{command} {args}

## Runs
missionforge {cli-command} $ARGUMENTS

## What Bob Does Next
- **Read:** {file to inspect}
- **Fill:** {file agent must populate} (if applicable)
- **Next command:** /mf-{next-step}

## Example Prompts
- "{example prompt 1}"
- "{example prompt 2}"
- "{example prompt 3}"

## Common Issues
- **Issue:** {common error}
  - **Fix:** {solution}
```

---

## Implementation Strategy

### Phase 1: Core Files
1. Create `CLAUDE.md`
2. Create `skills/missionforge/SKILL.md`
3. Create `.bob/commands/mf-*.md` × 8 (canonical source)

### Phase 2: Agent-Specific Directories
4. Create `.claude/commands/` and copy 8 files
5. Create `.opencode/commands/` and copy 8 files
6. Create `.antigravity/commands/` and copy 8 files
7. Create `.copilot/commands/` and copy 8 files
8. Create `.cursor/commands/` and copy 8 files

### Phase 3: Configuration Files (Optional)
9. Create `.copilot/config.json` (if needed)
10. Create `.cursor/config.json` (if needed)

### Phase 4: Documentation
11. Update SKILL.md with agent-specific instructions
12. Update main README with multi-agent support info
13. Create INSTALLATION.md with per-agent guides

---

## Updated File Count

| Category | Files | Lines |
|----------|-------|-------|
| Core | 2 | ~405 |
| Canonical Commands | 8 | ~420 |
| Claude Code | 8 | ~420 |
| OpenCode | 8 | ~420 |
| Antigravity | 8 | ~420 |
| GitHub Copilot | 8 | ~420 |
| Cursor | 8 | ~420 |
| Config Files | 2 | ~20 |
| **Total** | **52** | **~2,945** |

---

## SKILL.md Updates

Add agent-specific installation section:

```markdown
## Installation

### For Claude Code Users
Commands are automatically available when you open this project.
Use `/mf-*` slash commands in the chat.

### For OpenCode Users
Commands are automatically discovered from `.opencode/commands/`.
Use `/mf-*` commands in the chat interface.

### For Antigravity Users
Commands are automatically discovered from `.antigravity/commands/`.
Use `/mf-*` commands in the chat interface.

### For GitHub Copilot Users
Workspace commands are automatically available.
Use `/mf-*` commands in Copilot Chat.

### For Cursor Users
Commands are automatically discovered from `.cursor/commands/`.
Use `/mf-*` commands in the chat interface.

### For Other Agents (Universal)
Install via skills.sh:
```bash
npx skills add <owner>/Mission-Forge
```

Then follow the workflow documentation in this skill file.
```

---

## Verification Checklist

- [ ] All 5 agent directories created
- [ ] All 8 commands copied to each directory
- [ ] SKILL.md includes agent-specific instructions
- [ ] Configuration files created (if needed)
- [ ] Commands work in Claude Code
- [ ] Commands work in OpenCode
- [ ] Commands work in Antigravity
- [ ] Commands work in GitHub Copilot
- [ ] Commands work in Cursor
- [ ] skills.sh installation works

---

## Benefits of Multi-Agent Support

✅ **Universal Compatibility** - Works with all major AI coding agents  
✅ **Consistent Experience** - Same commands across all agents  
✅ **Easy Adoption** - Developers can use their preferred agent  
✅ **Future-Proof** - Easy to add new agents  
✅ **Single Source of Truth** - `.bob/commands/` is canonical  
✅ **Low Maintenance** - Copy files, no custom logic per agent  

---

## Maintenance Strategy

### Adding a New Command
1. Create in `.bob/commands/mf-new.md`
2. Copy to all 5 agent directories
3. Update SKILL.md if needed

### Updating a Command
1. Update in `.bob/commands/mf-*.md`
2. Copy to all 5 agent directories
3. Verify changes in each agent

### Adding a New Agent
1. Create `.newagent/commands/` directory
2. Copy all 8 files from `.bob/commands/`
3. Add installation instructions to SKILL.md
4. Update this document

---

## Estimated Effort Update

- **Planning:** ✅ Complete (~1.5 hours)
- **Implementation:** ⏳ Ready (~3-4 hours)
  - Core files: 30 min
  - Canonical commands: 1 hour
  - 5 agent directories: 1 hour
  - Configuration files: 30 min
  - Documentation updates: 1 hour
- **Testing:** ⏳ Pending (~1 hour)
  - Test in each agent
- **Documentation:** ⏳ Pending (~30 min)

**Total:** ~6-7 hours for complete multi-agent implementation

---

**Made with Bob** 🤖