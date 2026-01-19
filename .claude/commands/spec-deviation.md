# /spec-deviation - Log Intentional Spec Deviation

**Syntax:** `/spec-deviation [feature_name] [--reason=<category>]`

Document an intentional departure from the specification with rationale.

## Overview

When implementation intentionally differs from spec, this creates a formal
deviation log. Deviations are tracked so that:

1. `/spec-validate` doesn't flag them as bugs
2. Future developers understand why code differs from spec
3. Deviations can be reviewed and reconsidered later
4. Debugging can distinguish bugs from intentional changes

## Before Using This Command

Fetch latest documentation if unsure about API/behavior:
- Spec-Kit: `mcp__context7__resolve-library-id("github spec-kit")`

## Deviation Categories

| Category | Use When |
|----------|----------|
| `technical_constraint` | Spec is ideal but technically infeasible |
| `user_request` | User explicitly requested different behavior |
| `performance_optimization` | Spec behavior has unacceptable performance |
| `security_requirement` | Security considerations override spec |
| `temporary_workaround` | Known issue, plan to align with spec later |

## Workflow

### Phase 1: Verification

1. **Confirm spec exists**
   - Load `.specify/specs/{feature_name}/spec.md`
   - Identify which section is being deviated from

2. **Check past decisions**
   - Read `.serena/memories/decision-log.md` for related architectural decisions
   - Past decisions may inform why deviation is needed or reveal prior discussions

3. **Verify this isn't a bug**
   - Ask: "Is this deviation intentional?"
   - If unintentional, redirect to bug fixing

4. **Check constitution**
   - Ensure deviation doesn't violate constitution.md
   - Constitution violations cannot be approved

### Phase 2: Documentation

1. **Create deviation file**
   ```
   .specify/deviations/{feature_name}-{id}.md
   ```

2. **Fill deviation template**
   ```markdown
   # Deviation: {feature_name}-{id}

   ## Metadata
   | Field | Value |
   |-------|-------|
   | **Feature** | {feature_name} |
   | **Spec Section** | {section reference} |
   | **Category** | {category} |
   | **Date** | {YYYY-MM-DD} |
   | **Status** | `approved` / `temporary` / `under_review` |

   ## Spec Says
   [Quote from specification]

   ## Implementation Does
   [Description of actual behavior]

   ## Rationale
   [Why this deviation is acceptable/necessary]

   ## Impact
   - [Impact 1]
   - [Impact 2]

   ## Alternatives Considered
   1. [Alternative 1] - rejected because [reason]
   2. [Alternative 2] - rejected because [reason]

   ## Review Plan
   - [ ] Review by: {date}
   - [ ] Conditions for removing deviation: [conditions]

   ## Approval
   - Approved by: {approver}
   - Date: {date}
   ```

3. **Link to spec**
   - Add deviation reference to spec file (if applicable)

### Phase 3: Integration

1. **Update decision log**
   - Add entry to `decision-log` memory
   - Include deviation ID and rationale summary

2. **Notify validation**
   - Deviation file will be read by `/spec-validate`
   - Won't be flagged as bug in future validations

3. **Set review reminder**
   - Temporary deviations should have review dates
   - Prompt for review when date approaches

## Example

```
User: /spec-deviation user-authentication --reason=performance_optimization

Claude: Logging intentional spec deviation...

## Phase 1: Verification

Spec loaded: .specify/specs/user-authentication/spec.md

What section of the spec is being deviated from?

User: The session token expiry - spec says 1 hour but we're using 15 minutes

Claude: Understood. Let me verify this is intentional...

Is this deviation intentional? (not a bug to fix)

User: Yes, we need shorter tokens for security on mobile

## Phase 2: Documentation

Creating deviation file...

### Deviation: user-authentication-001

**Spec Says**: Session tokens expire after 1 hour

**Implementation Does**: Session tokens expire after 15 minutes

**Category**: performance_optimization (also security_requirement)

**Rationale**:
- Mobile clients operate on untrusted networks
- Shorter token lifetime reduces exposure window
- Refresh token flow handles re-authentication seamlessly

**Impact**:
- More frequent token refreshes
- Slightly higher auth server load
- Better security posture on mobile

## Phase 3: Integration

Deviation logged: .specify/deviations/user-authentication-001.md
Added to decision-log memory

The deviation will now be recognized by /spec-validate and won't be flagged as a bug.

### Next Steps
1. Consider updating spec to make 15min the default
2. Or keep as approved deviation with review date
3. Document in API docs for client developers

Set review date? [Optional]

User: Review in 6 months

Claude: Review date set: 2026-07-17
```

## Temporary vs Permanent Deviations

| Type | Status | Review Required |
|------|--------|-----------------|
| Temporary | `temporary` | Yes, with specific date |
| Approved | `approved` | Optional, periodic |
| Under Review | `under_review` | Yes, pending decision |

## Integration Points

- **Read by `/spec-validate`**: Prevents false positive bug detection
- **Read by `/spec-debug`**: Distinguishes bugs from intentional changes
- **Updates `decision-log`**: Creates paper trail for decisions
- **May update spec**: If deviation becomes permanent standard
