# /claude-learns.spec-debug - Debug Using Specification as Source of Truth

**Syntax:** `/claude-learns.spec-debug [feature_name] [symptom_description]`

Debug an issue by comparing implementation against its specification,
generating hypotheses from deviations, and integrating with the elimination system.

## Overview

This is the key integration point between spec-kit and elimination debugging.
When a feature has unexpected behavior, spec-debug:

1. Loads the feature's specification
2. Compares spec expectations vs actual behavior
3. Generates hypotheses from deviations (with elevated confidence)
4. Initiates elimination debugging with spec context

## Before Using This Command

Fetch latest documentation if unsure about API/behavior:
- Spec-Kit: `mcp__context7__resolve-library-id("github spec-kit")`
- Serena: `mcp__context7__resolve-library-id("serena mcp")`

## Workflow

### Phase 1: Spec Loading

1. **Load feature specification**
   - Read `.specify/specs/{feature_name}/spec.md`
   - If spec doesn't exist, offer to create one first

2. **Parse behavioral expectations**
   - Extract "Expected Behavior" sections
   - Note acceptance criteria
   - Identify edge case handling

3. **Load deviation history**
   - Check approved deviations
   - Filter for feature-specific deviations

### Phase 2: Spec vs Reality Analysis

1. **Quick validation**
   - Run targeted checks against symptom area
   - Compare actual behavior to spec

2. **Identify spec deviations**
   ```
   ## Spec Deviations Detected

   | Spec Says | Reality | Deviation Type |
   |-----------|---------|----------------|
   | [Expected] | [Actual] | bug/missing/undocumented |
   ```

3. **Categorize deviations by symptom relevance**
   - Directly related to reported symptom
   - Potentially related
   - Unrelated (note for later)

### Phase 3: Hypothesis Generation (Spec-Informed)

1. **Generate hypotheses from spec deviations**

   For each relevant deviation:
   ```yaml
   hypothesis:
     id: H{n}
     description: "Spec deviation: {expected} vs {actual}"
     source: spec_deviation
     confidence: 0.70  # Elevated from default
     spec_reference: .specify/specs/{feature}/spec.md#{section}
   ```

2. **Add standard hypotheses**
   - Include non-spec hypotheses (config, dependencies, etc.)
   - Use lower default confidence (0.35)

3. **Prioritize by information value**
   - Spec deviations first (higher confidence = test first)
   - Then by expected information gain

### Phase 4: Elimination Integration

1. **Create elimination session with spec context**
   ```yaml
   session:
     type: spec_deviation_debug
     feature: {feature_name}
     symptom: {symptom_description}
     spec_reference: .specify/specs/{feature_name}/spec.md
     deviation_count: {n}
   ```

2. **Hand off to elimination system**
   - Write session to `.elimination/active/session.yaml`
   - Write hypotheses to `.elimination/active/hypotheses/`
   - Continue with evidence gathering phase

3. **Use spec as evidence source**
   - Spec defines expected behavior
   - Deviations from spec are strong evidence
   - Compliance with spec is evidence against code bugs

### Phase 5: Resolution

When root cause is found:

1. **If spec deviation was the cause**
   - Fix implementation to match spec, OR
   - Update spec if implementation is correct (with `/claude-learns.spec-deviation`)

2. **Update debugging lessons**
   - Add to `debugging-lessons` memory
   - Update `common-bugs` if pattern is recurring

3. **Archive session**
   - Include spec reference in archive
   - Track spec-based hypothesis success rate

## Example

```
User: /claude-learns.spec-debug user-authentication "login fails with correct credentials"

Claude: Starting spec-informed debugging...

## Phase 1: Spec Loading

Loaded: .specify/specs/user-authentication/spec.md
Feature has 12 acceptance criteria
1 approved deviation on record

## Phase 2: Spec vs Reality Analysis

Checking authentication flow against spec...

### Spec Deviations Detected

| Spec Says | Reality | Type |
|-----------|---------|------|
| bcrypt with cost 12 | bcrypt with cost 10 | deviation |
| Case-insensitive email | Case-sensitive comparison | bug |
| 5 login attempts | 3 attempts before lockout | deviation |

Deviation #2 directly relates to symptom (case-sensitive email matching).

## Phase 3: Hypothesis Generation

| ID | Hypothesis | Confidence | Source |
|----|------------|------------|--------|
| H1 | Case-sensitive email comparison | 0.85 | spec_deviation (directly related) |
| H2 | Email normalization missing | 0.70 | spec_deviation |
| H3 | Database collation mismatch | 0.40 | standard |
| H4 | Password encoding issue | 0.30 | standard |

## Phase 4: Elimination Integration

Creating spec-informed elimination session...

Session type: spec_deviation_debug
Spec reference: .specify/specs/user-authentication/spec.md

### Evidence Gathering

**Test 1**: Check email comparison in login code
- Found: `email === storedEmail` (strict equality)
- Spec says: case-insensitive comparison
- H1 confidence: 0.85 → 0.95 (CONFIRMED)

## Resolution

Root cause: Login uses case-sensitive email comparison.
User registered as "User@Email.com" but logging in with "user@email.com".

**Fix**: Change to `email.toLowerCase() === storedEmail.toLowerCase()`

This was a spec deviation - implementation should be updated to match spec.

### Learning

Added to debugging-lessons:
- Pattern: "auth fails with correct credentials" → check case sensitivity
```

## When to Use

| Scenario | Command |
|----------|---------|
| Bug in specced feature | `/claude-learns.spec-debug` |
| Bug without spec | `/claude-learns.debug` or `/claude-learns.eliminate` |
| Complex multi-cause issue | `/claude-learns.eliminate` (may call `/claude-learns.spec-debug` internally) |
| Validating implementation | `/claude-learns.spec-validate` |

## Integration Points

- **Calls `/claude-learns.eliminate`**: For the evidence gathering and elimination phases
- **Uses specs**: Reads from `.specify/specs/`
- **Updates memories**: Writes to `debugging-lessons`, `common-bugs`
- **May trigger `/claude-learns.spec-deviation`**: If intentional deviation found
