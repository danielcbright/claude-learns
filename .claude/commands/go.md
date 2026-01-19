Always follow these practices for this task:

## Step 0: Verify Working Location

Before modifying code, verify you're in the correct project directory.

```
Location Verification:
- [ ] Check: pwd && git branch --show-current
- [ ] Confirm: Is this the correct project/branch for this task?
- [ ] If uncertain (<95% confidence): ASK user before proceeding
```

**If uncertain, ask:**
> "Current location: [path], branch: [branch]. Should I work here or switch to a different location?"

## Step 0.5: Task Analysis

**Analyze the task type and suggest the appropriate workflow:**

### If NEW FEATURE:
```
For non-trivial features, consider starting with:
/claude-learns.spec-create [feature-name]

This creates a specification with acceptance criteria before implementation,
enabling proper verification with /claude-learns.spec-verify when done.
```

### If DEBUGGING / FIXING A BUG:
```
For bugs, use the dedicated debugging workflows:
/debug [issue]      - Systematic debugging with memory consultation
/claude-learns.eliminate [issue]  - Scientific elimination for complex/intermittent bugs

These check past debugging lessons and known bug patterns first.
```

### If EXPLORING UNFAMILIAR CODE:
```
For unfamiliar areas, start with exploration:
/explore [area]

This systematically maps the codebase area before making changes,
reducing risk of unintended side effects.
```

### If REFACTORING:
```
For refactoring, use the safe refactoring workflow:
/refactor [target]

This maps impact, makes incremental changes, and verifies with tests.
```

---

## Tool Usage
- Use **Serena** for all code navigation and editing (find_symbol, find_referencing_symbols, get_symbols_overview, replace_symbol_body)
- Use **Context7** for external library/framework documentation lookups
- Use **Sequential Thinking** for complex architectural decisions or debugging strategies
- Check `/mcp` if tools seem unavailable and suggest enabling them

## Before Starting
1. Read the CLAUDE.md file in the project root
2. Check `list_memories()` and read relevant project memories
3. Use `get_symbols_overview()` to understand affected areas

## During Work
- Navigate code semantically (find_symbol) not by reading entire files
- Edit with precision (replace_symbol_body, insert_after_symbol) not full file rewrites
- Trace relationships (find_referencing_symbols) before modifying shared code

## After Changes
- Run tests and linting
- Check `git diff` to verify changes
- Update memories if new patterns were established
- For features with specs: Run `/claude-learns.spec-verify` before claiming done

---

Now proceed with: $ARGUMENTS
