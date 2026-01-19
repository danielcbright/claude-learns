---
type: ai-agent-instructions
purpose: Guide Claude Code to install this template into a target project
trigger: When user asks to "use this template" or "add claude-learns to my project"
---

# Installation Guide for AI Agents

> **IMPORTANT**: This file contains instructions for Claude Code when a user points you at this repository and asks you to incorporate it into their project.

## When to Use This Guide

Use these instructions when the user says things like:
- "Use this template for my project"
- "Add claude-learns to my project"
- "Incorporate this into [project path]"
- "Set up Claude memory in my repo"
- "Copy this template to my project"

## Pre-Installation Checklist

Before proceeding, confirm with the user:

1. **Target project path**: Where should files be copied?
2. **Existing files**: Will this overwrite any existing `.claude/` or `.serena/` directories?
3. **Project language(s)**: What programming language(s) does the target project use?
4. **Project name**: What should the project be called in configurations?

## Installation Steps

### Step 1: Copy Core Directories

**Important**: Copy from `template/` directory, not from root-level files.

The root-level files are working copies for template development. The `template/`
directory contains the clean distributable versions.

```
FROM (template/)              TO (target project)
├── template/.claude/         → [target]/.claude/
│   └── commands/             → [target]/.claude/commands/
│       ├── audit.md
│       ├── debug.md
│       ├── explore.md
│       ├── go.md
│       ├── learn.md
│       ├── refactor.md
│       ├── skills.md
│       └── ... (20 commands total)
├── template/.serena/         → [target]/.serena/
│   └── memories/             → [target]/.serena/memories/
├── template/.elimination/    → [target]/.elimination/
├── template/.specify/        → [target]/.specify/
└── template/CLAUDE.md        → [target]/CLAUDE.md
```

### Step 1b: Update .gitignore

Add Claude-specific entries to the target project's `.gitignore`:

```bash
# If target has no .gitignore, copy the template:
cp template/.gitignore.template [target]/.gitignore

# If target already has .gitignore, append Claude entries:
cat >> [target]/.gitignore << 'EOF'

# Claude Code / Serena MCP
.serena/
.elimination/active/
.specify/reports/
EOF
```

Key entries explained:
- `.serena/` - MCP server state (machine-specific)
- `.elimination/active/` - Active debugging sessions (ephemeral)
- `.specify/reports/` - Generated verification reports

### Step 2: Copy and Customize CLAUDE.md

1. Copy `template/CLAUDE.md` to target project root
2. Replace ALL placeholders:
   - `[PROJECT_NAME]` → actual project name
   - `[PRIMARY_LANGUAGE]` → e.g., `typescript`, `go`, `python`
   - `[MAIN_ENTRY]`, `[KEY_CLASS]`, `[CONFIG]` → actual symbols
   - `[path]` → actual file paths
   - `[DATE]` → current date (YYYY-MM-DD)

### Step 3: Customize Memory File

Edit `.serena/memories/claude_code_patterns.md`:
- Replace `[PROJECT_TEST_COMMAND]` with actual test command
- Replace `[PROJECT_LINT_COMMAND]` with actual lint command
- Replace `[PROJECT_BUILD_COMMAND]` with actual build command
- Fill in architecture sections based on target project

### Step 4: Configure MCP Servers (Optional)

If the user wants enhanced functionality, suggest relevant MCP servers:
- **Serena**: For code navigation and symbol lookup
- **Context7**: For external library documentation
- **Sequential Thinking**: For complex architectural decisions

Run `/mcp` to check current MCP server status.

## Post-Installation Verification

After copying files, run health checks. **Output warnings but don't block installation.**

### Verify Commands Installed

Check `.claude/commands/` contains expected files (20 commands total):
- Core: go, explore, debug, refactor, learn, audit, skills
- Elimination: eliminate, hypothesis, evidence, eliminate-status, eliminate-history, bisect
- Spec: spec-create, spec-validate, spec-debug, spec-deviation, spec-list, spec-verify, spec-correction

### Check MCP Availability

Test if Serena MCP is available by calling `list_memories()` or `get_current_config()`.

If not available, warn user:
```
⚠️ Serena MCP not detected
To install: claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project [target]
```

### Prompt for Constitution

Ask user to define 2-3 non-negotiable project rules for `.specify/memory/constitution.md`:
- Example: "All API endpoints must have authentication"
- Example: "No direct database queries outside repository classes"

User can skip and configure later.

### Dry Run /learn Routing

Verify routing destinations exist:
- `.serena/memories/` exists?
- `.specify/memory/corrections.md` exists?
- `.serena/memories/decision-log.md` exists?
- `.elimination/learned/heuristics.yaml` exists?

## Post-Installation Summary

After completing installation and verification, report to user:

```
## Installation Complete!

### Files Created
- .claude/commands/ (20 commands)
- .serena/memories/ (6 memory files)
- .elimination/ (debugging system)
- .specify/ (spec system)
- CLAUDE.md

### Health Check Results
- Commands: ✅ 20/20 installed
- Serena MCP: ✅ Connected / ⚠️ Not detected
- Constitution: ✅ Configured / ⚠️ Skipped
- Routing: ✅ All paths verified

### Next Steps
1. Review and customize CLAUDE.md for your project
2. [If needed] Install Serena MCP
3. [If skipped] Edit .specify/memory/constitution.md
4. Test with: /go [small task]

### Quick Test Commands
- /learn              → Verify routing works
- /eliminate-status   → Should show "No active investigation"
- /spec-list          → Should show specs directory
```

## Files NOT to Copy

Do NOT copy these files (they're template-specific):
- `README.md` (this is the template's readme)
- `INSTALL.md` (this file - for agents only)
- `.git/` directory
- Any `.example` files (use as reference only)

## Handling Existing Files

If target project already has these files:

| File | Action |
|------|--------|
| `.claude/commands/*` | Merge - add missing commands only |
| `.serena/memories/*` | Skip - preserve existing memories |
| `CLAUDE.md` | Ask user - merge or replace? |

## Quick Installation (Single Command Approach)

For users who want minimal interaction, you can execute all steps and report results. Only ask for confirmation before:
1. Overwriting existing CLAUDE.md
2. Modifying existing memories

## Troubleshooting Installation

| Issue | Solution |
|-------|----------|
| Can't write to target | Check permissions, confirm path with user |
| Commands don't appear | Restart Claude Code after copying .claude/ |
| Memories not loading | Check `.serena/memories/` path is correct |

---

*This file is for AI agent consumption. Humans should refer to README.md.*
