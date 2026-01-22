# Ralph Loop Guide for Claude-Learns

> Autonomous iteration loops that learn as they build.

## What is Ralph?

Ralph is a technique that runs Claude in a continuous loop, iterating on the same task until completion. Named after Ralph Wiggum from The Simpsons, it embodies the philosophy: **"Iteration beats perfection."**

Claude-learns integrates ralph-loop with:
- **Memory persistence** - Session state survives `/clear`
- **Learning each iteration** - Patterns captured to Serena memories
- **Tool enforcement** - Serena tools used correctly every time
- **Elimination integration** - Auto-debug when stuck

## Quick Start

### With a Spec (Recommended)
```bash
# Create spec first
/claude-learns.spec-create user-auth

# Start ralph with spec
/claude-learns.ralph --spec user-auth --max-iterations 30
```

### Direct Task
```bash
/claude-learns.ralph "Build REST API for todos. Criteria: CRUD endpoints, validation, tests >80%, README. Promise: TODOS-DONE"
```

## How It Works

### The Loop

```
┌────────────────────────────────────────────────────────────────────┐
│                         RALPH LOOP                                  │
│                                                                    │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │
│  │ 1. READ      │ ──▶ │ 2. WORK      │ ──▶ │ 3. LEARN     │       │
│  │              │     │              │     │              │       │
│  │ • Memories   │     │ • Serena     │     │ • Update     │       │
│  │ • Progress   │     │   tools      │     │   memories   │       │
│  │ • Git log    │     │ • Tests      │     │ • Patterns   │       │
│  └──────────────┘     └──────────────┘     └──────────────┘       │
│         │                                          │               │
│         │              ┌──────────────┐            │               │
│         │              │ 4. COMMIT    │            │               │
│         │              │              │ ◀──────────┘               │
│         │              │ • Git commit │                            │
│         │              │ • Progress   │                            │
│         │              └──────────────┘                            │
│         │                     │                                    │
│         │              ┌──────────────┐                            │
│         │              │ 5. CHECK     │                            │
│         │              │              │                            │
│         │              │ Complete?    │──── YES ──▶ EXIT           │
│         │              │ Stuck?       │──── YES ──▶ ELIMINATION    │
│         │              │ Max iter?    │──── YES ──▶ EXIT           │
│         │              └──────────────┘                            │
│         │                     │ NO                                 │
│         └─────────────────────┘                                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Persistence Strategy

| What | Where | Survives |
|------|-------|----------|
| Loop state | `.claude/ralph-loop.local.md` | Session end |
| Code changes | Git history | Everything |
| Iteration log | `progress.txt` | In git |
| **Learnings** | Serena memories | `/clear`, restarts |

The key addition is **Serena memories**. Each iteration writes insights, so even if you `/clear` mid-loop, memories retain context.

## Iteration Discipline

### 1. READ Context First

**EVERY iteration MUST start by reading memories:**

```python
# Required at start of each iteration
list_memories()
read_memory("ralph-session-{name}")     # Session state
read_memory("claude_code_patterns")     # How to work here
read_memory("debugging-lessons")        # Past gotchas
```

This ensures context recovery after `/clear`.

### 2. WORK Using Serena

Follow CLAUDE.md tool rules:
- `get_symbols_overview()` before reading files
- `find_symbol()` for navigation (NOT grep)
- `replace_symbol_body()` for edits (NOT rewrites)
- `find_referencing_symbols()` before modifying shared code

### 3. LEARN Each Iteration

After working, update memories:

```python
# Update session memory with progress
edit_memory("ralph-session-{name}",
    needle="### Latest Iteration:.*",
    repl="### Latest Iteration: 5\n\n**Status**: success\n**Summary**: Implemented auth middleware\n**Tests**: 4/5 passing\n**Next**: Add refresh endpoint\n",
    mode="regex")

# If discovered a pattern or gotcha
edit_memory("debugging-lessons",
    needle="## Recent Lessons\n",
    repl="## Recent Lessons\n\n### JWT payload validation\nAlways check structure before accessing claims.\n\n",
    mode="literal")
```

### 4. COMMIT Changes

```bash
git add -A
git commit -m "ralph iteration 5: implemented auth middleware"
```

### 5. Update Progress

Append to `progress.txt`:
```
--- Iteration 5 ---
✓ Implemented auth middleware
✓ Tests: 4/5 passing
Next: Add refresh endpoint
```

## Elimination Integration

When ralph detects being stuck (same error 3+ iterations), it automatically switches to elimination debugging.

### Detection

```
Iteration 3: TypeError: Cannot read 'exp'
Iteration 4: TypeError: Cannot read 'exp'  
Iteration 5: TypeError: Cannot read 'exp'
^^^ STUCK - 3 consecutive same errors
```

### Flow

```
RALPH (stuck)
    │
    ▼
UPDATE MEMORY
    │ Write blocker to ralph-session memory
    │
    ▼
START ELIMINATION
    │ /claude-learns.eliminate "TypeError: Cannot read 'exp'"
    │
    ▼
ELIMINATION LOOP
    │ Generate hypotheses
    │ Gather evidence
    │ Eliminate until confirmed
    │ Apply fix
    │
    ▼
WRITE TO MEMORY
    │ Add to debugging-lessons
    │ Update ralph-session with resolution
    │
    ▼
RESUME RALPH
    │ Ralph reads memories
    │ Sees fix in git history
    │ Continues building
    │
    ▼
COMPLETION
```

### Memory Continuity

Elimination reads the same memories as ralph, so it has full context:
- What was being built
- What iteration we were on
- What was already tried

## Writing Good Prompts

### Required Elements

1. **Clear task description**
2. **Acceptance criteria** (checkable items)
3. **Completion promise** (exact text to output when done)
4. **Stuck instructions** (what to do if blocked)

### Template

```
You are in a ralph-loop building: [TASK]

EVERY ITERATION:
1. Read memories first (list_memories, read_memory)
2. Follow CLAUDE.md tool rules (Serena)
3. Write learnings to memories
4. Commit changes

ACCEPTANCE CRITERIA:
1. [ ] [Criterion 1]
2. [ ] [Criterion 2]
3. [ ] [Criterion 3]

When ALL criteria met: <promise>[PROMISE]</promise>

If stuck (same error 3x):
- Document blocker in memory
- System will switch to elimination
```

### Examples

**Good:**
```
Build user authentication. Criteria:
1. JWT login at /api/auth/login
2. Token refresh at /api/auth/refresh
3. Auth middleware for protected routes
4. Tests passing (>80% coverage)
5. README documents auth flow

When complete: <promise>AUTH-DONE</promise>
```

**Bad:**
```
Build a good auth system
```
(No criteria, no promise, no way to verify)

## Best Practices

### Do

- ✅ Start with `/claude-learns.spec-create` for complex features
- ✅ Set reasonable `--max-iterations` (20-30 typical)
- ✅ Use specs for completion criteria
- ✅ Let elimination handle stuck states
- ✅ Review git history after completion

### Don't

- ❌ Use ralph for debugging (use elimination)
- ❌ Use ralph for exploratory work
- ❌ Skip the memory reads
- ❌ Try random fixes when stuck (let elimination handle it)
- ❌ Run without iteration limits

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/claude-learns.ralph [task]` | Start ralph with claude-learns integration |
| `/claude-learns.ralph-status` | Check session status |
| `/cancel-ralph` | Stop the loop |
| `/claude-learns.eliminate [symptom]` | Switch to elimination (auto or manual) |
| `/claude-learns.spec-verify [name]` | Verify completion after ralph |
| `/claude-learns.learn` | Capture session insights |

## Troubleshooting

### Ralph not starting?

Check plugin is installed:
```bash
/plugin list | grep ralph
```

Install if needed:
```bash
/plugin install ralph-loop@claude-plugins-official
```

### Context lost after /clear?

Memories should persist. Recover with:
```python
list_memories()
read_memory("ralph-session-{name}")
```

### Stuck in elimination?

Check status:
```bash
/claude-learns.eliminate-status
```

Can cancel and restart:
```bash
/cancel-ralph
/claude-learns.ralph --spec {spec}
```

### Loop running forever?

Always set `--max-iterations`. Check completion promise is achievable.

## Real-World Results

The ralph technique has been used to:
- Build complete programming languages over months
- Ship 6+ repos overnight in hackathons
- Complete $50k contracts for <$300 in API costs

The key is **clear specs + iteration + learning**.

---

## Related

- [CLAUDE.md](./CLAUDE.md) - Tool usage rules
- [.elimination/README.md](.elimination/README.md) - Elimination debugging
- [.specify/README.md](.specify/README.md) - Spec-driven development
- [Official ralph-loop plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-loop)

---

*Part of the claude-learns template*
