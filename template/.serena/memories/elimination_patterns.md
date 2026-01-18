<!--
ROUTING GUIDE
─────────────
WHEN TO USE: Quick reference patterns for /eliminate sessions (human-readable)
WRITTEN BY: /eliminate (on session complete)
NOT FOR: Statistical tracking (use heuristics.yaml), Detailed lessons (use debugging-lessons.md)
-->

# Elimination Patterns - Quick Reference for Claude Code Sessions

This file provides quick-access patterns learned from debugging sessions.
Read this at the start of any debugging session for context.

## High-Value Elimination Patterns

### 🔥 Intermittent Errors Under Load
**First checks:**
1. Concurrency issues (race conditions, lock contention)
2. Resource pool exhaustion (connections, threads)
3. Timeout configurations

**Quick discriminators:**
- If errors correlate with RPS → likely concurrency
- If errors correlate with pool metrics → likely pool exhaustion
- If errors are truly random → likely timing/network

### 🗄️ Database-Related Symptoms
**First checks:**
1. Connection pool metrics
2. Slow query log
3. Lock wait timeouts

**Quick discriminators:**
- Pool at capacity during errors → pool sizing
- Long-running queries visible → query optimization
- No pool/query issues → likely application code

### 🚀 Post-Deployment Issues
**First checks:**
1. Config diff between environments
2. Dependency version changes
3. Feature flag states

**Quick discriminators:**
- Works in one env, not another → config
- Worked before update → dependency change
- Partial rollout affected → feature flag

### 🔄 Async/Promise Issues
**First checks:**
1. Unhandled promise rejections
2. Race conditions in state updates
3. Missing await keywords

**Quick discriminators:**
- Errors appear after refactoring async code → missing await
- State inconsistencies → race condition
- Silent failures → unhandled rejections

## Evidence Gathering Priorities

### Most Discriminating Evidence Types
1. **Correlation analysis** - Does metric X correlate with errors?
2. **Timing logs** - When exactly do failures occur?
3. **Diff comparison** - What changed between working/broken states?
4. **Isolation tests** - Does problem persist with component X disabled?

### Least Useful Evidence Types
1. "It works on my machine" - Too many confounding variables
2. Single anecdotal observation - Need reproducible pattern
3. Speculation without data - Collect evidence first

## Elimination Decision Thresholds

| Confidence | Status | Action |
|------------|--------|--------|
| > 0.90 | Confirmed | Proceed to verification |
| 0.25 - 0.90 | Active | Continue gathering evidence |
| 0.05 - 0.25 | Unlikely | Deprioritize, may revisit |
| < 0.05 | Eliminated | Archive, allow resurrection |

## Common Mistakes to Avoid

### Premature Elimination
❌ Eliminating based on single piece of evidence
✅ Require 2-3 confirmatory tests before hard elimination

### Incomplete Hypothesis Space
❌ Only considering obvious causes
✅ Use Ishikawa categories to ensure coverage

### Confirmation Bias
❌ Only looking for evidence supporting favorite hypothesis
✅ Design tests that could ELIMINATE the leading hypothesis

### Forgetting to Learn
❌ Fixing the bug and moving on
✅ Document pattern, update heuristics, archive session

## Session Workflow Reminder

```
1. /eliminate [symptom]     → Generate hypotheses
2. /eliminate-status        → Review current state
3. /hypothesis [new idea]   → Add hypothesis if needed
4. /evidence [H#] [result]  → Record evidence
5. /eliminate-status        → Check convergence
6. Repeat 3-5 until confirmed
7. Verify fix works
8. Learning phase runs automatically
```

## Integration with Project

- Hypotheses stored in: `.elimination/active/hypotheses/`
- Evidence stored in: `.elimination/active/evidence/`
- Heuristics in: `.elimination/learned/heuristics.yaml`
- Config in: `.elimination/config.yaml`
- Archives in: `.elimination/archive/`
