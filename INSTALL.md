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

Copy these directories to the target project root:

```
FROM (this template)          TO (target project)
├── .claude/                  → [target]/.claude/
│   └── commands/             → [target]/.claude/commands/
│       ├── audit.md
│       ├── debug.md
│       ├── explore.md
│       ├── go.md
│       ├── learn.md
│       ├── refactor.md
│       └── skills.md
└── .serena/                  → [target]/.serena/
    └── memories/             → [target]/.serena/memories/
        └── claude_code_patterns.md
```

### Step 2: Copy and Customize CLAUDE.md

1. Copy `CLAUDE.md` to target project root
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

## Post-Installation Summary

After completing installation, report to user:

```
Template installation complete!

Files created:
- .claude/commands/ (7 slash commands)
- .serena/memories/claude_code_patterns.md
- CLAUDE.md

Next steps:
1. Review and customize CLAUDE.md for your project
2. Fill in project-specific sections
3. (Optional) Configure MCP servers with /mcp
4. Test with: /go [small task]

Available commands:
- /go [task] - Start task with best practices
- /explore [area] - Explore codebase systematically
- /debug [issue] - Debug with structured approach
- /refactor [target] - Safe refactoring
- /learn - Trigger learning loop
- /audit - Check documentation freshness
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
