# Claude Code Instructions for claude-learns

## Project Overview
This is the **claude-learns template repository** - a framework for creating self-learning Claude Code projects with persistent memory. It uses a **dual-location architecture**: root files are for development/testing, `template/` contains clean distributable copies.

## Critical Workflows

### Installing Template to New Projects
1. Read `INSTALL.md` for complete installation guide
2. Copy from `template/` directory (not root-level files)
3. Customize `CLAUDE.md` with project-specific values
4. Configure MCP servers (Serena recommended for symbol navigation)

### Developing the Template Itself
- **Work in root files** (`.claude/`, `.serena/`, etc.) for development
- **Sync to `template/`** using categorized approach (see `DEVELOPMENT.md`)
- **Preserve placeholders** in `template/` (e.g., `[PROJECT_NAME]`, not real values)
- **Test installations** using `test-projects/minimal-{go,js,py}`

## Key Architectural Patterns

### Memory Management System
- **Tool Priority**: `list_memories()` → `read_memory()` → symbol lookups → file reads
- **MCP Integration**: Serena for code navigation, Context7 for external docs
- **Learning Loop**: Use `/claude-learns.learn` to capture insights and update memories

### Scientific Elimination Debugging
- Use `/claude-learns.eliminate [symptom]` for complex bugs with multiple causes
- Generate hypotheses, gather evidence, update confidence via Bayesian reasoning
- Integrate with specs via `/claude-learns.spec-debug [feature] [symptom]`

### Specification-Driven Development
- **Never claim done** without `/claude-learns.spec-verify [feature]` with concrete evidence
- Create specs first with `/claude-learns.spec-create`, validate with `/claude-learns.spec-validate`
- Log corrections with `/claude-learns.spec-correction` when claims were premature

## Project-Specific Conventions

### File Structure
```
.claude/commands/     # Slash commands (working copies)
.serena/memories/     # Persistent learnings (working copies)
.elimination/         # Debugging system (working copies)
.specify/            # Spec-driven development (working copies)
template/            # Distributable clean copies
test-projects/       # Installation test targets
```

### Command Patterns
- `/claude-learns.go [task]` - Start with best practices
- `/claude-learns.debug` vs `/claude-learns.eliminate` - Use elimination for multi-cause issues
- `/claude-learns.spec-*` commands - For feature development workflow
- `/claude-learns.learn` - Capture insights after tasks

### Code Editing
- Prefer Serena MCP tools: `find_symbol()`, `replace_symbol_body()`, `edit_memory()`
- Use targeted symbol operations over full file reads
- Preserve whitespace and indentation exactly in edits

## Integration Points

### MCP Servers
- **Serena**: Code navigation (`get_symbols_overview()`, `find_symbol()`)
- **Context7**: External library documentation
- **Sequential Thinking**: Complex architectural decisions

### External Dependencies
- Works with any language/framework (test projects: Go, JS, Python)
- Git integration for `/update` command safety
- No specific build tools required

## Common Pitfalls

- **Don't modify `template/` directly** - sync from root with placeholders
- **Don't claim completion** without `/claude-learns.spec-verify` evidence
- **Don't rsync blindly** - follow Category A/B/C sync procedures in `DEVELOPMENT.md`
- **Don't leak dev content** to template (no real project names/dates)

## Quick Reference
- **Entry Points**: `CLAUDE.md` (read first), `INSTALL.md`, `DEVELOPMENT.md`
- **Key Memories**: `claude_code_patterns.md`, `elimination_patterns.md`
- **Test Installation**: `/claude-learns.install test-projects/minimal-js`