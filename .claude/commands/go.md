Always follow these practices for this task:

## Step 0: MCP & Environment Check

**BEFORE doing anything else, verify your tools are available.**

```
Environment Verification:
- [ ] Run /mcp to check MCP server status
- [ ] Confirm Serena is connected (if not, suggest installing it)
- [ ] Check: pwd && git branch --show-current
- [ ] Confirm: Is this the correct project/branch for this task?
```

If Serena is NOT connected and the task involves code:
```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)
```

**If uncertain about location, ask:**
> "Current location: [path], branch: [branch]. Should I work here or switch?"

---

## Step 1: Read Context

**MUST read memories before exploring code.**

```python
# Check available memories
list_memories()

# Read essential memories for this task type
read_memory("claude_code_patterns")     # Always
read_memory("serena-tools-reference")   # If unsure about tools
read_memory("debugging-lessons")        # If debugging
read_memory("decision-log")             # If architectural changes
```

---

## Step 2: Task Analysis

**Analyze the task and suggest the appropriate workflow:**

### NEW FEATURE:
```
Consider starting with:
/claude-learns.spec-create [feature-name]

Creates specification with acceptance criteria.
Enables verification with /claude-learns.spec-verify when done.
```

### DEBUGGING / FIXING A BUG:
```
Use dedicated debugging workflows:
/debug [issue]                    - Systematic debugging
/claude-learns.eliminate [issue]  - Scientific elimination for complex bugs

These check past debugging lessons first.
```

### EXPLORING UNFAMILIAR CODE:
```
Start with exploration:
/explore [area]

Maps the codebase area before making changes.
```

### REFACTORING:
```
Use safe refactoring workflow:
/refactor [target]

Maps impact, makes incremental changes, verifies with tests.
```

---

## Step 3: Tool Usage Rules

**YOU MUST follow these rules. Serena provides semantic understanding; built-in tools see text.**

### Decision Tree

```
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

### Tool Priority Order

1. **Memories first** → `list_memories()` then `read_memory(name)`
2. **Understand structure** → `get_symbols_overview(path)`
3. **Find specific code** → `find_symbol(pattern)`
4. **Find relationships** → `find_referencing_symbols(name, path)`
5. **Pattern search** → `search_for_pattern(regex)` (fallback)
6. **File reads** → `read_file(path)` (last resort, non-code only)

### Other MCPs

- **Context7**: For external library/framework documentation
- **Sequential Thinking**: For complex architectural decisions

For detailed tool docs: `read_memory("serena-tools-reference")`

---

## Step 4: Execute Task

**During work:**
- Navigate code semantically (`find_symbol`) not by reading entire files
- Edit with precision (`replace_symbol_body`, `insert_after_symbol`)
- Trace relationships (`find_referencing_symbols`) before modifying shared code
- Keep edits minimal and focused

---

## Step 5: Verify & Complete

**After changes:**
- [ ] Run tests and linting
- [ ] Check `git diff` to verify changes are correct
- [ ] Update memories if new patterns were established
- [ ] For features with specs: Run `/claude-learns.spec-verify` before claiming done

**IMPORTANT: Evidence must be concrete, not assumptions.**
- ✅ "Test output: PASS - 15 assertions"
- ❌ "I believe this works"

---

Now proceed with: $ARGUMENTS
