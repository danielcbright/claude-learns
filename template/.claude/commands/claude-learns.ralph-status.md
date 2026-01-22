Check the status of the current or most recent ralph session.

## Step 1: Find Active Session

Look for ralph session memories:

```python
list_memories()
# Look for memories starting with "ralph-session-"
```

Check native ralph state:
```bash
# Check if ralph-loop is active
cat .claude/ralph-loop.local.md 2>/dev/null || echo "No active ralph-loop"
```

Check progress file:
```bash
cat progress.txt 2>/dev/null || echo "No progress.txt found"
```

---

## Step 2: Read Session Memory

If session memory found:
```python
read_memory("ralph-session-{name}")
```

Extract and display:
- Task description
- Current status (active/paused/completed)
- Latest iteration number
- Test status
- Any blockers

---

## Step 3: Display Status

Format output:

```
═══════════════════════════════════════════════════════════════════════════════
RALPH SESSION STATUS
═══════════════════════════════════════════════════════════════════════════════

Session: {name}
Status: {active | paused-elimination | completed}

Task: {description}
Spec: {spec_path or "None"}

Progress:
  Iteration: {N} / {max}
  Tests: {X/Y passing}
  
Recent Activity:
  {Last 3 iterations from progress log}

Blockers:
  {Any unresolved blockers or "None"}

Elimination Detours:
  {Count and brief summary or "None"}

═══════════════════════════════════════════════════════════════════════════════
```

---

## Step 4: Recommendations

Based on status, suggest next action:

| Status | Recommendation |
|--------|----------------|
| active | Ralph is running. Monitor or `/cancel-ralph` if needed |
| paused-elimination | Elimination in progress. Check `/claude-learns.eliminate-status` |
| stuck | Consider running `/claude-learns.eliminate {symptom}` |
| completed | Run `/claude-learns.spec-verify` then `/claude-learns.learn` |
| no session | Start with `/claude-learns.ralph "task"` |

---

Now execute for: $ARGUMENTS
