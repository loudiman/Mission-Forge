# MF-012: Bob Skill and Slash Commands

## Mission Overview

Create a universal skill system with 8 slash commands for MissionForge workflow, supporting all major AI coding agents (Claude Code, OpenCode, Antigravity, GitHub Copilot, Cursor) plus universal installation via `npx skills add` (skills.sh ecosystem).

**Core Principle:** "Bob measures the code. MissionForge measures the mission."

---

## Planning Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [PLAN_SUMMARY.md](PLAN_SUMMARY.md) | Executive summary and overview | ✅ Complete |
| [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | Detailed implementation specifications | ✅ Complete |
| [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md) | Visual workflow and architecture | ✅ Complete |
| [METRIC_MEASUREMENT_GUIDE.md](METRIC_MEASUREMENT_GUIDE.md) | Comprehensive metric measurement guide | ✅ Complete |
| [MULTI_AGENT_SUPPORT.md](MULTI_AGENT_SUPPORT.md) | Multi-agent support strategy | ✅ Complete |

---

## Quick Reference

### Files to Create (52 total)

1. **`CLAUDE.md`** - Project root, points to skill
2. **`skills/missionforge/SKILL.md`** - Installable skill (~400 lines)
3-10. **`.bob/commands/mf-*.md`** × 8 - Canonical command docs (source of truth)
11-18. **`.claude/commands/mf-*.md`** × 8 - Claude Code slash commands
19-26. **`.opencode/commands/mf-*.md`** × 8 - OpenCode commands
27-34. **`.antigravity/commands/mf-*.md`** × 8 - Antigravity commands
35-42. **`.copilot/commands/mf-*.md`** × 8 - GitHub Copilot commands
43-50. **`.cursor/commands/mf-*.md`** × 8 - Cursor commands
51-52. **Config files** - Optional agent configurations

### Slash Commands

| Command | Purpose | CLI Wrapped |
|---------|---------|-------------|
| `/mf-init` | Initialize mission | `missionforge init <ID>` |
| `/mf-mission` | Validate mission | `missionforge mission <ID> --validate` |
| `/mf-decompose` | Decompose into sub-missions | `missionforge decompose <ID>` |
| `/mf-plan` | Generate execution plan | `missionforge plan <ID>` |
| `/mf-next` | Show next ready sub-mission | `missionforge plan <ID>` |
| `/mf-baseline` | Capture/commit baseline | `missionforge baseline capture/commit <SUB_ID>` |
| `/mf-validate` | Capture/commit validation | `missionforge validate capture/commit <SUB_ID>` |
| `/mf-report` | Generate final report | `missionforge plan <ID>` |

---

## Workflow at a Glance

```
init → validate → decompose → plan → next
  ↓
  FOR EACH SUB-MISSION:
    baseline capture → baseline commit → implement
    → validate capture → validate commit
  ↓
validate parent → report
```

---

## Key Features

✅ **Universal Multi-Agent Support** - Works with 5+ major AI coding agents
✅ **One-Command Install** - `npx skills add <owner>/Mission-Forge`
✅ **Complete Workflow** - All 8 mission steps covered
✅ **Enhanced Docs** - Metric measurement, troubleshooting, examples
✅ **Clear Guidance** - Next steps for every command
✅ **Single Source of Truth** - `.bob/commands/` is canonical

---

## Implementation Status

### Planning Phase: ✅ Complete

- [x] Analyzed MissionForge codebase
- [x] Reviewed CLI commands and source code
- [x] Created comprehensive implementation plan
- [x] Designed workflow diagrams
- [x] Documented metric measurement guide
- [x] Planned multi-agent support strategy
- [x] Specified all 52 files to create
- [x] Defined success criteria

### Implementation Phase: ⏳ Ready to Start

**Next Action:** Switch to Code mode to implement all 12 files

---

## Success Criteria

✅ External devs can install with: `npx skills add <owner>/Mission-Forge`
✅ Works with 5+ major AI coding agents
✅ All 8 slash commands work in each agent
✅ Clear guidance at every workflow step
✅ Agents understand Bob vs CLI responsibilities
✅ Metric measurement is well-documented
✅ Common errors have documented solutions

---

## Estimated Effort

- **Planning:** ✅ Complete (~1.5 hours)
- **Implementation:** ⏳ Ready (~3-4 hours)
- **Testing:** ⏳ Pending (~1 hour, test in each agent)
- **Documentation:** ⏳ Pending (~30 min)

**Total:** ~5-6 hours end-to-end

---

## Quick Start (After Implementation)

### For External Developers
```bash
# Install the skill
npx skills add <owner>/Mission-Forge

# Start using slash commands
/mf-init MF-001
```

### For This Repository
```bash
# Skill is already available
# Just use the slash commands in Claude Code
/mf-init MF-001
```

---

## Documentation Structure

```
Mission-Forge/
├── CLAUDE.md                          # Points to skill
├── skills/missionforge/SKILL.md       # Main skill file
├── .bob/commands/                     # Canonical docs (source of truth)
│   └── [8 mf-*.md files]
├── .claude/commands/                  # Claude Code commands
│   └── [8 mf-*.md files]
├── .opencode/commands/                # OpenCode commands
│   └── [8 mf-*.md files]
├── .antigravity/commands/             # Antigravity commands
│   └── [8 mf-*.md files]
├── .copilot/commands/                 # GitHub Copilot commands
│   └── [8 mf-*.md files]
└── .cursor/commands/                  # Cursor commands
    └── [8 mf-*.md files]
```

---

## References

- **Main README:** [../../README.md](../../README.md)
- **Decompose Docs:** [../../docs/DECOMPOSE_COMMAND.md](../../docs/DECOMPOSE_COMMAND.md)
- **CLI Source:** [../../src/missionforge/cli/](../../src/missionforge/cli/)
- **AGENTS.md:** [../../.bob/rules-plan/AGENTS.md](../../.bob/rules-plan/AGENTS.md)

---

## Contact

For questions or issues with this plan, refer to the planning documents above or consult the main project README.

---

**Status:** ✅ Planning Complete - Ready for Implementation

**Made with Bob** 🤖