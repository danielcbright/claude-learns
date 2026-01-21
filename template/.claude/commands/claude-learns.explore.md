Explore this codebase area systematically using Serena:

## Exploration Strategy

1. **Start broad** - Use `get_symbols_overview()` on the target directory/file
2. **Map relationships** - Use `find_referencing_symbols()` on key symbols
3. **Understand depth** - Use `find_symbol(depth=1, include_body=False)` for structure
4. **Deep dive selectively** - Only use `include_body=True` for specific symbols of interest

## Output Format

Provide a structured summary:
- **Key Components**: Main classes/functions and their purposes
- **Relationships**: How components interact (who calls what)
- **Patterns**: Notable architectural patterns observed
- **Entry Points**: Where external code interfaces with this area

## Save Findings

If significant patterns are discovered, offer to save them:
```
write_memory("area_name_patterns", summary)
```

---

Area to explore: $ARGUMENTS
