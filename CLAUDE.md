---
type: template
name: claude-learns
version: "1.1"
purpose: Self-learning Claude Code template with persistent memory
install_guide: INSTALL.md
repository: https://github.com/danielcbright/claude-learns
---

# CLAUDE.md - claude-learns

<!--
TEMPLATE MODE: You are in the claude-learns REPOSITORY (the template source).
- To INSTALL this template into another project: Read INSTALL.md
- To DEVELOP this template: Read DEVELOPMENT.md
  - Root files are working copies for development
  - template/ contains distribution files with [PLACEHOLDERS]
  - NEVER rsync blindly - follow sync procedures in DEVELOPMENT.md
-->

## Project Overview

- **Project Name**: claude-learns
- **Type**: Claude Code Template / Framework
- **Languages**: Python (scripts), Markdown (documentation, commands)
- **Purpose**: Self-learning template that helps Claude Code improve over time

---

## CRITICAL: Tool Usage Rules

**YOU MUST follow these rules for ALL code operations.**

### Decision Tree: How to Work with Code

```
┌─────────────────────────────────────────────────────────────────┐
│ BEFORE touching any code, ask: "Is Serena MCP connected?"       │
│                                                                 │
│ YES → Use Serena for EVERYTHING below                           │
│ NO  → Run /mcp, suggest installing Serena, use built-in tools   │
└─────────────────────────────────────────────────────────────────┘

READING CODE:
  Need to understand a file?
    → FIRST: get_symbols_overview(path)
    → THEN: find_symbol(name, include_body=True) for specific parts
    → NEVER: Read entire files unless non-code (config, docs)

  Need to find a function/class?
    → MUST USE: find_symbol("ClassName") or find_symbol("ClassName/method")
    → NOT: grep, search, or reading files hoping to find it

  Need to find who calls something?
    → MUST USE: find_referencing_symbols(name, path)
    → NOT: grep for the function name

EDITING CODE:
  Replacing a function/method body?
    → MUST USE: replace_symbol_body(name_path, file, new_body)
    → NEVER: Full file rewrites or Edit tool on code files

  Adding new code after existing?
    → MUST USE: insert_after_symbol(name_path, file, code)

  Adding imports or code before something?
    → MUST USE: insert_before_symbol(name_path, file, code)

  Renaming across codebase?
    → MUST USE: rename_symbol(name_path, file, new_name)

  Editing non-code files (config, docs)?
    → USE: replace_content(path, needle, replacement, mode)

SEARCHING:
  Looking for patterns in code?
    → USE: search_for_pattern(regex, relative_path="src/")
    → NOT: grep or bash find commands
```

### Why This Matters

Serena provides **semantic understanding**. Built-in tools see **text**.
- `find_symbol("AuthService/validate")` knows it's a method
- `grep "validate"` finds every occurrence of the string

Semantic tools = fewer tokens, better accuracy, precise edits.

### Tool Priority Order

1. **First**: Check memories → `list_memories()` then `read_memory(name)`
2. **Then**: Understand structure → `get_symbols_overview(path)`
3. **Then**: Find specific code → `find_symbol(pattern)`
4. **Then**: Find relationships → `find_referencing_symbols(name, path)`
5. **Fallback**: Pattern search → `search_for_pattern(regex)`
6. **Last resort**: File reads → `read_file(path)` (non-code only)

### Installing Serena

If Serena is not connected:
```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)
```

For detailed tool documentation: `read_memory("serena-tools-reference")`

---

## Memory System

Memories persist across sessions. **Always check memories before exploring code.**

### Core Memories

| Memory | Purpose | When to Read |
|--------|---------|--------------|
| `claude_code_patterns` | Quick reference for this project | Session start |
| `serena-tools-reference` | Full Serena tool documentation | When unsure about tool usage |
| `elimination_patterns` | Elimination debugging patterns | Before `/claude-learns.eliminate` |
| `debugging-lessons` | Past bugs and solutions | Before debugging |
| `decision-log` | Architectural decisions | Before major changes |

### Memory Commands

```python
list_memories()                    # See all memories
read_memory("name")                # Read a memory
write_memory("name", content)      # Create/overwrite
edit_memory("name", old, new, mode)  # Edit in place
```

### When to Write Memories

- After discovering patterns worth preserving
- After architectural decisions
- Before `/clear` to preserve context
- When documenting gotchas

---

## Before Starting Any Task

- [ ] Run `/mcp` to verify Serena is connected
- [ ] Read relevant memories
- [ ] Check git status

## After Completing Tasks

- [ ] Write/update memories if new patterns emerged
- [ ] Run tests (if applicable)
- [ ] For features with specs: Run `/claude-learns.spec-verify`

---

## Quick Reference

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/claude-learns.go [task]` | Start task with best practices |
| `/claude-learns.explore [area]` | Systematically explore code area |
| `/claude-learns.debug [issue]` | Structured debugging |
| `/claude-learns.eliminate [symptom]` | Scientific debugging for complex bugs |
| `/claude-learns.spec-create [name]` | Create feature specification |
| `/claude-learns.spec-verify [name]` | Verify before claiming done |
| `/claude-learns.learn` | Trigger learning loop |
| `/claude-learns.ralph [task]` | Start autonomous ralph-loop with learning |
| `/claude-learns.ralph-status` | Check ralph session status |
| `/claude-learns.install [path]` | Install template to target project |
| `/claude-learns.update [tool]` | Update tools with git safety |
| `/claude-learns.optimize [area]` | Analyze and optimize for context efficiency |
| `/claude-learns.audit` | Check accuracy and completeness |

### Completion Standards

**IMPORTANT: YOU MUST run `/claude-learns.spec-verify` before claiming done.**

Evidence must be concrete:
- ✅ "Test output: PASS - 15 assertions"
- ✅ "curl returned 200 with expected body"
- ❌ "I believe this works"
- ❌ "Should be fine"

---

## Ralph Loop Mode (Autonomous Iteration)

Ralph-loop enables autonomous development - Claude works on a task iteratively until completion.

### When to Use Ralph

| Use Ralph | Don't Use Ralph |
|-----------|-----------------|
| Well-defined features with specs | Debugging (use `/claude-learns.eliminate`) |
| Test-driven development | Exploratory work |
| Batch operations | Design decisions |
| Greenfield with clear criteria | Unclear success criteria |

### Ralph + Claude-Learns Integration

```
/claude-learns.ralph "task" --spec feature-name --max-iterations 30
```

Each iteration:
1. **READ** - Serena memories first (survives /clear)
2. **WORK** - Follow CLAUDE.md tool rules
3. **LEARN** - Write insights to memories
4. **COMMIT** - Git commit with summary

If stuck (same error 3x):
- Auto-switches to `/claude-learns.eliminate`
- Elimination finds root cause
- Resumes ralph after fix

### Key Commands

| Command | Purpose |
|---------|---------|
| `/claude-learns.ralph [task]` | Start ralph with claude-learns integration |
| `/claude-learns.ralph-status` | Check session status |
| `/cancel-ralph` | Stop the loop |

For detailed guide: See `RALPH.md`

---

## Project-Specific Patterns

### Architecture

This is a **template repository** with dual-location architecture:

```
claude-learns/
├── CLAUDE.md              # Working copy (this file) - for development
├── template/              # Distribution files - for installation
│   ├── CLAUDE.md          # Template with [PLACEHOLDERS]
│   ├── .claude/           # Commands and skills
│   ├── .serena/           # Memory system
│   ├── .elimination/      # Debugging system
│   └── .specify/          # Spec system
├── .claude/               # Working commands (dev)
├── .serena/               # Working memories (dev)
└── DEVELOPMENT.md         # Sync procedures
```

### Key Rules

1. **NEVER rsync blindly** - Root → template/ requires placeholder restoration
2. **template/ keeps [PLACEHOLDERS]** - Never commit real values there
3. **Test installations** in `test-projects/` not in template/
4. **Read DEVELOPMENT.md** before modifying template sync

### Code Conventions

- Python scripts: PEP 8, type hints
- Markdown: GitHub-flavored, keep lines under 100 chars
- YAML: 2-space indent, explicit quotes for strings
- Commands: Markdown instructions, not executable code

### Key Entry Points

| Symbol | Location | Purpose |
|--------|----------|---------|
| `/claude-learns.install` | `.claude/commands/install.md` | Template installation |
| `/claude-learns.learn` | `.claude/commands/learn.md` | Learning loop |
| `/claude-learns.go` | `.claude/skills/go.md` | Task starter |

---

## Extended Documentation

For detailed information, read the appropriate memory:

| Topic | Memory |
|-------|--------|
| Serena tools | `serena-tools-reference` |
| Debugging patterns | `elimination_patterns` |
| Past decisions | `decision-log` |
| Known bugs | `common-bugs` |

For system documentation:
- Spec-driven development: `.specify/README.md`
- Elimination debugging: `.elimination/README.md`
- Skills system: `.claude/skills/README.md`
- Template development: `DEVELOPMENT.md`
- Installation guide: `INSTALL.md`

---

## Learning Loop

At natural breakpoints, proactively offer:

```
Based on this session, I recommend:
1. **New Memory**: [name] - [reason]
2. **CLAUDE.md Update**: [section] - [change]

Would you like me to make these updates?
```

---

*Last Updated: 2026-01-21*
*Template: claude-learns v1.1*
