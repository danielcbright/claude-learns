# /claude-learns.status - System Status Overview

Display active sessions and recent activity across claude-learns subsystems.

## Syntax

```bash
# Show active sessions only (default)
/claude-learns.status

# Show full system state including completed sessions
/claude-learns.status --verbose
```

---

## Step 1: Parse Arguments

Check for `--verbose` flag in `$ARGUMENTS`.

---

## Step 2: Check Ralph Sessions

Use Serena MCP to check for active ralph sessions:

```python
list_memories()
# Filter for memories starting with "ralph-session-"
# Read each to check status
```

Look for:
- Active ralph-loop (`.claude/ralph-loop.local.md` exists)
- Ralph session memories with `status: active`

---

## Step 3: Check Elimination Sessions

Check for active elimination debugging session:

```bash
# Check if active session exists
if [ -f .elimination/active/session.yaml ]; then
  # Parse session info
  python .claude/scripts/elimination/eliminate_status.py --json
fi
```

---

## Step 4: Check Spec System

Count specs and check for in-progress work:

```bash
# Count total specs
spec_count=$(find .specify/specs -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)

# Check for recent spec work
recent_specs=$(find .specify/specs -name "spec.md" -mtime -7 2>/dev/null | wc -l)
```

---

## Step 5: Display Status

### Default View (Active Sessions Only)

```
═══════════════════════════════════════════════════════════════════════════
CLAUDE-LEARNS STATUS
═══════════════════════════════════════════════════════════════════════════

ACTIVE SESSIONS:
  [If ralph active]: Ralph: {task-name} (iteration {N}/{max}, {X} tests passing)
  [If elimination active]: Elimination: {symptom} ({N} hypotheses, H{X} leading at {confidence})
  [If neither]: No active sessions

[If no active sessions]:
QUICK START:
  → Start new task: /claude-learns.go "your task description"
  → Begin debugging: /claude-learns.eliminate "symptom description"
  → Create specification: /claude-learns.spec-create feature-name
  → Start autonomous loop: /claude-learns.ralph "task with clear success criteria"

[If active sessions exist]:
QUICK ACTIONS:
  → Ralph details: /claude-learns.ralph-status
  → Elimination details: /claude-learns.eliminate-status
  → View all specs: /claude-learns.spec-list
  → Continue working: /claude-learns.go "resume {task}"

═══════════════════════════════════════════════════════════════════════════

Use --verbose to see system stats and completed sessions
```

### Verbose View (--verbose flag)

Add these sections:

```
SYSTEM STATS:
  Memories: {count} files in .serena/memories/
  Specs: {count} specifications in .specify/specs/
  Archived Eliminations: {count} past debugging sessions
  Last Learning: {most recent memory update timestamp}

RECENT ACTIVITY:
  [Last 3 completed ralph sessions with dates]
  [Last 3 archived elimination sessions with dates]
  [Last 3 verified specs with dates]

MCP STATUS:
  Serena: {Connected | Not connected - run /mcp to set up}
```

---

## Implementation

Now execute for: $ARGUMENTS

**Step-by-step:**

1. Parse arguments:
   - Check if `--verbose` in `$ARGUMENTS`
   - Set `VERBOSE=true` or `VERBOSE=false`

2. Check ralph sessions:
   ```python
   list_memories()
   ```
   Look for `ralph-session-*` memories and read them to check status.

3. Check elimination:
   ```bash
   PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
   if [ -f "$PROJECT_ROOT/.elimination/active/session.yaml" ]; then
     python3 "$PROJECT_ROOT/.claude/scripts/elimination/eliminate_status.py" --json 2>/dev/null
   fi
   ```

4. Check specs:
   ```bash
   PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
   find "$PROJECT_ROOT/.specify/specs" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l
   ```

5. Format and display output based on findings.

---

## Notes

- This command is **read-only** - it never modifies state
- Designed for quick orientation ("What am I working on?")
- Smart defaults: Only shows what's relevant
- Use at session start to resume work
- Use during work to check progress
