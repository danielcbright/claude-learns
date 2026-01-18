Perform a safe refactoring operation using Serena's semantic tools:

## Pre-Refactor Checklist

0. **Verify Worktree**
   - Run `pwd && git branch --show-current`
   - If not in correct worktree for this task, ASK user before proceeding
   - Never refactor in main repo if changes should go to feature branch

1. **Map Impact**
   - Use `find_referencing_symbols()` to find ALL usages
   - Use `find_symbol(depth=2)` to understand the full structure
   - Document the scope of changes needed

2. **Verify Clean State**
   - Check `git status` - should be clean
   - Run existing tests - should pass
   - Run linting - should pass

3. **Plan the Change**
   - List all symbols that need modification
   - Identify the order of changes (dependencies first)
   - Note any test files that need updates

## Refactoring Execution

Use the right Serena tool for each operation:
- **Renaming**: `rename_symbol("old", "new")` - handles all references automatically
- **Moving code**: `replace_symbol_body()` + `insert_after_symbol()`
- **Signature changes**: Update implementation, then update all call sites found via `find_referencing_symbols()`

## Post-Refactor Validation

1. Run full test suite
2. Run linting
3. Review `git diff` for unexpected changes
4. Verify no broken references with targeted `find_referencing_symbols()` calls
5. **If binaries needed**: Rebuild from same worktree

## Memory Update

If this establishes new patterns, save to memory:
```
write_memory("refactoring_[date]", summary_of_changes)
```

---

Refactoring task: $ARGUMENTS
