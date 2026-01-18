# /eliminate - Scientific Process of Elimination Debugging

**Syntax:** `/eliminate [symptom_description]`

Initiate systematic elimination-based debugging using the scientific method.

## Overview

This command implements Sherlock Holmes' famous maxim: "When you have eliminated the impossible, whatever remains, however improbable, must be the truth." It uses modus tollens logic - if hypothesis H predicts outcome O, and O is not observed, then H is eliminated.

## Workflow

### Phase 1: Hypothesis Generation (2-3 minutes)

1. **Load context**
   - Read `.elimination/learned/heuristics.yaml` for matching patterns
   - Check `.elimination/learned/templates/` for domain-specific hypothesis templates
   - Review `.serena/memories/elimination_patterns.md` for project-specific patterns
   - Review `.serena/memories/debugging-lessons.md` for past insights on similar symptoms
   - Reference `.elimination/samples/` for YAML file structure examples
   - **Check for spec context**: If symptom relates to a specced feature, load `.specify/specs/{feature}/spec.md`
   - **Load spec deviations**: Check `.specify/deviations/` for known deviations

2. **Generate hypotheses** across these categories (Ishikawa/Fishbone):
   - **Code**: Logic errors, algorithm bugs, type mismatches, off-by-one errors
   - **Configuration**: Environment variables, settings, feature flags
   - **Dependencies**: Version conflicts, API changes, missing packages
   - **Data**: Invalid input, state corruption, edge cases
   - **Infrastructure**: Resource exhaustion, network issues, service availability
   - **Concurrency**: Race conditions, deadlocks, timing issues

3. **Assign initial confidence** (0.0-1.0)
   - Use learned priors from `heuristics.yaml` if pattern matches
   - Default priors: Code (0.35), Config (0.20), Dependencies (0.15), Data (0.15), Infrastructure (0.10), Concurrency (0.05)
   - **Spec-informed**: Hypotheses from spec deviations start at 0.70 (elevated confidence)

4. **Write to active session**
   - Create `.elimination/active/session.yaml` with session metadata
   - If spec context exists, add `spec_reference` and `session_type: spec_deviation_debug`
   - Write each hypothesis to `.elimination/active/hypotheses/hyp-{id}.yaml`

### Phase 2: Evidence Gathering Loop

For each hypothesis (ordered by expected information gain):

1. **Design discriminating test**
   - What observation would ELIMINATE this hypothesis if not seen?
   - Prefer tests that eliminate multiple hypotheses at once

2. **Execute test and record evidence**
   - Write to `.elimination/active/evidence/ev-{id}.yaml`
   - Include: test description, result, timestamp, source references

3. **Update confidence via Bayesian reasoning**
   ```
   P(H|E) = P(E|H) * P(H) / P(E)
   ```
   - Supporting evidence: multiply confidence by likelihood ratio (1.2-2.0)
   - Contradicting evidence: multiply by inverse ratio (0.1-0.5)

4. **Apply elimination thresholds**
   - **Hard eliminate** at confidence < 0.05 (mark as `eliminated`)
   - **Soft eliminate** at confidence < 0.25 (mark as `unlikely`)
   - **Confirm** at confidence > 0.90 (proceed to verification)

5. **Log elimination decision** to `.elimination/logs/elimination_log.yaml`

### Phase 3: Verification

1. **Implement fix** based on confirmed hypothesis
2. **Run verification tests** to confirm resolution
3. **If verified**: Mark session as `success`, proceed to learning
4. **If failed**: 
   - Consider resurrecting eliminated hypotheses
   - Expand hypothesis space with derived hypotheses
   - Return to Phase 2

### Phase 4: Learning

1. **Generate self-reflection**
   ```
   What worked? What was eliminated too early or too late?
   Which tests provided the most information gain?
   What patterns should be remembered for future debugging?
   ```

2. **Update heuristics** in `.elimination/learned/heuristics.yaml`
   - Increment success/failure counts
   - Adjust confidence priors based on outcome

3. **Archive session** to `.elimination/archive/{year}-{month}/session-{id}/`

## Convergence Criteria

Stop eliminating when ANY of:
- Leading hypothesis confidence > 0.90
- Separation margin > 0.30 between top two hypotheses
- Maximum iterations reached (default: 20)
- Information gain per iteration < 0.01

## Key Principles

1. **Soft elimination preferred**: Reduce probability, don't zero it until very confident
2. **Multiple evidence required**: Need 2-3 confirmatory tests before hard elimination
3. **Resurrection allowed**: Track rollback info to restore hypotheses if new evidence emerges
4. **Complete hypothesis space**: The true cause must be among generated hypotheses

## Example Session

```
User: /eliminate API returning 500 errors intermittently

Claude: Starting elimination-based debugging...

## Phase 1: Hypothesis Generation

Based on "intermittent 500 errors" pattern, generating hypotheses:

| ID | Hypothesis | Initial Confidence |
|----|------------|-------------------|
| H1 | Database connection pool exhaustion | 0.70 (matches learned pattern) |
| H2 | Memory leak causing OOM | 0.40 |
| H3 | Race condition in request handler | 0.35 |
| H4 | Upstream service timeout | 0.30 |
| H5 | Configuration drift between instances | 0.25 |

## Phase 2: Evidence Gathering

**Test 1**: Check DB connection metrics during error spikes
- Result: Connection count normal (< 50% pool)
- H1 confidence: 0.70 → 0.15 (contradicting evidence)
- H1 status: SOFT ELIMINATED

**Test 2**: Check memory usage patterns
- Result: Memory stable, no growth pattern
- H2 confidence: 0.40 → 0.10 (contradicting evidence)
- H2 status: SOFT ELIMINATED

**Test 3**: Check error correlation with concurrent requests
- Result: Errors correlate with request count > 100/sec
- H3 confidence: 0.35 → 0.75 (supporting evidence)

**Test 4**: Add mutex logging to request handler
- Result: Lock contention detected in shared cache access
- H3 confidence: 0.75 → 0.92 (strong confirmation)
- H3 status: CONFIRMED

## Phase 3: Verification

Implementing fix: Replace shared cache with request-scoped cache
Running verification: 10,000 requests at 150/sec
Result: Zero 500 errors

✅ Resolution verified

## Phase 4: Learning

Self-reflection: 
- Pattern "intermittent errors correlating with load" strongly indicates concurrency issues
- DB connection hypothesis could have been eliminated faster by checking metrics first
- Adding heuristic: "When errors correlate with request rate, prioritize concurrency hypotheses"

Updating heuristics.yaml with new pattern...
Archiving session to .elimination/archive/2026-01/session-001/
```
