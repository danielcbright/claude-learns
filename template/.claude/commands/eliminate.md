# /eliminate - Scientific Process of Elimination Debugging

**Syntax:** `/eliminate [symptom_description]`

Initiate systematic elimination-based debugging using the scientific method.

## Overview

This command implements Sherlock Holmes' famous maxim: "When you have eliminated the impossible, whatever remains, however improbable, must be the truth." It uses modus tollens logic - if hypothesis H predicts outcome O, and O is not observed, then H is eliminated.

---

## Script-Enforced Process

**IMPORTANT:** This process is enforced by scripts to prevent deviation.

### Available Scripts

Located in `.claude/scripts/elimination/`:

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `eliminate_init.py` | Initialize session | Start of investigation |
| `eliminate_research.py` | Research hypotheses online | Before/during testing |
| `eliminate_next.py` | Get next hypothesis to test | After each checkpoint |
| `eliminate_checkpoint.py` | Record test, update confidences | After each test |
| `eliminate_status.py` | View current state | Any time |
| `eliminate_archive.py` | Archive completed session | End of investigation |

### Script-Driven Workflow

```bash
# 1. Initialize session with hypotheses
python .claude/scripts/elimination/eliminate_init.py \
  --symptom "API returning 500 errors intermittently" \
  --interactive

# 2. RESEARCH: Get search queries and URLs for online research
python .claude/scripts/elimination/eliminate_research.py --all

# 3. Use WebSearch/WebFetch to investigate, then record findings
python .claude/scripts/elimination/eliminate_research.py \
  --hypothesis H1 \
  --record '{"source": "GitHub Issue #1234", "summary": "Known race condition"}' \
  --boost 0.15

# 4. Get first hypothesis to test (research may have changed rankings)
python .claude/scripts/elimination/eliminate_next.py

# 5. After testing, record checkpoint (MUST update ALL hypotheses)
python .claude/scripts/elimination/eliminate_checkpoint.py \
  --test "Check DB connection pool" \
  --evidence "Pool at 45%, normal" \
  --updates "H1:0.15,H2:0.42,H3:0.38,H4:0.30,H5:0.25"

# 6. Optionally research the next hypothesis before testing
python .claude/scripts/elimination/eliminate_research.py --hypothesis H2

# 7. Get next hypothesis (script determines this, not you!)
python .claude/scripts/elimination/eliminate_next.py

# 8. Repeat steps 5-7 until convergence

# 9. Archive when done
python .claude/scripts/elimination/eliminate_archive.py \
  --outcome success \
  --confirmed H3 \
  --root-cause "Race condition in shared cache"
```

### Process Enforcement

The scripts enforce correct behavior:

- **`eliminate_checkpoint.py`** will **REFUSE** to proceed unless ALL active hypotheses have updated confidences
- **`eliminate_next.py`** tells you EXACTLY which hypothesis to test - removes your discretion
- **`eliminate_status.py`** validates process adherence and flags violations

---

## Research Phase

**IMPORTANT:** Before testing hypotheses, research online to find supporting evidence. This can significantly boost confidence and save testing time.

### When to Research

| Timing | Benefit |
|--------|---------|
| After hypothesis generation | Validate hypotheses, find known issues |
| Before testing a hypothesis | Find existing solutions, known fixes |
| When hypothesis has high confidence | Seek confirmation from others |
| When stuck | Discover approaches you haven't tried |

### Research Sources

The `eliminate_research.py` script generates search queries for:

1. **GitHub Issues** - Find similar bugs, discussions, fixes
2. **Stack Overflow** - Community solutions and explanations
3. **Web Search** - Blog posts, tutorials, documentation

### Using the Research Script

```bash
# Generate research plan for all hypotheses
python .claude/scripts/elimination/eliminate_research.py --all

# Research specific hypothesis
python .claude/scripts/elimination/eliminate_research.py --hypothesis H1

# Output as JSON (for programmatic use)
python .claude/scripts/elimination/eliminate_research.py --all --json
```

### Executing Research with Claude Tools

After getting search queries from the script, use Claude's tools:

```
# Web Search for general queries
WebSearch: "race condition async cache Node.js"

# Fetch GitHub Issues
WebFetch: "https://github.com/search?q=race+condition+cache&type=issues"

# Fetch Stack Overflow
WebFetch: "https://stackoverflow.com/search?q=race+condition+node+cache"
```

### Recording Research Findings

**IMPORTANT:** Record findings to update hypothesis confidence.

```bash
# Record finding with confidence boost
python .claude/scripts/elimination/eliminate_research.py \
  --hypothesis H1 \
  --record '{
    "source": "GitHub Issue #1234",
    "url": "https://github.com/owner/repo/issues/1234",
    "summary": "Exact same error, confirmed race condition in cache layer",
    "relevance": "high",
    "has_fix": true
  }' \
  --boost 0.15
```

### Confidence Boost Guidelines

| Finding Quality | Boost |
|-----------------|-------|
| Exact error message match + same stack | 0.15-0.20 |
| Similar issue in same framework | 0.10-0.15 |
| Related issue, different context | 0.05-0.10 |
| General information, tangentially related | 0.00-0.05 |

**Max boost per finding: 0.20** (to prevent over-reliance on research)

### Research Best Practices

1. **Search before testing** - Don't reinvent the wheel
2. **Include tech stack** - "Node.js Express" not just "server error"
3. **Try multiple queries** - Error messages, symptoms, hypothesis descriptions
4. **Check issue status** - Closed issues often have solutions
5. **Note versions** - Solutions may be version-specific
6. **Record everything** - Even negative findings are valuable

---

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

---

## IMPORTANT: Process Adherence Rules

**YOU MUST follow the systematic process. Do not deviate.**

### After Eliminating a Hypothesis

When you eliminate a hypothesis (soft or hard):

1. **DO NOT** immediately start testing a new idea that just occurred to you
2. **DO NOT** jump to implementing a fix until convergence criteria are met
3. **DO** proceed to the NEXT hypothesis on your ranked list
4. **DO** update the status table and continue the Evidence Gathering Loop

### State Machine (Follow This Exactly)

```
┌─────────────────────────────────────────────────────────────────┐
│                    ELIMINATION STATE MACHINE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START → Generate Hypotheses → Rank by Information Gain        │
│                                       │                         │
│                                       ▼                         │
│                         ┌─────────────────────────┐             │
│                         │  Pick NEXT hypothesis   │◄────────┐   │
│                         │  from ranked list       │         │   │
│                         └───────────┬─────────────┘         │   │
│                                     │                       │   │
│                                     ▼                       │   │
│                         ┌─────────────────────────┐         │   │
│                         │  Design & execute test  │         │   │
│                         └───────────┬─────────────┘         │   │
│                                     │                       │   │
│                                     ▼                       │   │
│                         ┌─────────────────────────┐         │   │
│                         │  Update ALL hypothesis  │         │   │
│                         │  confidences            │         │   │
│                         └───────────┬─────────────┘         │   │
│                                     │                       │   │
│                                     ▼                       │   │
│                         ┌─────────────────────────┐         │   │
│                    NO   │  Convergence criteria   │  NO     │   │
│              ┌──────────┤  met?                   ├─────────┘   │
│              │          └───────────┬─────────────┘             │
│              │                      │ YES                       │
│              ▼                      ▼                           │
│   ┌───────────────────┐   ┌─────────────────────┐              │
│   │ More hypotheses?  │   │  VERIFY top hypothesis│              │
│   │ If NO: expand     │   │  (implement & test)  │              │
│   │ hypothesis space  │   └─────────────────────┘              │
│   └───────────────────┘                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Anti-Patterns to Avoid

❌ **Shiny Object Syndrome**: "While testing H1, I noticed something about X, let me investigate that instead..."
   → STOP. Log the observation as a potential new hypothesis, continue with current test.

❌ **Premature Fix Attempt**: "H1 is eliminated, and I have a hunch about H3, let me just try fixing it..."
   → STOP. You must gather evidence on H2 first (unless H3 is next in your ranked list).

❌ **Abandoning the List**: "The first hypothesis was wrong, let me think of completely new possibilities..."
   → STOP. You already generated hypotheses in Phase 1. Work through them systematically.

❌ **Skipping Updates**: Eliminating H1 without updating the confidence scores of ALL hypotheses.
   → Evidence often affects multiple hypotheses. Update all confidences after each test.

### Checkpoint After Each Test

After EVERY test, explicitly state:

```
## Test {N} Complete

**Evidence**: {what was observed}

**Hypothesis Updates**:
| ID | Hypothesis | Previous | New | Status |
|----|------------|----------|-----|--------|
| H1 | ...        | 0.70     | 0.15| SOFT ELIMINATED |
| H2 | ...        | 0.40     | 0.45| active |
| H3 | ...        | 0.35     | 0.35| active |

**Convergence Check**:
- Leading hypothesis: H2 (0.45)
- Separation margin: 0.10 (need > 0.30)
- Status: NOT CONVERGED

**Next Action**: Test H2 (highest remaining confidence)
```

### If You Feel the Urge to Deviate

1. **Pause** and acknowledge the urge
2. **Log** the new idea as a potential hypothesis addition
3. **Ask yourself**: "Have I completed the current Evidence Gathering Loop iteration?"
4. **If NO**: Complete the current iteration first
5. **If YES and idea is valuable**: Add hypothesis via `/hypothesis` command, re-rank, continue

### User Can Override

If the user explicitly says "skip to H5" or "try this instead", follow their direction. But without explicit user override, **stay on the systematic path**.

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
