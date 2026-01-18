<!--
ROUTING GUIDE
─────────────
WHEN TO USE: ONLY for "claimed done but wasn't" situations
WRITTEN BY: /spec-correction, /learn
NOT FOR: General bug patterns (use common-bugs.md)
-->

# Corrections Log

Persistent record of premature completion claims. Read by `/spec-verify` to
prevent repeat failures.

> **Purpose**: When Claude claims "done" but the implementation wasn't actually
> working, corrections are logged here. Future `/spec-verify` runs check these
> patterns to avoid repeating the same mistakes.

---

## How This File Works

1. **When corrections are added**: After user reports something "isn't working"
   that was claimed complete, run `/spec-correction` to add an entry here.

2. **When corrections are used**: Before claiming completion, `/spec-verify`
   reads this file and checks patterns relevant to the feature type.

3. **Organization**: Entries grouped by feature type (Authentication, API, UI, etc.)

---

## Authentication

<!-- Corrections for auth-related features go here -->

---

## API

<!-- Corrections for API-related features go here -->

---

## UI

<!-- Corrections for UI-related features go here -->

---

## Data / State Management

<!-- Corrections for state/data features go here -->

---

## Configuration

<!-- Corrections for config-related features go here -->

---

## Pattern Index

Quick lookup of common correction patterns:

| Pattern | Category | Occurrences | Features Affected |
|---------|----------|-------------|-------------------|
| <!-- Example: Email special chars | Input validation | 2 | Auth, Profile --> |

---

## Entry Template

When adding a new correction, use this format:

```markdown
### CORR-{id}: {Feature Name} - {Date}

**Feature Type**: {category}

**Claimed**: "{exact claim made}"

**Actually**: {what actually happened / the bug}

**Would Have Caught It**:
- Test: {specific test command or scenario}
- Check: {specific thing to verify}

**Pattern**: {generalized pattern for future reference}
- Category: {Input validation | Edge case | Async timing | State management | etc.}
```

---

*Last Updated: 2026-01-17*
