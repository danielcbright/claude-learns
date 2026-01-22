---
type: serena-memory
name: ralph-session-template
purpose: Template for tracking ralph-loop sessions - copy and customize for each session
read_at: never (this is a template)
customize: true
---

# Ralph Session Template

> **How to use**: Copy this template to `ralph-session-[feature].md` when starting a new ralph-loop.
> The session memory persists across `/clear` and enables context recovery.

---

## Session: [FEATURE_NAME]

**Task**: [Brief description of what we're building]
**Spec**: [Path to spec if exists, e.g., .specify/specs/feature/spec.md]
**Completion Promise**: [The exact promise text, e.g., FEATURE-COMPLETE]
**Started**: [Date/time]
**Status**: active | paused-elimination | completed

---

## Acceptance Criteria

From spec or user-defined:

1. [ ] [Criterion 1]
2. [ ] [Criterion 2]
3. [ ] [Criterion 3]
4. [ ] [Criterion 4]

---

## Current Progress

### Latest Iteration: [N]

**Status**: success | failure | stuck
**Summary**: [What was accomplished or attempted]
**Tests**: [X/Y passing, coverage %]
**Next**: [What needs to happen next]

### Progress Log

| Iter | Status | Summary | Tests |
|------|--------|---------|-------|
| 1 | ✓ | Initial setup | 0/5 |
| 2 | ✓ | Core implementation | 2/5 |
| 3 | ✗ | Error X | 2/5 |

---

## Blockers Resolved

### Blocker 1: [Error/Symptom]
- **Iterations stuck**: [N-M]
- **Root cause**: [What was actually wrong]
- **Fix**: [What fixed it]
- **Lesson**: [What to remember for next time]

---

## Patterns Discovered

- [Pattern 1]: [Description]
- [Pattern 2]: [Description]

---

## Elimination Detours

### Detour 1 (if any)
- **Triggered at**: Iteration [N]
- **Symptom**: [Error message]
- **Hypotheses tested**: [Count]
- **Confirmed hypothesis**: [Which one]
- **Iterations spent**: [Count]
- **Resumed at**: Iteration [N+1]

---

## Notes

[Any additional context, decisions made, things to remember]

---

*Last updated: [timestamp]*
