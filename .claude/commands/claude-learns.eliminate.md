# /eliminate - Scientific Process of Elimination Debugging

**Syntax:** `/claude-learns.eliminate [symptom_description]`

Initiate systematic elimination-based debugging using the scientific method with subagent orchestration.

---

## Ralph-Loop Integration

**CRITICAL**: Before starting elimination, check if this is being called from a ralph session.

### Detect Ralph Context

```python
# Check for active ralph session
list_memories()

# Look for any memory named "ralph-*" with status: paused-elimination
# If found, this elimination was triggered by ralph being stuck
```

If ralph context detected:
1. **Read ralph session memory** to understand what was being attempted
2. **Note the iteration** where ralph got stuck
3. **After fix**: Update ralph session memory with:
   - Fix description
   - Patterns learned
   - Status: `active` (signals ralph to resume)

### Example Ralph Context

```yaml
# From ralph session memory
Session: feature-auth-system
Status: paused-elimination
Current Iteration: 5
Blocker:
  symptom: "Tests failing with ECONNREFUSED"
  error_count: 3
  first_seen_iteration: 3
```

When elimination completes, write back:

```python
edit_memory("ralph-feature-auth-system", 
  old="Status: paused-elimination",
  new="Status: active",
  mode="literal")

edit_memory("ralph-feature-auth-system",
  old="Blocker:",
  new="""Blocker: RESOLVED
Resolution:
  symptom: "Tests failing with ECONNREFUSED"
  root_cause: "Mock server not started before tests"
  fix: "Added beforeAll() hook to start mock server"
  iteration_resolved: 5
  
Patterns Discovered:""",
  mode="literal")
```

---

## Overview

This command implements Sherlock Holmes' famous maxim: "When you have eliminated the impossible, whatever remains, however improbable, must be the truth."

**Architecture**: You (Claude) act as the **orchestrator**, delegating work to specialized subagents via the Task tool. Each subagent completes its phase and returns control to you.

---

## Orchestrator Pattern

**IMPORTANT:** You are the orchestrator. Do NOT do all the work yourself. Delegate to subagents.

### Your Role as Orchestrator

1. **Initialize** the session via script
2. **Launch subagents** for specific tasks
3. **Validate** subagent outputs via script gates
4. **Coordinate** the iterative loop
5. **Make decisions** on convergence and next steps
6. **Archive** the session when complete

### Available Subagents

| Agent | Purpose | Launch Via |
|-------|---------|------------|
| **HypothesisAgent** | Generate hypotheses from context | `Task(subagent_type="general-purpose")` |
| **ResearchAgent** | Search web for prior art | `Task(subagent_type="general-purpose")` |
| **CodeAnalysisAgent** | Analyze code paths with Serena | `Task(subagent_type="general-purpose")` |
| **TestRunnerAgent** | Execute discriminating tests | `Task(subagent_type="general-purpose")` |

### Script Gates (Enforced Between Phases)

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `eliminate_init.py` | Initialize session | Before HypothesisAgent |
| `eliminate_next.py` | Get next hypothesis | Before each test iteration |
| `eliminate_checkpoint.py` | Record test, update confidences | After TestRunnerAgent |
| `eliminate_archive.py` | Archive completed session | After convergence |

---

## Orchestrator Workflow

### Phase 0: Check Ralph Context (FIRST)

```python
# ALWAYS check for ralph context before anything else
list_memories()

# Look for memories matching "ralph-*" pattern
# Read any that have status: paused-elimination

for memory in memories:
    if memory.startswith("ralph-") and "paused-elimination" in read_memory(memory):
        # This elimination was triggered by ralph
        ralph_context = read_memory(memory)
        # Extract: session_name, iteration, blocker symptom
        # Use this context to inform hypothesis generation
```

If ralph context found:
- Note the session name for later update
- Use the blocker symptom as the primary symptom
- Consider patterns from ralph's progress log

---

### Phase 1: Initialize

```bash
# Run BEFORE launching HypothesisAgent
python .claude/scripts/elimination/eliminate_init.py \
  --symptom "$ARGUMENTS" \
  --interactive
```

If session already exists, ask user: resume or start fresh?

### Phase 2: Launch HypothesisAgent

```
Task(
  subagent_type="general-purpose",
  description="Generate elimination hypotheses",
  prompt="""
You are a HypothesisAgent for elimination debugging.

SYMPTOM: {symptom}
PROJECT: {project_path}

YOUR TASK:
1. Read .elimination/learned/heuristics.yaml for matching patterns
2. Read .elimination/config.yaml for confidence thresholds
3. Read .serena/memories/elimination_patterns.md for project patterns
4. Generate 3-7 hypotheses across categories:
   - Code: Logic errors, bugs, type mismatches
   - Configuration: Env vars, settings, feature flags
   - Dependencies: Version conflicts, API changes
   - Data: Invalid input, state corruption, edge cases
   - Infrastructure: Resource exhaustion, network issues
   - Concurrency: Race conditions, deadlocks
5. Assign initial confidence (use heuristics priors if available)
6. Write each hypothesis to .elimination/active/hypotheses/hyp-{id}.yaml

RETURN FORMAT:
## Hypotheses Generated

| ID | Category | Description | Confidence |
|----|----------|-------------|------------|
| H1 | {cat} | {desc} | {score} |
| H2 | {cat} | {desc} | {score} |
...

Files written: {list of files created}

Do NOT proceed to testing. Return control to orchestrator.
"""
)
```

### Phase 3: Validate Hypotheses (GATE)

After HypothesisAgent returns:

```bash
# Verify hypotheses were written
ls .elimination/active/hypotheses/
```

If no files exist, the gate fails. Ask HypothesisAgent to retry.

### Phase 4: Iterative Loop

```
LOOP until convergence:

  # 4a. Get next hypothesis to test
  python .claude/scripts/elimination/eliminate_next.py

  # Parse output to get: hypothesis_id, description, confidence

  # 4b. (Optional) Launch ResearchAgent
  Task(
    subagent_type="general-purpose",
    description="Research hypothesis {id}",
    prompt="""
You are a ResearchAgent for elimination debugging.

HYPOTHESIS: {id} - {description}
SYMPTOM: {symptom}
TECH STACK: {inferred from project}

YOUR TASK:
1. Use WebSearch to find similar issues, known bugs
2. Search GitHub Issues: "{error message} {framework}"
3. Search Stack Overflow: "{symptom} {tech stack}"
4. If relevant findings, record them:
   python .claude/scripts/elimination/eliminate_research.py \
     --hypothesis {id} \
     --record '{"source": "URL", "summary": "finding", "relevance": "high"}' \
     --boost {0.05-0.15}

RETURN FORMAT:
## Research Summary for {id}

- Sources checked: {count}
- Relevant findings: {count}
- Confidence boost applied: {total}
- Key insight: {one sentence}

Do NOT proceed to testing. Return control to orchestrator.
"""
  )

  # 4c. Launch CodeAnalysisAgent
  Task(
    subagent_type="general-purpose",
    description="Analyze code for hypothesis {id}",
    prompt="""
You are a CodeAnalysisAgent for elimination debugging.

HYPOTHESIS: {id} - {description}
SYMPTOM: {symptom}

YOUR TASK:
1. Use find_symbol() to locate relevant code
2. Use find_referencing_symbols() to trace call chains
3. Use get_symbols_overview() to understand file structure
4. Identify patterns that could cause hypothesized issue
5. Determine what test would ELIMINATE this hypothesis

RETURN FORMAT:
## Code Analysis for {id}

### Relevant Files
- {file}:{line} - {why relevant}

### Suspicious Patterns
- {pattern description}

### Recommended Test
{description of discriminating test}
- If hypothesis TRUE, expect: {outcome}
- If hypothesis FALSE, expect: {outcome}

Do NOT run tests or modify code. Return control to orchestrator.
"""
  )

  # 4d. Launch TestRunnerAgent
  Task(
    subagent_type="general-purpose",
    description="Execute test for hypothesis {id}",
    prompt="""
You are a TestRunnerAgent for elimination debugging.

HYPOTHESIS: {id} - {description}
TEST TO RUN: {from CodeAnalysisAgent recommendation}
EXPECTED IF TRUE: {outcome}
EXPECTED IF FALSE: {outcome}

YOUR TASK:
1. Execute the discriminating test via Bash
2. Capture all relevant output (logs, errors, metrics)
3. Compare result to expected outcomes
4. Determine if evidence supports or contradicts hypothesis

RETURN FORMAT:
## Test Result for {id}

### Test Executed
{command or procedure}

### Output
```
{relevant output, truncated if long}
```

### Interpretation
- Result: {SUPPORTS | CONTRADICTS | NEUTRAL}
- Evidence: {brief summary}
- Confidence recommendation: {old} → {new}

Suggested updates for ALL hypotheses:
{id}:{new_confidence}, {id2}:{confidence2}, ...

Do NOT update files directly. Return control to orchestrator.
"""
  )

  # 4e. Record checkpoint (GATE)
  python .claude/scripts/elimination/eliminate_checkpoint.py \
    --test "{test description}" \
    --evidence "{evidence summary}" \
    --updates "{H1:conf1,H2:conf2,...}"

  # 4f. Check convergence
  # Read checkpoint output for:
  # - Leading hypothesis confidence (> 0.90 = converged)
  # - Separation margin (> 0.30 = converged)
  # - Iteration count (> 20 = max reached)

  IF converged: break loop
  IF max iterations: ask user to continue or stop
```

### Phase 5: Verification

When convergence reached:

1. Announce confirmed hypothesis
2. Launch TestRunnerAgent to implement/verify fix
3. Run verification tests
4. If fix works: proceed to archive
5. If fix fails: consider resurrecting eliminated hypotheses

### Phase 6: Archive

```bash
python .claude/scripts/elimination/eliminate_archive.py \
  --outcome success \
  --confirmed {hypothesis_id} \
  --root-cause "{description}"
```

---

## Convergence Criteria

Stop the loop when ANY of:
- Leading hypothesis confidence > 0.90
- Separation margin > 0.30 between top two
- Maximum iterations reached (default: 20)
- User requests stop

---

## Anti-Patterns to Avoid

As orchestrator, do NOT:

❌ **Do the work yourself** - Always delegate to subagents
❌ **Skip script gates** - Gates enforce process
❌ **Launch multiple agents in parallel** - One at a time, validate between
❌ **Let subagents chain** - Each returns to you, you decide next step
❌ **Ignore subagent failures** - Retry or ask user

---

## Example Orchestration Session

```
User: /eliminate API returning 500 errors intermittently

Orchestrator: Starting elimination debugging session...

## Phase 1: Initialize
Running eliminate_init.py...
Session created: .elimination/active/session.yaml

## Phase 2: Generate Hypotheses
Launching HypothesisAgent...

[Task tool call to HypothesisAgent]

HypothesisAgent returned:
| ID | Category | Description | Confidence |
|----|----------|-------------|------------|
| H1 | Infrastructure | DB connection pool exhaustion | 0.70 |
| H2 | Code | Memory leak in request handler | 0.40 |
| H3 | Concurrency | Race condition in cache | 0.35 |
| H4 | Dependencies | Upstream service timeout | 0.30 |
| H5 | Configuration | Inconsistent config across instances | 0.25 |

## Phase 3: Validate (GATE)
✅ 5 hypothesis files created

## Phase 4: Iterative Loop

### Iteration 1
eliminate_next.py says: Test H1 (0.70)

Launching CodeAnalysisAgent for H1...
[Task tool call]

CodeAnalysisAgent returned:
- Relevant: src/db/pool.ts:42-78
- Test: Check connection count during error spike
- If TRUE: connections > 90% pool
- If FALSE: connections normal

Launching TestRunnerAgent for H1...
[Task tool call]

TestRunnerAgent returned:
- Test: SELECT count(*) from pg_stat_activity
- Result: 23/100 connections (23%)
- Interpretation: CONTRADICTS H1
- Recommendation: H1: 0.70→0.12, H3: 0.35→0.45

Recording checkpoint (GATE)...
✅ Checkpoint recorded

Convergence check: H3 leading at 0.45, not converged

### Iteration 2
eliminate_next.py says: Test H3 (0.45)

[...continues until convergence...]

## Phase 5: Verification
H3 confirmed at 0.92 - Race condition in cache
Implementing fix: Add mutex to cache access
Verification test: 10,000 requests at 150/sec → 0 errors

## Phase 6: Archive
✅ Session archived to .elimination/archive/2026-01/

## Summary
Root cause: Race condition in shared cache (H3)
Iterations: 4
Hypotheses eliminated: H1, H2, H4, H5
Fix verified: Yes
```

---

## Quick Reference

```bash
# Initialize (run first)
python .claude/scripts/elimination/eliminate_init.py --symptom "..." --interactive

# Get next hypothesis (script decides, not you)
python .claude/scripts/elimination/eliminate_next.py

# Record research findings
python .claude/scripts/elimination/eliminate_research.py --hypothesis H1 --record '{...}' --boost 0.1

# Record test checkpoint (GATE - required after each test)
python .claude/scripts/elimination/eliminate_checkpoint.py --test "..." --evidence "..." --updates "H1:0.1,H2:0.5,..."

# Check status anytime
python .claude/scripts/elimination/eliminate_status.py

# Archive when done
python .claude/scripts/elimination/eliminate_archive.py --outcome success --confirmed H3 --root-cause "..."
```

---

## Resuming an Existing Session

If `.elimination/active/session.yaml` exists:

1. Run `eliminate_status.py` to see current state
2. Ask user: "Active session found. Resume or start fresh?"
3. If resume: continue from last checkpoint
4. If fresh: archive current session first, then initialize new

---

## Returning to Ralph (After Completion)

If this elimination was triggered from a ralph session:

### 1. Update Ralph Session Memory

```python
# Read current ralph session
read_memory("ralph-{session_name}")

# Update status and add resolution
edit_memory("ralph-{session_name}",
  old="Status: paused-elimination",
  new="Status: active",
  mode="literal")

# Add the blocker resolution and patterns learned
edit_memory("ralph-{session_name}",
  old="## Blockers Resolved",
  new="""## Blockers Resolved

### Blocker from Iteration {N}
- **Symptom**: {original symptom}
- **Root Cause**: {confirmed hypothesis description}
- **Fix Applied**: {what was changed}
- **Verified**: {yes/no with evidence}

## Blockers Resolved""",
  mode="literal")
```

### 2. Signal Ralph to Resume

The status change to `active` signals ralph to:
1. Read the updated session memory
2. See the resolved blocker
3. Continue from where it left off

### 3. Commit Before Returning

```bash
git add -A
git commit -m "fix: {root cause description}

Elimination session: {session_id}
Iterations: {count}
Confirmed hypothesis: {id}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

The ralph loop will pick up from here on the next iteration.

---

## Arguments

- `$ARGUMENTS` - Description of the symptom to investigate

