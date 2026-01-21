---
type: template
name: claude-learns
version: "1.1"
purpose: Self-learning Claude Code template with persistent memory
install_guide: INSTALL.md
repository: https://github.com/danielcbright/claude-learns
---

# CLAUDE.md - [PROJECT_NAME]

<!--
TEMPLATE MODE: You are in the claude-learns REPOSITORY.
- To INSTALL this template: Read INSTALL.md
- To DEVELOP this template: Read DEVELOPMENT.md
-->

## Project Overview

- **Project Name**: [PROJECT_NAME]
- **Type**: [e.g., Web App, CLI Tool, Library]
- **Languages**: [e.g., TypeScript, Python]
- **Frameworks**: [e.g., React, FastAPI]

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
- [ ] Run tests
- [ ] For features with specs: Run `/claude-learns.spec-verify`

---

## Quick Reference

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/go [task]` | Start task with best practices |
| `/explore [area]` | Systematically explore code area |
| `/debug [issue]` | Structured debugging |
| `/claude-learns.eliminate [symptom]` | Scientific debugging for complex bugs |
| `/claude-learns.spec-create [name]` | Create feature specification |
| `/claude-learns.spec-verify [name]` | Verify before claiming done |
| `/claude-learns.learn` | Trigger learning loop |

### Completion Standards

**IMPORTANT: YOU MUST run `/claude-learns.spec-verify` before claiming done.**

Evidence must be concrete:
- ✅ "Test output: PASS - 15 assertions"
- ✅ "curl returned 200 with expected body"
- ❌ "I believe this works"
- ❌ "Should be fine"

---

## Project-Specific Patterns

### Architecture
<!-- Document key patterns, data flow, module responsibilities -->

### Code Conventions
<!-- Naming, imports, file organization, style rules -->

### Testing
<!-- How to run tests, coverage expectations -->

### Key Entry Points
| Symbol | Location | Purpose |
|--------|----------|---------|
| [MAIN_ENTRY] | [path] | Application entry |
| [KEY_CLASS] | [path] | Core logic |

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

*Last Updated: [DATE]*
*Template: claude-learns v1.1*
