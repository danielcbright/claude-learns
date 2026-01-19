# /claude-learns.spec-create - Create Feature Specification

**Syntax:** `/claude-learns.spec-create [feature_name] [--type=feature|bug-fix|refactor]`

Create a complete specification for a feature, bug fix, or refactoring effort.

## Overview

Specifications define expected behavior before implementation. This creates a
contract that can be validated and used for debugging when behavior deviates.

## Before Using This Command

Fetch latest documentation if unsure about API/behavior:
- Spec-Kit: `mcp__context7__resolve-library-id("github spec-kit")`
- Serena: `mcp__context7__resolve-library-id("serena mcp")`

## Workflow

### Phase 1: Context Gathering

1. **Check existing specs**
   - List `.specify/specs/` to avoid duplicates
   - Read related specs for consistency

2. **Review constitution**
   - Read `.specify/memory/constitution.md` for invariants
   - Ensure spec doesn't violate core principles

3. **Load relevant memories**
   - Read `decision-log` for related past decisions
   - Check `common-bugs` for known issues in this area

4. **Check external dependencies**
   - If feature involves external APIs, read `.serena/memories/tool-documentation.md` for reference links
   - Verify you have current documentation before specifying integration behavior

### Phase 2: Spec Creation

1. **Select template** based on `--type`:
   - `feature`: `.specify/templates/feature-spec.md`
   - `bug-fix`: `.specify/templates/bug-fix-spec.md`
   - `refactor`: `.specify/templates/refactor-spec.md`

2. **Create spec directory**
   ```
   .specify/specs/{feature_name}/
   ├── spec.md           # Main specification
   ├── examples/         # Code examples (if needed)
   └── diagrams/         # Architecture diagrams (if needed)
   ```

3. **Fill in template sections**
   - Ask clarifying questions for unclear requirements
   - Reference existing code for technical design
   - Define clear, testable acceptance criteria

4. **Cross-reference**
   - Link to related specs
   - Reference constitution principles if applicable
   - Note dependencies on other features

### Phase 3: Validation

1. **Check completeness**
   - All template sections filled or marked N/A
   - Acceptance criteria are specific and testable
   - Edge cases documented

2. **Technical feasibility**
   - Proposed design is implementable
   - No constitution violations
   - Dependencies are available

3. **Generate summary**
   ```
   ## Spec Created: {feature_name}

   **Type**: {type}
   **Location**: .specify/specs/{feature_name}/spec.md
   **Status**: draft

   ### Key Points
   - [Summary point 1]
   - [Summary point 2]

   ### Next Steps
   1. Review and approve spec
   2. Implement following spec
   3. Validate with `/claude-learns.spec-validate {feature_name}`
   ```

## Example

```
User: /claude-learns.spec-create user-authentication --type=feature

Claude: Creating feature specification for user-authentication...

## Phase 1: Context Gathering

Checking existing specs... none found for authentication.
Reading constitution... found security invariant S1 (all auth must use bcrypt).
Checking decision-log... found preference for JWT tokens.

## Phase 2: Spec Creation

I have some questions to clarify the requirements:

1. Authentication method: OAuth, JWT, session-based, or combination?
2. Supported identity providers: Google, GitHub, email/password?
3. Session duration and refresh token strategy?

[User provides answers]

Creating spec at .specify/specs/user-authentication/spec.md...

## Spec Created: user-authentication

**Type**: feature
**Location**: .specify/specs/user-authentication/spec.md
**Status**: draft

### Key Points
- JWT-based authentication with refresh tokens
- Google and email/password providers
- Compliant with constitution S1 (bcrypt for passwords)

### Next Steps
1. Review spec for completeness
2. Implement authentication module
3. Validate with `/claude-learns.spec-validate user-authentication`
```

## Integration Points

- **With `/claude-learns.eliminate`**: Specs provide expected behavior for hypothesis generation
- **With `/claude-learns.spec-debug`**: Debugging uses spec as source of truth
- **With memories**: Decisions are logged to `decision-log`
