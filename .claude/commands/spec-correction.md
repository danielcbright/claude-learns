# /spec-correction - Capture Corrections When Claims Were Wrong

**Purpose**: When Claude claimed "done" but the implementation wasn't actually working, capture that correction to prevent future false claims.

---

## When to Use

Trigger immediately when:

- User says "this isn't working" after you claimed completion
- User finds a bug in something you said was "verified"
- Verification passed but production behavior differs
- Edge case was missed that should have been caught

---

## Workflow

### Step 1: Gather Correction Details

Identify:

1. **What was claimed**: The specific completion/verification claim made
2. **What actually happened**: The actual behavior or bug
3. **Feature type**: Category for pattern matching (Auth, API, UI, Data, etc.)
4. **What would have caught it**: The verification step that should have been done

### Step 2: Generate Correction Entry

Create a correction entry in this format:

```markdown
### CORR-{id}: {Feature Name} - {Date}

**Feature Type**: {category}

**Claimed**: "{exact claim made}"

**Actually**: {what actually happened / the bug}

**Would Have Caught It**: {specific verification that was missed}
- Test: {specific test command or scenario}
- Check: {specific thing to verify}

**Pattern**: {generalized pattern for future reference}
- Category: {Input validation | Edge case | Async timing | State management | etc.}
```

### Step 3: Append to Corrections Memory

Append the entry to `.specify/memory/corrections.md`:

```bash
# Append new correction
edit_memory("corrections") or append to .specify/memory/corrections.md
```

### Step 4: Check for Recurring Patterns

If this pattern has occurred 2+ times:

1. Update `.serena/memories/common-bugs.md` with the pattern
2. Consider adding to spec templates as a standard check

### Step 5: Re-verify

After documenting the correction:

1. Fix the actual issue
2. Run `/spec-verify` with full evidence
3. Explicitly verify the pattern that was missed

---

## Correction Entry Examples

### Example 1: Input Validation Edge Case

```markdown
### CORR-001: User Registration - 2026-01-17

**Feature Type**: Authentication

**Claimed**: "Registration works correctly, all tests pass"

**Actually**: Users with email addresses containing '+' (like test+tag@example.com)
got "Invalid email" error even though these are valid RFC 5322 addresses

**Would Have Caught It**:
- Test: Include test case with email "user+tag@domain.com"
- Check: Verify email regex allows plus signs in local part

**Pattern**: Special characters in email addresses
- Category: Input validation edge case
- Characters to test: + . - _ % in email local part
```

### Example 2: Async Timing Issue

```markdown
### CORR-002: Dashboard Loading - 2026-01-17

**Feature Type**: UI/Data Loading

**Claimed**: "Dashboard loads all widgets, verified with manual testing"

**Actually**: On slow connections, widgets show empty state because data fetch
races with render and loses

**Would Have Caught It**:
- Test: Throttle network to 3G in DevTools, reload page
- Check: Verify loading states and data arrival order

**Pattern**: Race condition between render and async data
- Category: Async timing
- Always test: Slow network, component mount/unmount timing
```

### Example 3: State Management

```markdown
### CORR-003: Cart Quantity Update - 2026-01-17

**Feature Type**: State Management

**Claimed**: "Cart quantity updates work, tested incrementing and decrementing"

**Actually**: Clicking + quickly multiple times only increments once because
state updates were batched and overwriting each other

**Would Have Caught It**:
- Test: Click increment button 5 times rapidly
- Check: Quantity should be 5, not 1

**Pattern**: Rapid state mutations overwriting each other
- Category: State management
- Always test: Rapid clicks, concurrent updates
```

---

## Integration with Future Verifications

When `/spec-verify` runs:

1. It reads `.specify/memory/corrections.md`
2. Filters for corrections matching the feature type
3. Adds those patterns to the verification checklist
4. Explicitly verifies those patterns weren't repeated

---

## Quick Reference

```bash
# After user says "login isn't working"
/spec-correction

# Prompts for:
# - What did you claim?
# - What actually happened?
# - What feature type is this?
# - What verification would have caught it?

# Generates CORR entry and appends to corrections.md
```

---

## Template for Quick Capture

When user corrects you, immediately gather:

```
Claimed: [copy your exact claim]
Actually: [what user reported / what you now see]
Feature Type: [Auth | API | UI | Data | State | Config | ...]
Would Have Caught It: [specific test/check to add]
Pattern: [generalized for future use]
```

Then run `/spec-correction` to persist it.

---

## Memory Structure

The corrections file (`.specify/memory/corrections.md`) is organized:

```markdown
# Corrections Log

Persistent record of premature completion claims. Read by /spec-verify to
prevent repeat failures.

---

## Authentication

### CORR-001: ...
### CORR-004: ...

## API

### CORR-002: ...

## UI

### CORR-003: ...

---

## Pattern Index

Quick lookup of common correction patterns:

| Pattern | Category | Occurrences | Features Affected |
|---------|----------|-------------|-------------------|
| Email special chars | Input validation | 2 | Auth, Profile |
| Rapid click handling | State management | 1 | Cart |
```
