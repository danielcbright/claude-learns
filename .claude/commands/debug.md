Debug this issue systematically using available tools:

## Step 0: Check Past Knowledge

**Before diving in, check what we already know:**

### Read Debugging Lessons
```
read_memory("debugging-lessons") or read .serena/memories/debugging-lessons.md
```
Look for:
- Similar symptoms we've seen before
- Non-obvious root causes for this type of issue
- Approaches that worked (or didn't)

### Check Common Bugs for This Area
```
read_memory("common-bugs") or read .serena/memories/common-bugs.md
```
Scan for:
- Known bug patterns in the affected feature area
- Recurring issues that match this symptom
- Previously identified root causes

### Complexity Check

**Consider `/claude-learns.eliminate` immediately if:**
- Issue is **intermittent** or timing-dependent
- **Multiple systems** could be involved
- Symptom is **vague** ("sometimes it doesn't work")
- You've seen this pattern fail simple debugging before

```
/claude-learns.eliminate [symptom description]
```

---

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
This debugging session would benefit from Sequential Thinking MCP
for structured hypothesis testing. Enable via:
claude mcp add sequential-thinking -- npx -y @anthropic/mcp-sequential-thinking
```

### Escalate to /eliminate

Consider switching to `/claude-learns.eliminate` (scientific elimination debugging) when:
- **Multiple possible causes exist** and you can't narrow down quickly
- **Initial debugging hasn't found root cause** after 10-15 minutes
- **Issue is intermittent** or timing-dependent
- **You need to track hypotheses** systematically with confidence scores

```
/claude-learns.eliminate [symptom description]
```

This uses Bayesian reasoning to systematically eliminate hypotheses until
only the true cause remains. Especially useful for race conditions,
intermittent failures, and complex multi-system issues.

### 5. Verify & Fix
- Make minimal, targeted fix using `replace_symbol_body()` or similar
- Add test case that reproduces the issue
- Verify fix with test run

### 6. Document & Learn
If this reveals a common pitfall:
```
write_memory("debugging_[issue_type]", lessons_learned)
```

Consider running `/claude-learns.learn` to route insights to the appropriate memory.

---

Issue to debug: $ARGUMENTS
