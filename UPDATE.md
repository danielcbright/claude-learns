# Updating claude-learns

This document contains update instructions and changelog for the claude-learns template.

## How to Update

Use the `/claude-learns.update` command to safely update your installation:

```bash
/update                     # Check for updates (dry run)
/update claude-learns       # Update the template
/update serena              # Update Serena MCP
/update --all               # Update all registered tools
/update --rollback          # Rollback if something goes wrong
```

### Safety Features

- **Git checkpoint**: A commit is created before any update
- **Rollback**: Use `/claude-learns.update --rollback` to undo updates
- **Protected files**: Your memories and specs are never modified
- **Conflict detection**: You're asked before overwriting modified files

---

## Current Version

**Version**: 1.1.0
**Release Date**: 2026-01-19

---

## Changelog

### Version 1.1.0 (2026-01-19)

Two major features: template sync and elimination debugging orchestrator pattern.

#### Features

**Template Sync**
- **Manifest-based updates**: Added `template/manifest.yaml` listing all updateable files with SHA256 checksums
- **Conflict detection**: Detects when user has modified template files and offers choices (keep local, take update, view diff)
- **File categories**:
  - `always_update`: Critical files like the update command itself
  - `updateable`: Commands and scripts with conflict detection
  - `merge_only`: Config files that preserve user values while adding new keys
  - `protected`: User data that is never touched
- **Backup system**: Modified files are backed up to `.claude-learns-backup/` before overwriting
- **Manifest generator**: Added `template/.claude/scripts/generate-manifest.py` for maintainers

**Elimination Debugging Orchestrator Pattern**
- **Orchestrator architecture**: Claude now acts as orchestrator, delegating to specialized subagents
- **Function-based agents**: HypothesisAgent, ResearchAgent, CodeAnalysisAgent, TestRunnerAgent
- **Iterative loop**: Orchestrator cycles through agents until convergence criteria met
- **Script gates preserved**: Existing Python scripts validate work between phases
- **Phase handoff**: Each subagent completes its phase and returns control to orchestrator
- **Updated commands**: `/claude-learns.eliminate` and `/claude-learns.eliminate-status` rewritten

#### Changed

- Updated `/claude-learns.update` command with detailed manifest processing instructions

---

### Version 1.0.0 (2026-01-18)

Initial release of claude-learns template.

#### Features

**Core Commands (7)**
- `/claude-learns.go` - Start tasks with best practices
- `/claude-learns.explore` - Systematically explore codebase
- `/claude-learns.debug` - Structured debugging approach
- `/claude-learns.refactor` - Safe refactoring workflow
- `/claude-learns.learn` - Learning loop with intelligent routing
- `/claude-learns.audit` - Documentation audit
- `/claude-learns.skills` - Skill discovery

**Scientific Elimination Debugging (6)**
- `/claude-learns.eliminate` - Start elimination-based debugging
- `/claude-learns.hypothesis` - Add hypothesis to investigation
- `/claude-learns.evidence` - Record evidence for hypothesis
- `/claude-learns.eliminate-status` - View investigation state
- `/claude-learns.eliminate-history` - Search past sessions
- `/claude-learns.bisect` - Git bisect integration

**Specification System (7)**
- `/claude-learns.spec-create` - Create feature specification
- `/claude-learns.spec-validate` - Validate implementation
- `/claude-learns.spec-debug` - Debug with spec context
- `/claude-learns.spec-deviation` - Log intentional deviation
- `/claude-learns.spec-verify` - Verification gate before claiming done
- `/claude-learns.spec-correction` - Capture corrections
- `/claude-learns.spec-list` - List all specifications

**Update System (1)**
- `/claude-learns.update` - Update tools and template safely

**Installation (1)**
- `/claude-learns.install` - Install template to target project

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

These files are NEVER modified by `/claude-learns.update`:

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

If you installed claude-learns before the `/claude-learns.update` command existed:

1. Create the update registry:
   ```bash
   # The /update command will create this automatically on first run
   /update --list
   ```

2. Your existing memories and customizations are safe - they won't be touched.

3. Run `/claude-learns.update claude-learns` to get latest commands.

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

If the `/claude-learns.update` command itself has issues:

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
   /claude-learns.audit
   ```

---

## Reporting Issues

If you encounter problems with updates:

1. Check rollback is available: `cat .claude/update-checkpoint.txt`
2. Rollback if needed: `/claude-learns.update --rollback`
3. Report issue: https://github.com/danielcbright/claude-learns/issues

Include:
- Your installed version (from `.claude/update-registry.yaml`)
- Error messages
- Steps to reproduce
