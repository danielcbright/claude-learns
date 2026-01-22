Start a ralph-loop with claude-learns best practices.

Ralph-loop creates autonomous iteration loops. Claude-learns adds:
- Memory persistence (survives /clear)
- Learning each iteration (patterns captured)
- Serena tool enforcement
- Elimination integration (auto-debug when stuck)

---

## Step 1: Parse Arguments

Parse the user's request: $ARGUMENTS

Extract:
- **task**: What to build (required)
- **spec**: Spec name if mentioned (optional, e.g., "--spec user-auth")
- **max-iterations**: Safety limit (default: 30)
- **stuck-threshold**: Failures before elimination (default: 3)

---

## Step 2: Initialize Session Memory

Create a session memory to persist context across /clear:

```python
# Generate session memory name from task
session_name = "ralph-session-" + task_slug  # e.g., "ralph-session-user-auth"

# Read template
read_memory("ralph-session-template")

# Create session memory with initial context
write_memory(session_name, """---
type: serena-memory
name: {session_name}
purpose: Track ralph session for {task}
read_at: ralph-iteration-start
---

## Session: {task}

**Task**: {task_description}
**Spec**: {spec_path or "None"}
**Completion Promise**: {promise}
**Started**: {timestamp}
**Status**: active

## Acceptance Criteria

{criteria_from_spec_or_user}

## Current Progress

### Latest Iteration: 0

**Status**: not started
**Next**: Begin implementation

## Blockers Resolved

(none yet)

## Patterns Discovered

(none yet)
""")
```

---

## Step 3: Load Spec (If Provided)

If a spec was provided:

```python
# Read the spec
spec_path = f".specify/specs/{spec_name}/spec.md"
read_file(spec_path)

# Extract:
# - Acceptance criteria (for the prompt)
# - Completion promise (for --completion-promise flag)
```

If no spec, ask user for:
- Clear acceptance criteria
- Completion promise text

---

## Step 4: Generate Ralph Prompt

Create the prompt that will be fed each iteration:

```markdown
You are in a ralph-loop building: {TASK}

═══════════════════════════════════════════════════════════════════════════════
CRITICAL: EVERY ITERATION MUST FOLLOW THIS SEQUENCE
═══════════════════════════════════════════════════════════════════════════════

## 1. READ CONTEXT FIRST (Serena Memories)

Before doing ANY work, read your context:

```
list_memories()
read_memory("{session_name}")           # Your session state
read_memory("claude_code_patterns")     # How to work in this project
read_memory("debugging-lessons")        # Past gotchas to avoid
```

Also check:
- progress.txt (if exists) - iteration history
- git log --oneline -5 - recent changes

## 2. FOLLOW CLAUDE.md TOOL RULES

You MUST use Serena for all code operations:
- get_symbols_overview() before reading files
- find_symbol() for navigation (NOT grep)
- replace_symbol_body() for edits (NOT full rewrites)
- find_referencing_symbols() before modifying shared code

## 3. WORK ON NEXT STEP

Based on progress, implement the next piece:
- One logical step per iteration
- Run tests after changes
- Keep changes focused and atomic

## 4. LEARN - UPDATE MEMORIES

After working, update your session memory:

```
edit_memory("{session_name}", 
  needle="### Latest Iteration:.*?(?=## Blockers|## Patterns|$)",
  repl="### Latest Iteration: {N}\n\n**Status**: {success|failure}\n**Summary**: {what_you_did}\n**Tests**: {X/Y passing}\n**Next**: {what_comes_next}\n\n",
  mode="regex")
```

If you discovered a pattern or gotcha:
```
edit_memory("debugging-lessons", add_new_lesson)
```

## 5. COMMIT CHANGES

```bash
git add -A
git commit -m "ralph iteration {N}: {summary}"
```

## 6. UPDATE progress.txt

Append iteration summary to progress.txt for quick reference.

═══════════════════════════════════════════════════════════════════════════════
ACCEPTANCE CRITERIA
═══════════════════════════════════════════════════════════════════════════════

{CRITERIA_LIST}

═══════════════════════════════════════════════════════════════════════════════
COMPLETION
═══════════════════════════════════════════════════════════════════════════════

When ALL acceptance criteria are met with evidence:
1. Verify each criterion (run tests, check output)
2. Update session memory status to "completed"
3. Output: <promise>{COMPLETION_PROMISE}</promise>

═══════════════════════════════════════════════════════════════════════════════
IF STUCK (Same error 3+ times)
═══════════════════════════════════════════════════════════════════════════════

If you encounter the same error/failure for {stuck_threshold} consecutive iterations:

1. Update session memory:
   - Add to "## Blockers Resolved" section (even though not resolved yet)
   - Mark status as "stuck"
   - Document the symptom clearly

2. The system will automatically switch to elimination debugging.
   Elimination will:
   - Generate hypotheses for the root cause
   - Systematically test and eliminate
   - Apply fix when confirmed
   - Resume this ralph loop

Do NOT try random fixes. Document and let elimination handle it.
```

---

## Step 5: Start Ralph Loop

Execute the ralph-loop command:

```bash
/ralph-loop "{generated_prompt}" \
  --max-iterations {max_iterations} \
  --completion-promise "{promise_text}"
```

---

## Step 6: Monitor for Stuck State

The stop hook should detect stuck state by checking:
- Session memory status
- Consecutive failures in progress

When stuck detected:
1. Pause ralph (native mechanism)
2. Extract symptom from session memory
3. Run: `/claude-learns.eliminate {symptom}`
4. Elimination will fix and signal resume

---

## Step 7: On Completion

When ralph completes (promise found):

1. **Verify with spec** (if exists):
   ```
   /claude-learns.spec-verify {spec_name}
   ```

2. **Run learning loop**:
   ```
   /claude-learns.learn
   ```

3. **Archive session memory**:
   - Rename to `ralph-session-{name}-completed-{date}`
   - Or delete if not worth keeping

4. **Summary**:
   ```
   ════════════════════════════════════════
   RALPH SESSION COMPLETE
   
   Task: {task}
   Total iterations: {N}
   Elimination detours: {M}
   Time: {duration}
   Result: SUCCESS
   ════════════════════════════════════════
   ```

---

## Quick Start Examples

### With Spec
```
/claude-learns.ralph --spec user-auth
```

### Direct Task
```
/claude-learns.ralph "Build REST API for todos with CRUD, validation, tests. Promise: TODO-API-DONE"
```

### With Options
```
/claude-learns.ralph "Migrate from Jest to Vitest" --max-iterations 50 --stuck-threshold 5
```

---

## Troubleshooting

### Loop not starting?
- Check ralph-loop plugin is installed: `/plugin list`
- Install if needed: `/plugin install ralph-loop@claude-plugins-official`

### Context lost after /clear?
- Session memory should persist
- Run `read_memory("ralph-session-{name}")` to recover

### Stuck in elimination?
- Check `/claude-learns.eliminate-status`
- Can manually `/cancel-ralph` and restart

---

Now execute steps 1-5 for: $ARGUMENTS
