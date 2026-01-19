# /spec-verify - Verification Gate Before Claiming Completion

**Purpose**: Require concrete evidence for each acceptance criterion before claiming implementation is complete.

**CRITICAL**: Never claim "done" without running this command first.

---

## Workflow

### Step 1: Load Past Corrections

Read `.specify/memory/corrections.md` for this feature type. Past corrections inform what to double-check.

```bash
# Check for correction patterns
read_memory("corrections") or read .specify/memory/corrections.md
```

Look for patterns matching this feature type (e.g., "Authentication", "API", "UI").

### Step 2: Load the Specification

```bash
# Load the spec
cat .specify/specs/{feature}/spec.md
```

Extract all **Acceptance Criteria** from the spec.

### Step 3: Verify Each Criterion

For **each** acceptance criterion:

1. **Identify Verification Method**:
   - Test command to run
   - Manual check to perform
   - Code inspection required
   - Log/output to examine

2. **ACTUALLY RUN the verification** (do not assume or claim):
   - Execute the test
   - Trigger the scenario
   - Inspect the code
   - Check the output

3. **Record Concrete Evidence**:
   - Test output (copy actual output)
   - Screenshot reference
   - Log entries
   - Code snippets showing implementation

### Step 4: Generate Verification Report

Create a verification table:

```markdown
## Verification Report: {feature}

**Date**: {date}
**Spec Version**: {version from spec}

### Criteria Results

| # | Criterion | Verification Method | Result | Evidence |
|---|-----------|---------------------|--------|----------|
| 1 | "User can login with email" | Run login test | ✅ PASS | `npm test auth.login` output: 5 tests passed |
| 2 | "Errors display to user" | Trigger invalid login | ❌ FAIL | No error message rendered, console shows error swallowed |
| 3 | "Session persists on refresh" | Manual browser test | ✅ PASS | localStorage shows valid token after F5 |

### Known Corrections Checked

| Pattern from corrections.md | Verified? | Result |
|-----------------------------|-----------|--------|
| "Email special chars (+) break login" | Yes | ✅ test+user@example.com works |
| "Password field accepts < 8 chars" | Yes | ✅ Validation rejects short passwords |

### Overall Status

- Total Criteria: {n}
- Passed: {passed}
- Failed: {failed}
- **GATE RESULT**: {PASS / FAIL}
```

### Step 5: Gate Decision

**IF ALL CRITERIA PASS**:
- May claim implementation complete
- Include verification report summary in completion message

**IF ANY CRITERION FAILS**:
- **DO NOT** claim "done" or "implementation complete"
- List the failing criteria
- Fix each issue
- Re-run `/spec-verify` until all pass

### Step 6: Persist Report

**Always** save the verification report for audit trail:

```bash
# Report location
.specify/reports/{feature}-verify-{YYYY-MM-DD}.md
```

**Report Template:**

```markdown
# Verification Report: {feature}

**Date**: {YYYY-MM-DD}
**Status**: {PASS / FAIL}
**Spec Version**: {from spec file}

## Criteria Checked

| # | Criterion | Method | Result | Evidence |
|---|-----------|--------|--------|----------|
| 1 | {criterion text} | {how verified} | ✅ PASS / ❌ FAIL | {concrete evidence} |
| 2 | ... | ... | ... | ... |

## Known Corrections Checked

| Pattern | Verified | Result |
|---------|----------|--------|
| {from corrections.md} | Yes/No | ✅/❌ |

## Issues Found

{List any failing criteria with details, or "None - all criteria passed"}

## Summary

- **Total Criteria**: {n}
- **Passed**: {count}
- **Failed**: {count}
- **Gate Result**: {PASS / FAIL}

---
*Verified by Claude Code via /spec-verify*
```

---

## Evidence Quality Standards

### Good Evidence (Concrete)

```
✅ "Test output: PASS - 15 assertions, 0 failures"
✅ "curl -X POST /api/login returned 200 with token"
✅ "Error message 'Invalid credentials' displayed in .error-banner"
✅ "Code at auth.ts:42 validates email format with regex"
```

### Bad Evidence (Assumptions)

```
❌ "I believe this works"
❌ "Should be fine based on the implementation"
❌ "This pattern is correct"
❌ "Tests would pass"
```

---

## Integration with Correction Loop

If user later says "this isn't working":

1. **Immediately run `/spec-correction`** to capture what went wrong
2. The correction gets added to `.specify/memory/corrections.md`
3. Future `/spec-verify` runs will check for this pattern

---

## Quick Reference

```bash
# Verify a feature before claiming done
/spec-verify login-feature

# What happens:
# 1. Load past corrections for "Authentication" features
# 2. Load .specify/specs/login-feature/spec.md
# 3. For each criterion, run actual verification
# 4. Generate evidence table
# 5. Gate: ALL PASS → may claim done, ANY FAIL → fix and re-verify
```

---

## Example Session

```
User: Implement the login feature per spec

Claude: I've implemented the login feature. Let me verify before claiming completion.

/spec-verify login-feature

## Verification Report: login-feature

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Email/password login works | `npm test auth` | ✅ PASS | 12 tests passed |
| Invalid credentials show error | Manual trigger | ❌ FAIL | Error logged but not displayed |
| Remember me persists session | Browser test | ✅ PASS | Cookie set with 30-day expiry |

**GATE RESULT: FAIL** - 1 criterion not met

I found that error messages aren't being displayed to the user. Let me fix that...

[fixes the error display]

/spec-verify login-feature

| Criterion | Method | Result | Evidence |
|-----------|--------|--------|----------|
| Email/password login works | `npm test auth` | ✅ PASS | 12 tests passed |
| Invalid credentials show error | Manual trigger | ✅ PASS | "Invalid credentials" shown in .error-message |
| Remember me persists session | Browser test | ✅ PASS | Cookie set with 30-day expiry |

**GATE RESULT: PASS** - All 3 criteria verified

Implementation is complete. All acceptance criteria have been verified with concrete evidence.
```
