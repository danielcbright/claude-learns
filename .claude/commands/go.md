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

---

Now proceed with: $ARGUMENTS
