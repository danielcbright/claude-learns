---
type: serena-memory
name: claude_code_patterns
purpose: Session quick reference for Claude Code + Serena integration
read_at: session-start
customize: true
---

# Claude Code Integration Patterns

> This memory helps Claude Code work effectively with this project using Serena.
> Read this at session start. Keep it current with architectural changes.

## Tool Priority Reminder

1. Check memories first (`list_memories()`)
2. Use `get_symbols_overview()` before reading files
3. Use `find_symbol()` for targeted lookups
4. Use `search_for_pattern()` for non-code/unknown names
5. Full file reads only when necessary

## MCP Tools Available

### Serena (Primary for Code Navigation)
- **Status**: Connected via `--context claude-code --project [path]`
- **Use for**: All symbol lookup, code relationships, precise edits
- **Skip when**: Simple config files, documentation

### Other Recommended MCPs
<!-- Update based on what's configured -->
- Context7: For looking up external library APIs
- Sequential Thinking: For architectural decisions

## Code Navigation Patterns

### Finding Code
```
find_symbol("AuthService")                    # Find any symbol
find_symbol("AuthService/validateToken")      # Find nested member
find_symbol("Component", depth=1)             # Get immediate children
```

### Understanding Relationships
```
find_referencing_symbols("validateToken")     # Who uses this?
get_symbols_overview("src/services/auth.ts")  # What's in this file?
```

### Making Changes
```
rename_symbol("oldName", "newName")           # Rename everywhere
replace_symbol_body("Service/method", code)   # Replace implementation
insert_after_symbol("existingFunc", code)     # Add after existing
```

## Project-Specific Commands

### Testing
```bash
# Run all tests
[PROJECT_TEST_COMMAND]

# Run specific test
[PROJECT_TEST_SINGLE_COMMAND]
```

### Linting
```bash
[PROJECT_LINT_COMMAND]
```

### Building
```bash
[PROJECT_BUILD_COMMAND]
```

## Key Entry Points

<!-- Document commonly searched symbols here -->
| Symbol | Location | Purpose |
|--------|----------|---------|
| `[MainEntry]` | [path] | Application entry |
| `[CoreService]` | [path] | Business logic |

## Common Gotchas

<!-- Add project-specific issues Claude should know about -->
- [Document any non-obvious behaviors or edge cases]
- [Include workarounds for known issues]
- [Note any dependencies or setup requirements]

## Architecture Quick Reference

### Module Structure
```
[Describe key modules and their responsibilities]
- src/          → Main source code
- tests/        → Test files
- config/       → Configuration files
```

### Data Flow
```
[Describe how data moves through the system]
Input → Processing → Storage → Output
```

### Key Abstractions
```
[List important base classes, interfaces, patterns]
- Service pattern for business logic
- Repository pattern for data access
- Factory pattern for object creation
```
