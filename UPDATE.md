# Updating claude-learns

This document contains update instructions and changelog for the claude-learns template.

## How to Update

Use the `/update` command to safely update your installation:

```bash
/update                     # Check for updates (dry run)
/update claude-learns       # Update the template
/update serena              # Update Serena MCP
/update --all               # Update all registered tools
/update --rollback          # Rollback if something goes wrong
```

### Safety Features

- **Git checkpoint**: A commit is created before any update
- **Rollback**: Use `/update --rollback` to undo updates
- **Protected files**: Your memories and specs are never modified
- **Conflict detection**: You're asked before overwriting modified files

---

## Current Version

**Version**: 1.0.0
**Release Date**: 2026-01-18

---

## Changelog

### Version 1.0.0 (2026-01-18)

Initial release of claude-learns template.

#### Features

**Core Commands (7)**
- `/go` - Start tasks with best practices
- `/explore` - Systematically explore codebase
- `/debug` - Structured debugging approach
- `/refactor` - Safe refactoring workflow
- `/learn` - Learning loop with intelligent routing
- `/audit` - Documentation audit
- `/skills` - Skill discovery

**Scientific Elimination Debugging (6)**
- `/eliminate` - Start elimination-based debugging
- `/hypothesis` - Add hypothesis to investigation
- `/evidence` - Record evidence for hypothesis
- `/eliminate-status` - View investigation state
- `/eliminate-history` - Search past sessions
- `/bisect` - Git bisect integration

**Specification System (7)**
- `/spec-create` - Create feature specification
- `/spec-validate` - Validate implementation
- `/spec-debug` - Debug with spec context
- `/spec-deviation` - Log intentional deviation
- `/spec-verify` - Verification gate before claiming done
- `/spec-correction` - Capture corrections
- `/spec-list` - List all specifications

**Update System (1)**
- `/update` - Update tools and template safely

**Installation (1)**
- `/install` - Install template to target project

#### Memory System

- `claude_code_patterns.md` - Session quick reference
- `elimination_patterns.md` - Elimination debugging reference
- `debugging-lessons.md` - Past bugs and resolutions
- `common-bugs.md` - Recurring patterns by feature
- `decision-log.md` - Architectural decisions
- `tool-documentation.md` - Links to latest docs

#### Infrastructure

- Dual-location architecture (root for dev, template/ for distribution)
- Git safety protocol for updates
- Tool registry for multi-tool updates
- Serena MCP integration documented

---

## Protected Files

These files are NEVER modified by `/update`:

| Path | Content |
|------|---------|
| `.serena/memories/*` | Your learned knowledge |
| `.specify/specs/*` | Your feature specifications |
| `.specify/memory/constitution.md` | Your project rules |
| `.specify/memory/corrections.md` | Your correction history |
| `.elimination/active/*` | Active debugging sessions |
| `.elimination/archive/*` | Historical debugging data |

---

## Breaking Changes

### Version 1.0.0

No breaking changes (initial release).

---

## Migration Guides

### From Pre-1.0 (Manual Installation)

If you installed claude-learns before the `/update` command existed:

1. Create the update registry:
   ```bash
   # The /update command will create this automatically on first run
   /update --list
   ```

2. Your existing memories and customizations are safe - they won't be touched.

3. Run `/update claude-learns` to get latest commands.

---

## Rollback Instructions

If an update causes problems:

```bash
/update --rollback
```

This will:
1. Reset to the checkpoint commit created before the update
2. Restore all files to their pre-update state
3. Remove the checkpoint file

**Note**: Any changes made after the update will be lost during rollback.

---

## Manual Update (If /update Fails)

If the `/update` command itself has issues:

1. **Create a backup**:
   ```bash
   git add -A && git commit -m "backup before manual update"
   ```

2. **Fetch latest files**:
   ```bash
   # Clone fresh copy
   git clone https://github.com/danielcbright/claude-learns.git /tmp/claude-learns-latest

   # Copy only command files (not memories!)
   cp /tmp/claude-learns-latest/template/.claude/commands/*.md .claude/commands/
   ```

3. **Verify**:
   ```bash
   /audit
   ```

---

## Reporting Issues

If you encounter problems with updates:

1. Check rollback is available: `cat .claude/update-checkpoint.txt`
2. Rollback if needed: `/update --rollback`
3. Report issue: https://github.com/danielcbright/claude-learns/issues

Include:
- Your installed version (from `.claude/update-registry.yaml`)
- Error messages
- Steps to reproduce
