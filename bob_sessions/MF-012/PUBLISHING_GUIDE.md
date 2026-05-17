# Publishing MissionForge Skill to skills.sh

## Overview

To make the MissionForge skill publicly installable via `npx skills add`, you need to publish it to the skills.sh ecosystem.

---

## Prerequisites

1. **GitHub Repository**
   - Repository must be public
   - Contains `skills/missionforge/SKILL.md`

2. **skills.sh Account** (if required)
   - Visit https://skills.sh
   - Create account if needed

---

## Method 1: Direct GitHub Installation (Recommended)

The simplest method - users install directly from your GitHub repository.

### Step 1: Ensure Repository is Public

```bash
# Check if repo is public on GitHub
# Go to: https://github.com/<owner>/Mission-Forge/settings
# Under "Danger Zone" → Change visibility to Public
```

### Step 2: Users Install via GitHub URL

Users can install with:

```bash
# Full GitHub URL
npx skills add https://github.com/<owner>/Mission-Forge

# Or shorthand (if skills.sh supports it)
npx skills add <owner>/Mission-Forge
```

### How It Works

1. `npx skills add` reads from your GitHub repo
2. Finds `skills/missionforge/SKILL.md`
3. Copies it to user's skills directory (e.g., `~/.claude/skills/missionforge/`)
4. Skill is now available to the agent

---

## Method 2: Publish to skills.sh Registry (If Available)

If skills.sh has a central registry:

### Step 1: Create skills.json (if required)

Create `skills.json` in repository root:

```json
{
  "name": "missionforge",
  "version": "1.0.0",
  "description": "MissionForge mission workflow for AI agents",
  "author": "<your-name>",
  "repository": "https://github.com/<owner>/Mission-Forge",
  "skills": [
    {
      "name": "missionforge",
      "path": "skills/missionforge/SKILL.md",
      "description": "Complete MissionForge workflow with 8 slash commands"
    }
  ]
}
```

### Step 2: Register with skills.sh

```bash
# If skills.sh has a CLI tool
npx skills publish

# Or via web interface
# Visit https://skills.sh/publish
# Submit your repository URL
```

### Step 3: Users Install from Registry

```bash
npx skills add missionforge
```

---

## Current Setup (Already Complete)

Your repository is already set up correctly:

✅ **File Location:** `skills/missionforge/SKILL.md`
✅ **Frontmatter:** Proper YAML frontmatter with name and description
✅ **Content:** Complete skill documentation
✅ **Structure:** Follows skills.sh conventions

---

## Installation Instructions for Users

### For Your Repository

Add this to your README.md:

```markdown
## Installation

### Install MissionForge Skill

```bash
# Install from GitHub
npx skills add <owner>/Mission-Forge
```

This installs the MissionForge skill to your AI agent, enabling `/mf-*` slash commands.

### Supported Agents

- Claude Code
- OpenCode
- Antigravity
- GitHub Copilot
- Cursor
- Codex
- Any agent supporting skills.sh

### Verify Installation

After installation, the skill will be available at:
- Claude Code: `~/.claude/skills/missionforge/`
- Other agents: Check agent-specific skills directory

### Usage

Once installed, use slash commands:
- `/mf-init MF-001` - Initialize mission
- `/mf-baseline MF-001-A --capture` - Capture baseline
- And 6 more commands...
```

---

## Testing Installation

### Test Locally

```bash
# Test the installation command
npx skills add file:///path/to/Mission-Forge

# Or test from GitHub (after pushing)
npx skills add https://github.com/<owner>/Mission-Forge
```

### Verify Installation

```bash
# Check if skill was installed
ls -la ~/.claude/skills/missionforge/

# Should see SKILL.md
cat ~/.claude/skills/missionforge/SKILL.md
```

---

## Distribution Options

### Option 1: GitHub Only (Simplest)

✅ **Pros:**
- No additional setup
- Works immediately
- Full control

❌ **Cons:**
- Users need full GitHub URL
- No version management

**Installation:**
```bash
npx skills add <owner>/Mission-Forge
```

### Option 2: skills.sh Registry (If Available)

✅ **Pros:**
- Shorter install command
- Version management
- Discoverability

❌ **Cons:**
- Requires registration
- May have approval process

**Installation:**
```bash
npx skills add missionforge
```

### Option 3: npm Package (Alternative)

Publish as npm package:

```bash
npm publish @<owner>/missionforge-skill
```

**Installation:**
```bash
npx @<owner>/missionforge-skill install
```

---

## Recommended Approach

### For Immediate Use

1. **Push to GitHub** (ensure repo is public)
2. **Update README** with installation instructions
3. **Share GitHub URL** with users

```bash
npx skills add <owner>/Mission-Forge
```

### For Long-Term

1. **Register with skills.sh** (if registry exists)
2. **Publish to npm** (for broader distribution)
3. **Create releases** on GitHub for versioning

---

## Example README Section

Add this to your main README.md:

```markdown
## 🚀 Quick Start with AI Agents

### Install MissionForge Skill

```bash
npx skills add <owner>/Mission-Forge
```

This installs the MissionForge skill system, enabling 8 powerful slash commands in your AI coding agent.

### Available Commands

- `/mf-init <ID>` - Initialize mission
- `/mf-mission <ID> --validate` - Validate mission
- `/mf-decompose <ID>` - Decompose into sub-missions
- `/mf-plan <ID>` - Generate execution plan
- `/mf-next <ID>` - Show next ready sub-mission
- `/mf-baseline <SUB_ID> --capture|--commit` - Baseline metrics
- `/mf-validate <SUB_ID> --capture|--commit` - Validation metrics
- `/mf-report <ID>` - Generate final report

### Supported Agents

✅ Claude Code
✅ OpenCode
✅ Antigravity
✅ GitHub Copilot
✅ Cursor
✅ Codex

### Learn More

See [skills/missionforge/SKILL.md](skills/missionforge/SKILL.md) for complete documentation.
```

---

## Troubleshooting

### Issue: "Skill not found"

**Solution:**
- Ensure repository is public
- Check file exists at `skills/missionforge/SKILL.md`
- Verify frontmatter is correct

### Issue: "Installation failed"

**Solution:**
- Check internet connection
- Verify GitHub URL is correct
- Try with full URL: `https://github.com/<owner>/Mission-Forge`

### Issue: "Skill not appearing in agent"

**Solution:**
- Restart agent
- Check agent's skills directory
- Verify agent supports skills.sh

---

## Next Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add MissionForge skill system"
   git push origin main
   ```

2. **Make Repository Public**
   - Go to GitHub repository settings
   - Change visibility to Public

3. **Test Installation**
   ```bash
   npx skills add <owner>/Mission-Forge
   ```

4. **Update README**
   - Add installation instructions
   - Document slash commands
   - Link to SKILL.md

5. **Share with Community**
   - Post on skills.sh (if available)
   - Share on social media
   - Add to agent marketplaces

---

## Maintenance

### Updating the Skill

1. Make changes to `skills/missionforge/SKILL.md`
2. Commit and push to GitHub
3. Users reinstall to get updates:
   ```bash
   npx skills add <owner>/Mission-Forge --force
   ```

### Versioning

Consider using Git tags for versions:

```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

Users can install specific versions:
```bash
npx skills add <owner>/Mission-Forge@v1.0.0
```

---

**Made with Bob** 🤖