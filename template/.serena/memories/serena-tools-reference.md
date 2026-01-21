---
type: serena-memory
name: serena-tools-reference
purpose: Complete Serena MCP tools reference documentation
read_at: when-needed
customize: false
---

# Serena MCP Tools Reference

> **Read this memory when you need detailed tool documentation.**
> For quick decisions, use the decision tree in CLAUDE.md instead.

## Project Activation

Before using any Serena tools, activate the project:
```python
activate_project("/path/to/project")
```

Check if onboarding is needed:
```python
check_onboarding_performed()
```

---

## Memory Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `list_memories()` | See available memories | Returns list of memory names |
| `read_memory("name")` | Read memory content | `read_memory("decision-log")` |
| `write_memory("name", content)` | Create/overwrite memory | `write_memory("new-feature", "# Notes\n...")` |
| `edit_memory("name", needle, repl, mode)` | Edit existing memory | See below |
| `delete_memory("name")` | Remove memory | Only on user request |

**Editing memories** (preferred over overwriting):
```python
# Literal replacement
edit_memory("decision-log",
    needle="*Total Decisions: 1*",
    repl="*Total Decisions: 2*",
    mode="literal")

# Regex replacement (for complex edits)
edit_memory("decision-log",
    needle="### DEC-001:.*?Review Date\\*\\*: [^\\n]+",
    repl="### DEC-001: ... (new content)",
    mode="regex")
```

---

## Code Navigation Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `get_symbols_overview(path)` | File structure overview | `get_symbols_overview("src/auth.ts")` |
| `find_symbol(pattern)` | Find symbol by name | `find_symbol("AuthService")` |
| `find_symbol(pattern, depth=1)` | Include children | `find_symbol("AuthService", depth=1)` |
| `find_symbol(pattern, include_body=True)` | Get implementation | Full source code |
| `find_referencing_symbols(name, path)` | Who uses this? | `find_referencing_symbols("validateToken", "src/auth.ts")` |

### Name Path Patterns

```python
find_symbol("method")              # Any symbol named "method"
find_symbol("Class/method")        # Method within Class
find_symbol("/Class/method")       # Exact path (absolute)
find_symbol("Class/method[0]")     # First overload (for languages with overloading)
```

### Common Navigation Patterns

```python
# Find a class and see its methods
find_symbol("AuthService", depth=1)

# Get the full implementation of a specific method
find_symbol("AuthService/validateToken", include_body=True)

# Find all callers of a function
find_referencing_symbols("validateToken", "src/auth.ts")

# Explore a file's structure before diving in
get_symbols_overview("src/services/auth.ts")
```

---

## Code Editing Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `replace_symbol_body(name_path, relative_path, body)` | Replace implementation | Entire function/class |
| `insert_after_symbol(name_path, relative_path, body)` | Add after symbol | New method after existing |
| `insert_before_symbol(name_path, relative_path, body)` | Add before symbol | Import before first symbol |
| `rename_symbol(name_path, relative_path, new_name)` | Rename everywhere | Refactor across codebase |

### Examples

**Replace a method:**
```python
replace_symbol_body(
    name_path="AuthService/validateToken",
    relative_path="src/auth.ts",
    body="async validateToken(token: string): Promise<boolean> {\n  // new implementation\n}"
)
```

**Add a new method after an existing one:**
```python
insert_after_symbol(
    name_path="AuthService/validateToken",
    relative_path="src/auth.ts",
    body="\n\nasync refreshToken(token: string): Promise<string> {\n  // implementation\n}"
)
```

**Add imports at the top of a file:**
```python
# Find first symbol, then insert before it
insert_before_symbol(
    name_path="AuthService",  # First class/function in file
    relative_path="src/auth.ts",
    body="import { Logger } from './logger';\n\n"
)
```

**Rename across codebase:**
```python
rename_symbol(
    name_path="validateToken",
    relative_path="src/auth.ts",
    new_name="verifyToken"
)
```

---

## Search Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `search_for_pattern(pattern)` | Regex search in files | `search_for_pattern("TODO.*auth")` |
| `search_for_pattern(pattern, relative_path="src/")` | Scoped search | Only in src/ |
| `search_for_pattern(pattern, restrict_search_to_code_files=True)` | Code only | Skip config/docs |

### Search Parameters

```python
search_for_pattern(
    substring_pattern="TODO.*",           # Regex pattern
    relative_path="src/",                 # Scope to directory
    restrict_search_to_code_files=True,   # Only code files
    context_lines_before=2,               # Lines before match
    context_lines_after=2,                # Lines after match
    paths_include_glob="*.ts",            # Only .ts files
    paths_exclude_glob="*test*"           # Exclude tests
)
```

---

## File Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `read_file(path)` | Read file content | Non-code files, config, docs |
| `create_text_file(path, content)` | Create new file | New modules |
| `replace_content(path, needle, repl, mode)` | Edit file content | Non-symbol edits, config files |
| `list_dir(path, recursive)` | List directory | Exploring structure |
| `find_file(mask, path)` | Find files by pattern | `find_file("*.test.ts", ".")` |

### replace_content Examples

```python
# Literal replacement
replace_content(
    relative_path="config.yaml",
    needle="debug: false",
    repl="debug: true",
    mode="literal"
)

# Regex replacement (use $!1, $!2 for backreferences)
replace_content(
    relative_path="package.json",
    needle='"version": "([0-9.]+)"',
    repl='"version": "2.0.0"',
    mode="regex"
)

# Replace multiple occurrences
replace_content(
    relative_path="src/config.ts",
    needle="localhost",
    repl="production.example.com",
    mode="literal",
    allow_multiple_occurrences=True
)
```

---

## Shell Commands

```python
execute_shell_command(
    command="npm test",
    cwd=".",                    # Working directory (default: project root)
    capture_stderr=True         # Include stderr in output
)
```

**Safe commands only!** Never execute commands that:
- Require user interaction
- Run indefinitely (servers, watch modes)
- Could be destructive without confirmation

---

## Tool Selection Quick Reference

```
Need to...                          → Use this tool
────────────────────────────────────────────────────
Read/write project knowledge        → Memory tools
Find a class/function               → find_symbol()
See what's in a file                → get_symbols_overview()
Find who calls a function           → find_referencing_symbols()
Replace a function body             → replace_symbol_body()
Add new code after existing         → insert_after_symbol()
Rename across codebase              → rename_symbol()
Search for text patterns            → search_for_pattern()
Edit non-code files                 → replace_content()
Read config/docs                    → read_file()
Create new files                    → create_text_file()
Run tests/build                     → execute_shell_command()
```

---

## When NOT to Use Serena

Use built-in Claude Code tools instead when:
- **Simple one-off file reads** → Built-in Read tool is faster
- **Files Serena can't parse** → Use built-in tools
- **Quick directory listing** → Built-in LS may suffice
- **Binary files** → Serena is for text/code only

---

## Supported Languages

Serena supports 30+ languages via Language Server Protocol:
AL, Bash, C#, C/C++, Clojure, Dart, Elixir, Elm, Erlang, Fortran, Go, Haskell,
Java, JavaScript, Julia, Kotlin, Lua, Markdown, MATLAB, Nix, Perl, PHP,
PowerShell, Python, R, Ruby, Rust, Scala, Swift, TOML, TypeScript, YAML, Zig

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No active project" | Run `activate_project("project-name")` |
| Symbol not found | Check spelling, try `search_for_pattern()` first |
| Edit failed | Verify symbol exists with `find_symbol()` first |
| MCP not responding | Check `/mcp` status, restart if needed |
