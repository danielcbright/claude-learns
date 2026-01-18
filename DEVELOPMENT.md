# Developing claude-learns

> This file provides guidance for developing the claude-learns template itself.

## The Bootstrapping Problem

When Claude Code opens this repository, it loads `.claude/commands/` as available slash commands. However, these commands are designed for projects USING the template, not for developing the template itself.

**The risk**: Running `/learn` while developing could write learnings to `.serena/memories/`, polluting the template content that gets copied to other projects.

## Dual-Location Architecture

This project uses a dual-location architecture to solve the bootstrapping problem:

```
claude-learns/
├── .claude/commands/        # Working copies (development)
├── .serena/memories/        # Working copies (development)
├── .elimination/            # Working copies (development)
├── .specify/                # Working copies (development)
├── CLAUDE.md                # Working copy (development)
│
├── template/                # CLEAN DISTRIBUTABLE COPIES
│   ├── .claude/commands/    # Template commands
│   ├── .serena/memories/    # Template memories (with placeholders)
│   ├── .elimination/        # Template elimination system
│   ├── .specify/            # Template spec system
│   └── CLAUDE.md            # Template CLAUDE.md (with placeholders)
│
├── test-projects/           # Installation test targets
├── DEVELOPMENT.md           # This file
├── INSTALL.md               # Installation instructions
└── README.md                # Project overview
```

### Root Level (Development)

- Claude Code loads these as active commands
- Can be modified by `/learn`, `/eliminate`, etc. during development
- Used for testing and iterating on the template
- May contain development-specific content

### template/ (Distributable)

- Never loaded by Claude Code (not at root level)
- These are what `/install` copies to target projects
- Kept pristine with `[PLACEHOLDER]` values
- This is what users receive

---

## Safe vs Unsafe Operations

### Safe Operations (Development)

| Operation | Why Safe |
|-----------|----------|
| Editing command files directly | You're editing the template intentionally |
| Editing memory file templates | Explicit template work |
| Running `/audit` | Read-only, reports issues |
| Running `/spec-list` | Read-only |
| Running `/eliminate-status` | Read-only |
| Testing in `test-projects/` | Isolated from template |

### Operations That Modify Root Files

These modify root-level files, which is fine for development but should be synced to `template/` carefully:

| Operation | What It Modifies |
|-----------|-----------------|
| `/learn` | `.serena/memories/`, `.specify/memory/`, `.elimination/learned/` |
| `/eliminate` | `.elimination/active/`, `.elimination/logs/` |
| `/hypothesis`, `/evidence` | `.elimination/active/` |
| `/spec-create` | `.specify/specs/` |
| `/spec-deviation` | `.specify/deviations/` |
| `/spec-correction` | `.specify/memory/corrections.md` |

---

## Development Workflow

### 1. Make Changes to Root Files

Work in root-level files (`.claude/`, `.serena/`, etc.) as normal:

```bash
# Edit a command
vim .claude/commands/learn.md

# Test it naturally
/learn
```

### 2. Test Installation

Use test-projects/ to validate the installation process:

```bash
# Install to a test project
cd test-projects/minimal-js
# Then ask Claude to install the template here
```

### 3. Sync to template/

**IMPORTANT**: Not all files can be blindly synced. Follow this categorized approach:

#### Category A: Direct Sync (Generic Files)

These files are generic instructions and can be synced directly:

```bash
# Commands - generic instruction files
rsync -av .claude/commands/ template/.claude/commands/

# Update registry - generic tool definitions
cp .claude/update-registry.yaml template/.claude/update-registry.yaml

# Elimination system configs and templates (NOT active data)
rsync -av .elimination/config.yaml template/.elimination/
rsync -av .elimination/samples/ template/.elimination/samples/
rsync -av .elimination/learned/templates/ template/.elimination/learned/templates/

# Specify system configs and templates (NOT user specs)
rsync -av .specify/config.yaml template/.specify/
rsync -av .specify/templates/ template/.specify/templates/
```

#### Category B: Must Be Templated (Need Placeholders)

These files contain development-specific content and must be MANUALLY reviewed/edited:

| File | Must Have | NOT Have |
|------|-----------|----------|
| `template/CLAUDE.md` | `[PROJECT_NAME]`, `[PRIMARY_LANGUAGE]`, `[DATE]` | Real project names, dates |
| `template/.serena/memories/*.md` | Generic examples, placeholder content | Real learnings, decisions |
| `template/.specify/memory/constitution.md` | Example rules with `[PLACEHOLDER]` | Real project rules |
| `template/.specify/memory/corrections.md` | Empty or example structure | Real corrections |
| `template/.elimination/learned/heuristics.yaml` | Generic starting patterns | Project-specific patterns |

**Procedure for Category B files:**

1. **DO NOT rsync** - these need manual handling
2. Compare root file with template file: `diff root-file template/file`
3. If template has correct placeholders, only copy NEW SECTIONS from root
4. If syncing structural changes, restore placeholders afterward

#### Category C: Never Sync (User Data Directories)

These directories should only contain `.gitkeep` files and **intentional educational samples**:

```
template/.elimination/active/      # User's debugging sessions (empty)
template/.elimination/archive/     # User's past sessions (empty)
template/.elimination/logs/        # Empty template structure only
template/.specify/specs/           # Sample spec only (sample-feature/)
template/.specify/deviations/      # Sample deviation only (sample-feature-001.md)
template/.specify/reports/         # User's reports (empty)
```

**Intentional Educational Samples (DO NOT REMOVE):**
- `template/.specify/specs/sample-feature/spec.md` - Teaches users spec format
- `template/.specify/deviations/sample-feature-001.md` - Teaches users deviation format
- `template/.elimination/logs/elimination_log.yaml` - Empty template structure

**Verify no unexpected files:**
```bash
# Should only show .gitkeep, sample-feature files, and elimination_log.yaml
find template/.elimination/active template/.elimination/archive \
     -type f ! -name '.gitkeep'
# Expected: empty output

# These are expected (educational samples):
ls template/.specify/specs/sample-feature/spec.md
ls template/.specify/deviations/sample-feature-001.md
ls template/.elimination/logs/elimination_log.yaml
```

### 4. Required Placeholders in template/CLAUDE.md

The template CLAUDE.md MUST contain these placeholders (not real values):

```
[PROJECT_NAME]        - Project name in header and overview
[PRIMARY_LANGUAGE]    - e.g., TypeScript, Python, Go
[MAIN_ENTRY]          - Main entry point symbol
[KEY_CLASS]           - Key class/module
[CONFIG]              - Configuration location
[path]                - File paths
[DATE]                - Dates in changelog
[SKILL_NAME]          - Skill placeholders
```

**Verification:**
```bash
# Should find multiple matches
grep -c '\[PROJECT_NAME\]\|\[PRIMARY_LANGUAGE\]\|\[DATE\]' template/CLAUDE.md
```

### 5. Required Structure in template/.serena/memories/

Memory files should have:
- **Structure/headings**: Preserved from root
- **Content**: Generic examples or empty sections, NOT real learnings

Example for `decision-log.md`:
```markdown
# Decision Log

## Decisions by Category

### Architecture
<!-- No decisions yet - add with /learn -->

### DEC-001: [Example Decision Title]
**Date**: [DATE]
**Context**: [What prompted this]
...
```

**NOT** actual decisions like "DEC-002: Dual-location architecture"

### 6. Sync Verification Checklist

After syncing, verify:

```bash
# 1. Commands synced (should match count)
ls template/.claude/commands/*.md | wc -l
ls .claude/commands/*.md | wc -l

# 2. CLAUDE.md has placeholders
grep '\[PROJECT_NAME\]' template/CLAUDE.md

# 3. Active directories are empty (except intentional samples)
find template/.elimination/active template/.elimination/archive -type f ! -name '.gitkeep' | wc -l  # Should be 0
# These should exist (educational samples):
test -f template/.specify/specs/sample-feature/spec.md && echo "sample spec exists"
test -f template/.specify/deviations/sample-feature-001.md && echo "sample deviation exists"

# 4. Memories don't have dev-specific content
grep -l 'DEC-002\|Dual-location\|2026-01-18' template/.serena/memories/  # Should be empty

# 5. Test installation works
# /install test-projects/minimal-js
```

---

## Pre-Release Checklist

Before releasing a new version:

- [ ] All command files tested and working
- [ ] `template/` synced from root
- [ ] `template/CLAUDE.md` has `[PLACEHOLDERS]` not real values
- [ ] `template/.serena/memories/` has clean examples
- [ ] `template/.elimination/active/` is empty
- [ ] `/install test-projects/minimal-js` works correctly
- [ ] CLAUDE.md, INSTALL.md, README.md are consistent
- [ ] Version numbers updated if applicable

---

## Directory Purposes

| Directory | Purpose | Who Modifies |
|-----------|---------|--------------|
| `.claude/commands/` | Working commands | Developer directly |
| `.serena/memories/` | Working memories | Developer or commands |
| `template/.claude/` | Distributable commands | Sync from root |
| `template/.serena/` | Distributable memories | Sync from root + cleanup |
| `test-projects/` | Installation targets | Temporary during testing |

---

## Making Template Changes

### Adding a New Command

1. Create `.claude/commands/new-command.md`
2. Test the command
3. Update CLAUDE.md "Quick Reference" section
4. Update README.md "Available Slash Commands" section
5. Sync to `template/`
6. Verify with `/install test-projects/minimal-js`

### Modifying Memory Structure

1. Edit files in `.serena/memories/` using Serena MCP tools:
   - `read_memory("memory-name")` - Read current content
   - `edit_memory("memory-name", needle, repl, mode)` - Edit with regex or literal
   - `write_memory("memory-name", content)` - Overwrite entire memory
2. Update CLAUDE.md "Current Memories" table
3. Sync to `template/` and ensure placeholders
4. Test `/learn` routing in test-projects/

**Note**: Prefer `edit_memory` over direct file editing when Serena MCP is active - it provides better atomic operations and error handling.

### Adding Elimination Patterns

1. Edit `.elimination/learned/heuristics.yaml` directly
2. Add examples to `.elimination/samples/`
3. Update `elimination_patterns.md` memory
4. Sync to `template/`

---

## Quick Reference

```bash
# === CATEGORY A: Safe to sync directly ===
rsync -av .claude/commands/ template/.claude/commands/
cp .claude/update-registry.yaml template/.claude/update-registry.yaml
rsync -av .elimination/config.yaml template/.elimination/
rsync -av .elimination/samples/ template/.elimination/samples/
rsync -av .elimination/learned/templates/ template/.elimination/learned/templates/
rsync -av .specify/config.yaml template/.specify/
rsync -av .specify/templates/ template/.specify/templates/

# === CATEGORY B: Manual review required ===
# Compare and selectively update (preserve placeholders):
diff CLAUDE.md template/CLAUDE.md
diff .serena/memories/decision-log.md template/.serena/memories/decision-log.md
# ... review each memory file

# === VERIFICATION ===
# Commands match?
ls template/.claude/commands/*.md | wc -l
ls .claude/commands/*.md | wc -l

# Placeholders preserved?
grep '\[PROJECT_NAME\]' template/CLAUDE.md

# No dev content leaked?
grep -l 'DEC-002\|Dual-location\|2026-01-18' template/.serena/memories/

# Active dirs empty? (except educational samples)
find template/.elimination/active template/.elimination/archive -type f ! -name '.gitkeep'
# Verify educational samples exist:
ls template/.specify/specs/sample-feature/spec.md template/.specify/deviations/sample-feature-001.md

# === TEST INSTALLATION ===
cd test-projects/minimal-js
# Ask Claude: "/install" from the claude-learns repo

# === RESET TEST PROJECT ===
rm -rf test-projects/minimal-js/.claude test-projects/minimal-js/.serena \
       test-projects/minimal-js/.elimination test-projects/minimal-js/.specify \
       test-projects/minimal-js/CLAUDE.md
```
