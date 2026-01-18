# Bug Fix Specification: [BUG_TITLE]

> [One-line description of the bug]

---

## Metadata

| Field | Value |
|-------|-------|
| **Spec ID** | `bugfix-[id]` |
| **Status** | `investigating` / `root-caused` / `fixing` / `verified` / `closed` |
| **Severity** | `critical` / `high` / `medium` / `low` |
| **Reporter** | [Who reported] |
| **Assigned** | [Who is fixing] |
| **Created** | [YYYY-MM-DD] |
| **Related Issues** | [Links to issue tracker] |

---

## Bug Description

### Symptom

[What the user sees/experiences]

### Expected Behavior

[What should happen instead]

### Actual Behavior

[What actually happens]

### Reproduction Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]
4. Bug occurs

### Environment

| Factor | Value |
|--------|-------|
| OS | [e.g., macOS 14.0] |
| Version | [App version] |
| Browser | [If applicable] |
| Other | [Relevant env details] |

---

## Root Cause Analysis

### Investigation Path

[Chronological log of investigation steps]

1. **[Timestamp]**: [What was checked]
2. **[Timestamp]**: [What was found]

### Root Cause

[Clear explanation of why the bug occurs]

### Affected Code

| File | Function/Method | Issue |
|------|-----------------|-------|
| [path] | [name] | [what's wrong] |

### Related to Spec Deviation?

- [ ] Yes - deviation from spec: [link to spec]
- [ ] No - spec was followed correctly
- [ ] No spec exists for this behavior

---

## Fix Design

### Proposed Solution

[Description of the fix approach]

### Code Changes

```
[Pseudocode or description of changes]
```

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| [path] | `modify` / `add` / `delete` | [what changes] |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | `low/medium/high` | [Impact] | [How to mitigate] |

---

## Testing Plan

### Regression Test

- [ ] Bug no longer reproduces with original steps
- [ ] Related functionality still works

### New Tests to Add

- [ ] [Test case 1 - prevents regression]
- [ ] [Test case 2]

### Manual Verification

- [ ] [Manual check 1]
- [ ] [Manual check 2]

---

## Rollback Plan

[How to revert if the fix causes issues]

---

## Prevention

### How could this have been prevented?

[Analysis of process/code improvements]

### Recommendations

- [ ] [Add test for X]
- [ ] [Update spec for Y]
- [ ] [Add monitoring for Z]

---

## Timeline

| Date | Event |
|------|-------|
| [Date] | Bug reported |
| [Date] | Root cause identified |
| [Date] | Fix implemented |
| [Date] | Fix verified |

---

## Lessons Learned

[What was learned from this bug that should be remembered]

**Add to common-bugs memory?** [ ] Yes [ ] No

---

*Template Version: 1.0*
