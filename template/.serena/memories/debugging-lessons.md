<!--
ROUTING GUIDE
─────────────
WHEN TO USE: Detailed insights from ONE debugging session
WRITTEN BY: /learn
NOT FOR: Recurring patterns (use common-bugs.md), Statistical heuristics (use heuristics.yaml)
-->

# Debugging Lessons

> Lessons learned from past debugging sessions. Read this before starting complex debugging.

---

## Purpose

This memory captures insights from completed debugging sessions to:
- Avoid repeating the same investigation steps
- Recognize patterns that led to quick resolutions
- Remember non-obvious root causes for similar symptoms

## When to Read

- Before `/eliminate` sessions
- Before `/spec-debug` sessions
- When encountering a symptom that feels familiar

## When to Update

- After resolving a non-trivial bug
- When a debugging pattern proved especially effective
- After `/eliminate` Phase 4 (Learning) completes

---

## Lessons by Symptom Pattern

### Authentication/Login Issues

| Symptom | Likely Cause | Investigation Path |
|---------|--------------|-------------------|
| "Correct credentials rejected" | Case sensitivity | Check email normalization first |
| "Session expires too quickly" | Clock skew or config | Compare server time, check token expiry config |
| "Intermittent auth failures" | Race condition or cache | Check concurrent requests, cache invalidation |

### API/Network Issues

| Symptom | Likely Cause | Investigation Path |
|---------|--------------|-------------------|
| "Intermittent 500 errors" | Connection pool or concurrency | Check pool metrics, correlate with load |
| "Timeout under load" | Resource exhaustion | Check DB connections, memory, threads |
| "Works locally, fails in prod" | Environment config | Compare env vars, check secrets |

### Data/State Issues

| Symptom | Likely Cause | Investigation Path |
|---------|--------------|-------------------|
| "Data appears stale" | Caching issue | Check cache TTL, invalidation triggers |
| "Inconsistent results" | Race condition | Check transaction isolation, locking |
| "Works first time, fails second" | State not reset | Check cleanup in test/teardown |

---

## High-Value Debugging Techniques

### Technique: Binary Search Through History

**When**: Bug appeared "at some point" with no clear trigger
**How**: Use `/bisect` or manual git bisect
**Success rate**: High for regressions

### Technique: Spec Deviation Analysis

**When**: Feature exists but behaves "wrong"
**How**: Run `/spec-validate`, check each deviation
**Success rate**: Very high when spec exists

### Technique: Correlation Analysis

**When**: Intermittent issues
**How**: Correlate errors with time, load, specific inputs
**Success rate**: Medium-high, requires good logging

---

## Anti-Patterns (What NOT to Do)

### Anti-Pattern: Shotgun Debugging

**What**: Making multiple changes hoping something works
**Why bad**: Masks root cause, introduces new bugs
**Instead**: Change one thing, verify, revert if not fixed

### Anti-Pattern: Assuming Environment

**What**: Not verifying the actual environment state
**Why bad**: "It works on my machine"
**Instead**: Always verify env vars, versions, configs

### Anti-Pattern: Ignoring Spec Deviations

**What**: Dismissing spec differences as "intentional"
**Why bad**: Many bugs hide in undocumented deviations
**Instead**: Log all deviations, even if intentional

---

## Session Archive Reference

<!-- Add references to notable archived sessions -->

| Session ID | Date | Symptom | Root Cause | Key Lesson |
|------------|------|---------|------------|------------|
| `example-001` | 2026-01-17 | [Symptom] | [Cause] | [Lesson] |

---

## Pattern Recognition Triggers

When you see these patterns, check these causes first:

```
"works locally" → environment config, secrets, network
"intermittent" → concurrency, caching, external dependencies
"after deploy" → config change, migration, version mismatch
"only in prod" → scale issues, real data edge cases
"only for some users" → data-dependent, permissions, A/B testing
"since yesterday" → recent commit, external service change
```

---

*Last Updated: 2026-01-17*
*Entries: 0 specific lessons (template ready)*
