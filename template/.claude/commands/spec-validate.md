# /spec-validate - Validate Implementation Against Spec

**Syntax:** `/spec-validate [feature_name] [--strict] [--generate-report]`

Check whether the current implementation matches its specification.

## Overview

Compares actual behavior and code structure against the documented specification,
identifying deviations that may indicate bugs, incomplete features, or intentional
changes that need documentation.

## Before Using This Command

Fetch latest documentation if unsure about API/behavior:
- Spec-Kit: `mcp__context7__resolve-library-id("github spec-kit")`
- Serena: `mcp__context7__resolve-library-id("serena mcp")`

## Workflow

### Phase 1: Load Specification

1. **Read spec file**
   - Load `.specify/specs/{feature_name}/spec.md`
   - If not found, suggest creating with `/spec-create`

2. **Parse acceptance criteria**
   - Extract testable criteria from spec
   - Identify behavioral requirements
   - Note technical constraints

3. **Load deviation history**
   - Check `.specify/deviations/` for approved deviations
   - Filter to deviations for this feature

### Phase 2: Implementation Analysis

1. **Locate implementation code**
   - Use key components from spec
   - Find related files via symbol search
   - Map spec components to code locations

2. **Check each acceptance criterion**

   For each criterion:
   ```
   [ ] Criterion: {description}
       - Code location: {file:line}
       - Status: PASS | FAIL | PARTIAL | NOT_IMPLEMENTED
       - Evidence: {what was observed}
   ```

3. **Verify technical design**
   - Architecture matches spec
   - API contracts followed
   - Data model implemented correctly

4. **Check edge cases**
   - Error handling matches spec
   - Edge cases from spec are handled
   - No undocumented edge cases added

### Phase 3: Deviation Detection

1. **Classify deviations**

   | Type | Description | Action |
   |------|-------------|--------|
   | Bug | Unintentional deviation | Create bug-fix spec |
   | Missing | Not yet implemented | Track as incomplete |
   | Approved | Documented deviation | Reference deviation log |
   | Undocumented | Intentional but not logged | Log with `/spec-deviation` |

2. **Generate deviation list**
   ```
   ## Deviations Found

   ### Critical (Bugs)
   - [Deviation 1]: Expected X, found Y

   ### Missing Implementation
   - [Feature Z] not yet implemented

   ### Approved Deviations
   - [Deviation 2]: Approved in deviation-{id}.md

   ### Undocumented Changes
   - [Behavior A] differs from spec - needs documentation
   ```

### Phase 4: Report Generation

1. **Summary**
   ```
   ## Validation Report: {feature_name}

   **Spec Version**: {version/date}
   **Validation Date**: {today}
   **Overall Status**: PASS | PARTIAL | FAIL

   ### Criteria Summary
   - Passed: X/Y
   - Failed: X/Y
   - Not Implemented: X/Y

   ### Deviations
   - Critical: X
   - Approved: X
   - Undocumented: X
   ```

2. **Recommendations**
   - Bug fixes needed
   - Missing implementations to complete
   - Deviations to document
   - Spec updates needed (if implementation is correct)

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Fail on any undocumented deviation |

## Report Persistence

**Always** save validation reports for audit trail:

```bash
# Report location
.specify/reports/{feature}-validate-{YYYY-MM-DD}.md
```

**Report Template:**

```markdown
# Validation Report: {feature}

**Date**: {YYYY-MM-DD}
**Spec Version**: {version/date from spec}
**Overall Status**: {PASS / PARTIAL / FAIL}

## Criteria Summary

| Status | Count |
|--------|-------|
| Passed | {n} |
| Failed | {n} |
| Partial | {n} |
| Not Implemented | {n} |

## Acceptance Criteria Results

| # | Criterion | Status | Code Location | Evidence |
|---|-----------|--------|---------------|----------|
| AC1 | {description} | PASS/FAIL/PARTIAL | {file:line} | {observation} |
| ... | ... | ... | ... | ... |

## Deviations Found

### Critical (Bugs)
- {deviation description}

### Missing Implementation
- {what's not done yet}

### Approved Deviations
- {reference to deviation file}

### Undocumented Changes
- {needs /spec-deviation}

## Recommendations

1. {action item}
2. {action item}

---
*Validated by Claude Code via /spec-validate*
```

## Example

```
User: /spec-validate user-authentication

Claude: Validating user-authentication against spec...

## Phase 1: Load Specification

Loaded: .specify/specs/user-authentication/spec.md
Found 12 acceptance criteria
1 approved deviation found

## Phase 2: Implementation Analysis

### Acceptance Criteria Check

[PASS] AC1: Users can register with email/password
       - Code: src/auth/register.ts:45
       - Password hashed with bcrypt (constitution S1 compliant)

[PASS] AC2: Users can login with valid credentials
       - Code: src/auth/login.ts:23
       - Returns JWT token as specified

[FAIL] AC3: Login fails after 5 invalid attempts
       - Code: src/auth/login.ts:67
       - Expected: 5 attempts, Found: 3 attempts
       - Severity: Bug

[PARTIAL] AC4: Password reset via email
       - Code: src/auth/reset.ts
       - Email sending works, but link expiration not implemented

## Phase 3: Deviation Detection

### Critical (Bugs)
- AC3: Rate limiting threshold incorrect (3 vs 5)

### Missing Implementation
- AC4: Password reset link expiration

### Approved Deviations
- DEV-001: Using 15min token expiry instead of 1hr (performance)

## Validation Report: user-authentication

**Overall Status**: PARTIAL

### Criteria Summary
- Passed: 9/12
- Failed: 1/12
- Partial: 2/12

### Next Steps
1. Fix rate limiting bug (AC3)
2. Implement link expiration (AC4)
3. Consider spec update for AC3 if 3 attempts is intentional

Report saved to: .specify/reports/user-authentication-validate-2026-01-17.md
```

## Integration Points

- **Feeds into `/spec-debug`**: Validation failures become debugging hypotheses
- **Triggers `/spec-deviation`**: Undocumented changes need deviation logs
- **Updates memories**: Findings may update `common-bugs`
