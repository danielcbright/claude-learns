<!--
ROUTING GUIDE
─────────────
WHEN TO USE: Bug patterns that occur 2+ times in a feature area
WRITTEN BY: /learn, /spec-correction
NOT FOR: One-time insights (use debugging-lessons.md), Spec claim failures (use corrections.md)
-->

# Common Bugs

> Recurring bug patterns organized by feature area. Quick reference for known issues.

---

## Purpose

This memory tracks bugs that:
- Have occurred multiple times
- Have non-obvious root causes
- Affect specific features or areas

## When to Read

- When debugging a feature that has had bugs before
- When `/spec-validate` finds issues
- Before implementing changes to bug-prone areas

## When to Update

- After fixing a bug that has occurred before
- When a bug has a non-obvious solution worth remembering
- After `/eliminate` identifies a pattern

---

## Bugs by Feature Area

### [FEATURE_AREA_1]

#### Bug: [BUG_TITLE]

**Symptoms**: [What users see]

**Root Cause**: [Why it happens]

**Fix**: [How to resolve]

**Prevention**: [How to prevent recurrence]

**Occurrences**: [Count and dates]

---

### Authentication

#### Bug: Case-Sensitive Email Comparison

**Symptoms**: User can't login with correct password

**Root Cause**: Email stored as "User@Email.com" but login attempts with "user@email.com" fail due to strict equality comparison

**Fix**: Normalize emails to lowercase before comparison
```javascript
// Before
if (email === storedEmail) ...

// After
if (email.toLowerCase() === storedEmail.toLowerCase()) ...
```

**Prevention**: Add spec requirement for case-insensitive email handling

**Occurrences**: [Track here]

---

### API Layer

#### Bug: [Example - Connection Pool Exhaustion]

**Symptoms**: Intermittent 500 errors under load

**Root Cause**: Database connections not properly released in error paths

**Fix**: Ensure connection release in finally blocks

**Prevention**: Use connection middleware that auto-releases

**Occurrences**: [Track here]

---

### Data Layer

#### Bug: [Example - N+1 Query]

**Symptoms**: Slow page load for lists

**Root Cause**: Fetching related data in loop instead of batch

**Fix**: Use eager loading or batch queries

**Prevention**: Monitor query count in tests

**Occurrences**: [Track here]

---

## Bugs by Root Cause Category

### Race Conditions

| Location | Trigger | Fix Applied |
|----------|---------|-------------|
| [File:line] | [What causes it] | [How fixed] |

### Configuration Issues

| Setting | Wrong Value | Correct Value | Impact |
|---------|-------------|---------------|--------|
| [Setting] | [Wrong] | [Right] | [What broke] |

### Edge Cases

| Input | Expected | Actual | Fix |
|-------|----------|--------|-----|
| [Edge case] | [Expected behavior] | [Actual behavior] | [Fix] |

---

## High-Risk Areas

Areas that have historically been bug-prone:

| Area | Bug Count | Last Bug | Risk Level |
|------|-----------|----------|------------|
| [Area] | [Count] | [Date] | high/medium/low |

---

## Prevention Checklist

Before modifying these areas, verify:

### Authentication Changes
- [ ] Email handling is case-insensitive
- [ ] Password hashing uses approved algorithm
- [ ] Token expiry is configured correctly
- [ ] Rate limiting is in place

### API Changes
- [ ] Error responses follow spec format
- [ ] Connections are properly released
- [ ] Timeouts are configured

### Data Changes
- [ ] Migrations are reversible
- [ ] Indexes exist for query patterns
- [ ] Transactions used where needed

---

*Last Updated: 2026-01-17*
*Total Bugs Tracked: 0 (template ready)*
