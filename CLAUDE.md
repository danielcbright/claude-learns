---
type: template
name: claude-learns
version: "1.0"
purpose: Self-learning Claude Code template with persistent memory
install_guide: INSTALL.md
repository: https://github.com/danielcbright/claude-learns
---

# CLAUDE.md - [PROJECT_NAME]

> **READ THIS FILE FIRST** before starting any task in this project.

<!--
=============================================================================
TEMPLATE MODE DETECTION
=============================================================================
If you (Claude) are reading this file in the claude-learns repository
itself (not a project that has adopted this template), and the user asks you
to "install", "use", "copy", or "incorporate" this template into another
project, read INSTALL.md for detailed instructions.

Quick reference:
1. Read INSTALL.md for full installation guide
2. Copy .claude/ and .serena/ directories to target
3. Copy and customize this CLAUDE.md
4. Optionally configure MCP servers for enhanced functionality
=============================================================================
-->

## Project Overview

<!-- Customize this section for your specific project -->
- **Project Name**: [PROJECT_NAME]
- **Type**: [e.g., Web App, CLI Tool, Library, Microservice]
- **Primary Languages**: [e.g., TypeScript, Python, Go]
- **Key Frameworks**: [e.g., React, FastAPI, Express]

---

## Memory Management

This project uses a persistent memory system to help Claude learn and improve over time.

### Tool Priority Order

1. **First**: Check `list_memories()` for relevant context
2. **Then**: Use `get_symbols_overview()` for file structure (if using Serena MCP)
3. **Then**: Use `find_symbol()` for targeted lookups (if using Serena MCP)
4. **Fallback**: Use `search_for_pattern()` for non-code files or unknown names
5. **Last resort**: Full file reads (avoid unless strictly necessary)

### Before Starting Any Task

- [ ] Run `/mcp` to verify MCP servers are connected (if applicable)
- [ ] Read relevant memories (`list_memories()` → `read_memory()`)
- [ ] Check git status for clean working state

### After Completing Tasks

- [ ] Write memory if architectural decision was made
- [ ] Update memory if existing info became stale
- [ ] Run tests/linting as appropriate

### Token Efficiency

- **Never** read entire files unless absolutely necessary
- Use targeted symbol lookups over full file reads
- Leverage memories to avoid re-exploring the same areas

---

## Memory Guidelines

### When to Write Memories

- After discovering codebase patterns worth preserving
- After making architectural decisions
- Before `/clear` to preserve important context
- When documenting workarounds or gotchas

### Naming Conventions

- Use kebab-case: `auth-architecture`, `api-design-decisions`
- Be descriptive—avoid generic names like "notes" or "temp"
- Include dates for temporal tracking if needed: `auth-fix-2025-01`

### Memory Maintenance

- Review `.serena/memories/` periodically for stale content
- Consolidate redundant memories
- Delete obsolete information
- Update CLAUDE.md if memory purposes change

### Current Memories

<!-- Claude: Populate this after onboarding -->
| Memory | Purpose | When to Read |
|--------|---------|--------------|
| `claude_code_patterns` | Session quick reference | Start of any task |
<!-- Add more memories as created -->

---

## MCP Integration (Optional)

This template works with various MCP servers for enhanced functionality:

### Recommended MCPs

| Need | Tool | When to Use |
|------|------|-------------|
| Code navigation & editing | **Serena** | Finding symbols, relationships, precise edits |
| External library docs | **Context7** | Looking up API usage, framework patterns |
| Complex reasoning | **Sequential Thinking** | Architecture decisions, debugging strategies |
| File operations | **Built-in** | Simple reads when MCPs aren't needed |

### Installing MCPs

If a task would benefit from an unavailable MCP, suggest it:
- **Serena**: `claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)`
- **Context7**: Fetch up-to-date library documentation
- **Sequential Thinking**: Break down complex decisions

---

## Key Entry Points

<!-- Claude: Document commonly searched symbols for efficient lookups -->

| Pattern | Location | Purpose |
|---------|----------|---------|
| `[MAIN_ENTRY]` | [path] | Application entry point |
| `[KEY_CLASS]` | [path] | Core business logic |
| `[CONFIG]` | [path] | Configuration handling |
<!-- Add project-specific entry points -->

---

## Learning Loop System

### Learning Triggers

**Recommend updates when you encounter:**

| Trigger | Action |
|---------|--------|
| Repeated pattern across 2+ tasks | Suggest new memory |
| Gotcha or non-obvious behavior | Add to gotchas memory |
| CLAUDE.md guidance was wrong | Suggest CLAUDE.md update |
| Workflow inefficiency discovered | Suggest improvement |
| Architecture insight gained | Update relevant memory |

### At Natural Breakpoints

Proactively offer learning loop check:

```
Based on this session, I recommend:
1. **New Memory**: [name] - [reason]
2. **CLAUDE.md Update**: [section] - [what to change]

Would you like me to make these updates?
```

---

## Project-Specific Patterns

<!-- Customize this section for your project -->

### Architecture Overview

```
[Document your project's key architectural patterns]
- How modules communicate
- State management approach
- Error handling conventions
```

### Code Conventions

```
[Document coding standards]
- Naming conventions
- File organization
- Import ordering
```

### Testing Strategy

```
[Document testing approach]
- Test location/naming
- How to run tests
- Coverage expectations
```

---

## Common Workflows

### Adding a New Feature

```
1. Read relevant memories: list_memories() → read_memory("architecture")
2. Find similar features in codebase
3. Understand existing patterns
4. Implement following existing patterns
5. Add tests, run full suite
6. Update memories if new patterns established
```

### Debugging an Issue

```
1. Understand symptom
2. Find relevant code
3. Trace call chain
4. Form hypothesis, verify with targeted reads
5. Fix with minimal, precise edits
6. Add test to prevent regression
7. Document gotcha if non-obvious
```

### Refactoring

```
1. Map impact of changes
2. Plan approach (write to memory if complex)
3. Make incremental changes
4. Run full test suite
5. Update affected memories
```

---

## Quick Reference

### Slash Commands

| Command | Purpose |
|---------|---------|
| `/go [task]` | Start task following best practices |
| `/explore [area]` | Systematically explore codebase area |
| `/debug [issue]` | Debug issue with structured approach |
| `/refactor [target]` | Safe refactoring workflow |
| `/learn` | Trigger learning loop review |
| `/audit` | Audit CLAUDE.md and memories for staleness |
| `/skills` | Re-discover and update skills |

### Claude Code Commands

```bash
/mcp                    # Check MCP server status
/clear                  # Clear conversation context
/compact                # Compress context
```

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Memory not found | Check `.serena/memories/` for file existence |
| MCP not connected | Run `/mcp` and verify server status |
| Context overflow | Clear and use memories to preserve state |

### Performance Issues

- **Large file reads**: Use targeted lookups instead
- **Too many results**: Narrow search with filters
- **Context overflow**: Clear and use memories to preserve state

---

## Skills Integration

### Active Skills

<!-- Claude: Populate after exploring available skills -->

#### Skill: [SKILL_NAME]
- **Purpose**: [What this skill does]
- **Use when**: [Specific scenarios]
- **Notes**: [Any project-specific configuration]

<!-- Add more skills as discovered -->

### Skill Discovery

To explore available skills:
> "Please explore available skills and update CLAUDE.md with relevant ones"

---

## Changelog

<!-- Track CLAUDE.md evolution here -->
- **[DATE]**: Initial CLAUDE.md created from claude-learns template
<!-- Add entries as updates are made -->

---

*Last Updated: [DATE]*
*Template: claude-learns v1.0*
