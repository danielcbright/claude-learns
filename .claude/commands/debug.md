Debug this issue systematically using available tools:

## Tool Selection

- **Serena**: For tracing code paths and understanding symbol relationships
- **Sequential Thinking MCP**: For complex root cause analysis (suggest enabling if not available)
- **Built-in**: For reading logs, running tests, checking outputs

## Debugging Workflow

### 1. Understand the Symptom
- What is the expected behavior?
- What is the actual behavior?
- When did it start happening?

### 2. Locate Relevant Code
```
# Find the main component involved
find_symbol("ComponentName")

# Trace the call chain
find_referencing_symbols("suspectedFunction")

# Search for error patterns
search_for_pattern("error message text", [".ts", ".py"])
```

### 3. Trace Execution Path
Use `find_referencing_symbols()` to build the call graph:
```
Entry Point → Handler → Service → Repository → [Issue Location]
```

### 4. Form Hypothesis
Based on code analysis, hypothesize the root cause.

If the issue is complex, consider using Sequential Thinking MCP:
```
💡 This debugging session would benefit from Sequential Thinking MCP 
   for structured hypothesis testing. Enable via:
   claude mcp add sequential-thinking -- npx -y @anthropic/mcp-sequential-thinking
```

### 5. Verify & Fix
- Make minimal, targeted fix using `replace_symbol_body()` or similar
- Add test case that reproduces the issue
- Verify fix with test run

### 6. Document
If this reveals a common pitfall, save to memory:
```
write_memory("debugging_[issue_type]", lessons_learned)
```

---

Issue to debug: $ARGUMENTS
