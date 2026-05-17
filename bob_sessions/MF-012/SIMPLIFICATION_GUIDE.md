# Simplifying the MissionForge Skill Setup

## TL;DR

For `npx skills add` to work, you **only need**:
- ✅ `skills/missionforge/SKILL.md`

Everything else is optional!

---

## What's Required vs Optional

### Required for `npx skills add`

```
Mission-Forge/
└── skills/
    └── missionforge/
        └── SKILL.md          # ← ONLY THIS IS REQUIRED
```

That's it! When users run `npx skills add <owner>/Mission-Forge`, it:
1. Reads `skills/missionforge/SKILL.md` from your repo
2. Copies it to their agent's skills directory
3. Done!

### Optional (For Local Development)

```
Mission-Forge/
├── .claude/commands/         # ← Optional: Only if YOU use Claude Code
├── .opencode/commands/       # ← Optional: Only if YOU use OpenCode
├── .antigravity/commands/    # ← Optional: Only if YOU use Antigravity
├── .copilot/commands/        # ← Optional: Only if YOU use Copilot
├── .cursor/commands/         # ← Optional: Only if YOU use Cursor
├── .codex/commands/          # ← Optional: Only if YOU use Codex
└── .bob/commands/            # ← Optional: Canonical source (for maintenance)
```

These directories are useful for:
- **Your local development** - Commands work in your agent
- **Contributors** - They get commands when they clone
- **Documentation** - Shows how commands work

But they're **NOT required** for `npx skills add` to work!

---

## Recommended Simplification

### Option 1: Minimal (For Public Distribution)

Keep only what's needed for `npx skills add`:

```bash
# Keep these
skills/missionforge/SKILL.md
CLAUDE.md (optional, for Claude Code users)

# Remove these (or add to .gitignore)
.opencode/
.antigravity/
.copilot/
.cursor/
.codex/
```

**Pros:**
- Clean repository
- Faster clones
- Less maintenance

**Cons:**
- No local slash commands (unless you use Claude Code)
- Contributors need to set up their own commands

### Option 2: Keep Claude Code + Canonical

Keep commands for Claude Code (most popular) and canonical source:

```bash
# Keep these
skills/missionforge/SKILL.md
CLAUDE.md
.claude/commands/
.bob/commands/  # Canonical source

# Remove these
.opencode/
.antigravity/
.copilot/
.cursor/
.codex/
```

**Pros:**
- Works for Claude Code users out of the box
- Maintains canonical source for updates
- Still relatively clean

**Cons:**
- Other agent users need to set up manually

### Option 3: Keep All (Current Setup)

Keep everything for maximum compatibility:

```bash
# Keep everything
skills/missionforge/SKILL.md
CLAUDE.md
.bob/commands/
.claude/commands/
.opencode/commands/
.antigravity/commands/
.copilot/commands/
.cursor/commands/
.codex/commands/
```

**Pros:**
- Works for all agents out of the box
- Best for contributors
- Shows full compatibility

**Cons:**
- More files to maintain
- Larger repository

---

## How to Simplify

### Step 1: Decide What to Keep

Choose Option 1, 2, or 3 above based on your needs.

### Step 2: Remove Unnecessary Directories

```bash
# Example: Keep only skills/ and .claude/
rm -rf .opencode .antigravity .copilot .cursor .codex
```

### Step 3: Update .gitignore (Optional)

If you want to keep them locally but not commit them:

```bash
# Add to .gitignore
echo ".opencode/" >> .gitignore
echo ".antigravity/" >> .gitignore
echo ".copilot/" >> .gitignore
echo ".cursor/" >> .gitignore
echo ".codex/" >> .gitignore
```

### Step 4: Commit Changes

```bash
git add .
git commit -m "Simplify: Keep only required files for npx skills add"
git push
```

---

## What Users Get

### When They Run `npx skills add`

Users get:
- ✅ `skills/missionforge/SKILL.md` copied to their agent
- ✅ All documentation and guidance
- ✅ Instructions for 8 slash commands

They DON'T get:
- ❌ Your local `.claude/commands/` files
- ❌ Your local `.opencode/commands/` files
- ❌ etc.

### How Users Get Slash Commands

Each agent handles this differently:

**Claude Code:**
- Reads `CLAUDE.md` in the project
- Points to `skills/missionforge/SKILL.md`
- Commands work automatically

**Other Agents:**
- Read the installed skill
- Follow the documentation
- May need manual setup (depends on agent)

---

## Recommendation

### For Your Use Case

Since you're publishing for public use, I recommend **Option 1 (Minimal)**:

```bash
# Keep only these
skills/missionforge/SKILL.md  # Required for npx skills add
CLAUDE.md                     # Nice to have for Claude Code users
.bob/commands/                # Optional: Keep as canonical source

# Remove these
rm -rf .opencode .antigravity .copilot .cursor .codex
```

This gives you:
- ✅ Clean repository
- ✅ Works with `npx skills add`
- ✅ Works with Claude Code (most popular)
- ✅ Easy to maintain

### Commands to Run

```bash
# Remove unnecessary directories
rm -rf .opencode .antigravity .copilot .cursor .codex

# Commit
git add .
git commit -m "Simplify: Remove optional agent directories"
git push
```

---

## FAQ

### Q: Will `npx skills add` still work?

**A:** Yes! It only needs `skills/missionforge/SKILL.md`.

### Q: What about users of other agents?

**A:** They can:
1. Install via `npx skills add` (gets the skill documentation)
2. Follow the instructions in SKILL.md
3. Set up their agent manually if needed

### Q: Can I add them back later?

**A:** Yes! Just run:
```bash
mkdir -p .opencode/commands
cp .bob/commands/mf-*.md .opencode/commands/
```

### Q: What if I use multiple agents?

**A:** Keep the directories for agents YOU use. Remove the rest.

---

## Summary

**For `npx skills add` to work:**
- ✅ Only need: `skills/missionforge/SKILL.md`

**For local development:**
- ✅ Keep: `.claude/commands/` (if you use Claude Code)
- ✅ Keep: `.bob/commands/` (canonical source)
- ❌ Remove: Other agent directories (unless you use them)

**Recommended action:**
```bash
rm -rf .opencode .antigravity .copilot .cursor .codex
git add .
git commit -m "Simplify: Keep only required files"
git push
```

This keeps your repo clean while maintaining full `npx skills add` functionality!

---

**Made with Bob** 🤖