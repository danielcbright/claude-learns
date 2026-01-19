# Specification: elimination-subagent-orchestration

**Created**: 2026-01-19
**Status**: Implemented
**Verified**: 2026-01-19
**Author**: Claude (with user)

---

## Overview

Refactor the elimination debugging system to use Claude Code's Task tool with specialized subagents, where Claude acts as an orchestrator coordinating function-based agents in an iterative loop.

### Problem Statement

Currently, the elimination system relies on:
- Claude reading markdown instructions and following them manually
- Claude executing Python scripts via Bash
- No structured delegation - Claude does everything in a single context

This leads to:
- Context overload during complex debugging sessions
- No parallelization of research/analysis tasks
- Process adherence depends entirely on Claude's discipline
- Long elimination sessions can exceed context limits

### Goals

1. **Orchestrator pattern**: Claude Code acts as coordinator, delegating work to specialized subagents
2. **Function-based agents**: Each agent owns a capability (research, code analysis, test execution)
3. **Iterative loop**: Orchestrator cycles through agents: generate → test → update → repeat
4. **Script gates preserved**: Existing Python scripts validate work between phases
5. **Phase completion handoff**: Subagents complete their phase fully before returning control

---

## Architecture

### Agent Types

| Agent | Responsibility | Tools Available |
|-------|----------------|-----------------|
| **ResearchAgent** | Search web, fetch docs, find similar issues | WebSearch, WebFetch, Context7 |
| **CodeAnalysisAgent** | Analyze codebase, find symbols, trace flows | Serena MCP, Grep, Glob, Read |
| **TestRunnerAgent** | Execute tests, check logs, run diagnostics | Bash, Read |
| **HypothesisAgent** | Generate and refine hypotheses from context | Read (memories, heuristics), Write |

### Orchestrator Responsibilities

The orchestrator (main Claude session):
1. Initializes elimination session via `eliminate_init.py`
2. Launches subagents for specific tasks
3. Collects and validates subagent outputs
4. Runs script gates between phases
5. Maintains overall session state
6. Makes convergence decisions
7. Archives session when complete

### Control Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR CONTROL FLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  START                                                              │
│    │                                                                │
│    ▼                                                                │
│  ┌─────────────────────────────────────────┐                       │
│  │ 1. Initialize session (eliminate_init.py)│                       │
│  └───────────────┬─────────────────────────┘                       │
│                  │                                                  │
│                  ▼                                                  │
│  ┌─────────────────────────────────────────┐                       │
│  │ 2. Launch HypothesisAgent               │                       │
│  │    → Generate initial hypotheses        │                       │
│  │    → Returns: hypothesis list           │                       │
│  └───────────────┬─────────────────────────┘                       │
│                  │                                                  │
│                  ▼                                                  │
│  ┌─────────────────────────────────────────┐                       │
│  │ 3. GATE: Validate hypotheses written    │                       │
│  │    (check .elimination/active/hyp-*.yaml)│                       │
│  └───────────────┬─────────────────────────┘                       │
│                  │                                                  │
│    ┌─────────────┴─────────────────────────────────────┐           │
│    │              ITERATIVE LOOP                        │           │
│    │  ┌─────────────────────────────────────────────┐  │           │
│    │  │ 4. Get next hypothesis (eliminate_next.py)  │  │           │
│    │  └───────────────┬─────────────────────────────┘  │           │
│    │                  │                                 │           │
│    │                  ▼                                 │           │
│    │  ┌─────────────────────────────────────────────┐  │           │
│    │  │ 5. Launch ResearchAgent (optional)          │  │           │
│    │  │    → Search for prior art, known issues     │  │           │
│    │  │    → Returns: research findings             │  │           │
│    │  └───────────────┬─────────────────────────────┘  │           │
│    │                  │                                 │           │
│    │                  ▼                                 │           │
│    │  ┌─────────────────────────────────────────────┐  │           │
│    │  │ 6. Launch CodeAnalysisAgent                 │  │           │
│    │  │    → Analyze relevant code paths            │  │           │
│    │  │    → Returns: code insights                 │  │           │
│    │  └───────────────┬─────────────────────────────┘  │           │
│    │                  │                                 │           │
│    │                  ▼                                 │           │
│    │  ┌─────────────────────────────────────────────┐  │           │
│    │  │ 7. Launch TestRunnerAgent                   │  │           │
│    │  │    → Execute discriminating test            │  │           │
│    │  │    → Returns: test results                  │  │           │
│    │  └───────────────┬─────────────────────────────┘  │           │
│    │                  │                                 │           │
│    │                  ▼                                 │           │
│    │  ┌─────────────────────────────────────────────┐  │           │
│    │  │ 8. GATE: Record checkpoint                  │  │           │
│    │  │    (eliminate_checkpoint.py)                │  │           │
│    │  │    → Validates ALL hypotheses updated       │  │           │
│    │  └───────────────┬─────────────────────────────┘  │           │
│    │                  │                                 │           │
│    │                  ▼                                 │           │
│    │  ┌─────────────────────────────────────────────┐  │           │
│    │  │ 9. Check convergence criteria               │  │           │
│    │  │    → Leading > 0.90?                        │  │           │
│    │  │    → Separation > 0.30?                     │  │           │
│    │  └───────────────┬─────────────────────────────┘  │           │
│    │                  │                                 │           │
│    │         ┌───────┴───────┐                         │           │
│    │         │               │                         │           │
│    │    NOT CONVERGED    CONVERGED                     │           │
│    │         │               │                         │           │
│    │         ▼               │                         │           │
│    │    [Loop back to 4]     │                         │           │
│    │                         │                         │           │
│    └─────────────────────────┼─────────────────────────┘           │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────┐                       │
│  │ 10. Verification phase                  │                       │
│  │     → Launch TestRunnerAgent for fix    │                       │
│  └───────────────┬─────────────────────────┘                       │
│                  │                                                  │
│                  ▼                                                  │
│  ┌─────────────────────────────────────────┐                       │
│  │ 11. Archive (eliminate_archive.py)      │                       │
│  └─────────────────────────────────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Requirements

### Functional Requirements

#### FR-1: Orchestrator Command
- **FR-1.1**: Update `/claude-learns.eliminate` command to use orchestrator pattern
- **FR-1.2**: Orchestrator maintains session state in `.elimination/active/`
- **FR-1.3**: Orchestrator invokes subagents via Task tool with `subagent_type` parameter
- **FR-1.4**: Orchestrator collects subagent results and validates before proceeding

#### FR-2: HypothesisAgent
- **FR-2.1**: Reads heuristics.yaml, templates, and project memories
- **FR-2.2**: Generates 3-7 hypotheses across Ishikawa categories
- **FR-2.3**: Writes hypotheses to `.elimination/active/hypotheses/`
- **FR-2.4**: Returns structured summary to orchestrator

#### FR-3: ResearchAgent
- **FR-3.1**: Uses WebSearch and WebFetch to find similar issues
- **FR-3.2**: Searches GitHub Issues, Stack Overflow, documentation
- **FR-3.3**: Records findings via `eliminate_research.py --record`
- **FR-3.4**: Returns research summary with confidence boost recommendations

#### FR-4: CodeAnalysisAgent
- **FR-4.1**: Uses Serena MCP for symbol analysis
- **FR-4.2**: Traces code paths related to current hypothesis
- **FR-4.3**: Identifies suspicious patterns, recent changes
- **FR-4.4**: Returns analysis summary with relevant code locations

#### FR-5: TestRunnerAgent
- **FR-5.1**: Designs discriminating test for current hypothesis
- **FR-5.2**: Executes test via Bash
- **FR-5.3**: Captures and interprets results
- **FR-5.4**: Returns structured test result with evidence

#### FR-6: Script Gates
- **FR-6.1**: Orchestrator runs `eliminate_init.py` before HypothesisAgent
- **FR-6.2**: Orchestrator runs `eliminate_checkpoint.py` after each test
- **FR-6.3**: Orchestrator runs `eliminate_next.py` to determine next hypothesis
- **FR-6.4**: Orchestrator runs `eliminate_archive.py` at session end
- **FR-6.5**: Script gate failures block progression (orchestrator must handle)

#### FR-7: Iterative Loop
- **FR-7.1**: Orchestrator cycles through: next_hypothesis → research → analyze → test → checkpoint
- **FR-7.2**: Some steps can be skipped if not needed (e.g., research already done)
- **FR-7.3**: Loop continues until convergence criteria met
- **FR-7.4**: Orchestrator can request user intervention if stuck

---

### Non-Functional Requirements

#### NFR-1: Context Efficiency
- Subagents should have focused prompts with only relevant context
- Subagent results should be summarized before returning to orchestrator
- Long research/analysis outputs should be written to files, not passed in full

#### NFR-2: Process Adherence
- Script gates enforce process (existing behavior preserved)
- Subagents cannot bypass gates
- Orchestrator cannot skip required gates

#### NFR-3: Transparency
- Orchestrator announces each subagent launch
- Subagent results are visible to user
- Gate pass/fail status is reported

#### NFR-4: Graceful Degradation
- If subagent fails, orchestrator can retry or ask user
- If script gate fails, orchestrator reports reason and options
- If convergence not reached after max iterations, orchestrator summarizes and asks user

---

## Acceptance Criteria

### AC-1: Orchestrator Controls Flow
- [ ] Running `/claude-learns.eliminate` starts orchestrator pattern
- [ ] Orchestrator launches HypothesisAgent first
- [ ] Orchestrator waits for subagent completion before proceeding
- [ ] Orchestrator runs script gates between phases

### AC-2: HypothesisAgent Works
- [ ] HypothesisAgent reads heuristics and memories
- [ ] HypothesisAgent generates hypotheses and writes to files
- [ ] HypothesisAgent returns summary to orchestrator
- [ ] Orchestrator validates hypotheses exist before proceeding

### AC-3: ResearchAgent Works
- [ ] ResearchAgent uses WebSearch and WebFetch
- [ ] ResearchAgent records findings via script
- [ ] ResearchAgent returns research summary
- [ ] Research is optional (orchestrator can skip if not needed)

### AC-4: CodeAnalysisAgent Works
- [ ] CodeAnalysisAgent uses Serena MCP tools
- [ ] CodeAnalysisAgent identifies relevant code paths
- [ ] CodeAnalysisAgent returns analysis summary
- [ ] Analysis informs test design

### AC-5: TestRunnerAgent Works
- [ ] TestRunnerAgent executes tests via Bash
- [ ] TestRunnerAgent captures output
- [ ] TestRunnerAgent returns structured result
- [ ] Result includes evidence for checkpoint

### AC-6: Script Gates Enforced
- [ ] `eliminate_init.py` runs before hypothesis generation
- [ ] `eliminate_checkpoint.py` runs after each test
- [ ] `eliminate_next.py` determines next hypothesis (not subagent discretion)
- [ ] Gate failures prevent progression

### AC-7: Iterative Loop Works
- [ ] Orchestrator cycles through agents correctly
- [ ] Loop continues until convergence
- [ ] User can interrupt and resume
- [ ] Session can be archived when complete

---

## Design

### Subagent Prompts

#### HypothesisAgent Prompt Template

```
You are a HypothesisAgent for elimination debugging.

CONTEXT:
- Symptom: {symptom}
- Project: {project_path}

YOUR TASK:
1. Read .elimination/learned/heuristics.yaml for matching patterns
2. Read .serena/memories/elimination_patterns.md for project patterns
3. Generate 3-7 hypotheses across categories: Code, Config, Dependencies, Data, Infrastructure, Concurrency
4. Assign initial confidence scores (use heuristics priors if available)
5. Write each hypothesis to .elimination/active/hypotheses/hyp-{id}.yaml

RETURN FORMAT:
Summarize the hypotheses you generated:
- H1: {description} (confidence: {score})
- H2: {description} (confidence: {score})
...

Do NOT proceed to testing. Return control to orchestrator after generating hypotheses.
```

#### ResearchAgent Prompt Template

```
You are a ResearchAgent for elimination debugging.

CONTEXT:
- Current hypothesis: {hypothesis_id} - {hypothesis_description}
- Symptom: {symptom}
- Tech stack: {tech_stack}

YOUR TASK:
1. Use WebSearch to find similar issues, known bugs, solutions
2. Search GitHub Issues for related problems
3. Check Stack Overflow for community solutions
4. Record findings using: python .claude/scripts/elimination/eliminate_research.py --hypothesis {id} --record '{json}' --boost {value}

RETURN FORMAT:
Research summary:
- Sources checked: {count}
- Relevant findings: {count}
- Confidence boost applied: {total_boost}
- Key insight: {summary}

Do NOT proceed to testing. Return control to orchestrator.
```

#### CodeAnalysisAgent Prompt Template

```
You are a CodeAnalysisAgent for elimination debugging.

CONTEXT:
- Current hypothesis: {hypothesis_id} - {hypothesis_description}
- Symptom: {symptom}
- Suspected area: {suspected_area}

YOUR TASK:
1. Use find_symbol() to locate relevant code
2. Use find_referencing_symbols() to trace dependencies
3. Use get_symbols_overview() to understand structure
4. Identify code patterns that could cause the hypothesized issue

RETURN FORMAT:
Analysis summary:
- Files examined: {list}
- Suspicious patterns: {list}
- Relevant code locations: {list with line numbers}
- Recommended test: {what to test}

Do NOT modify code or run tests. Return control to orchestrator.
```

#### TestRunnerAgent Prompt Template

```
You are a TestRunnerAgent for elimination debugging.

CONTEXT:
- Current hypothesis: {hypothesis_id} - {hypothesis_description}
- Test to run: {test_description}
- Expected outcome if hypothesis TRUE: {expected_if_true}
- Expected outcome if hypothesis FALSE: {expected_if_false}

YOUR TASK:
1. Execute the discriminating test via Bash
2. Capture all relevant output
3. Interpret result relative to hypothesis

RETURN FORMAT:
Test result:
- Test executed: {description}
- Output: {relevant output}
- Interpretation: {supports/contradicts/neutral} hypothesis
- Evidence summary: {brief summary}
- Confidence update recommendation: {old} → {new}

Do NOT update hypothesis files directly. Return control to orchestrator.
```

### Orchestrator Command Updates

The `/claude-learns.eliminate` command will be updated to:

1. **Initialize**: Run `eliminate_init.py --symptom "..." --interactive` if no active session
2. **Launch HypothesisAgent**: `Task(subagent_type="general-purpose", prompt=hypothesis_prompt)`
3. **Validate**: Check `.elimination/active/hypotheses/` has files
4. **Loop**:
   - Run `eliminate_next.py` to get next hypothesis
   - Optionally launch ResearchAgent
   - Launch CodeAnalysisAgent
   - Launch TestRunnerAgent
   - Run `eliminate_checkpoint.py --test "..." --evidence "..." --updates "..."`
   - Check convergence
5. **Converge**: When criteria met, proceed to verification
6. **Archive**: Run `eliminate_archive.py`

---

## Out of Scope

- Parallel subagent execution (this spec uses sequential one-at-a-time)
- New script development (reuses existing scripts)
- Changes to hypothesis file format
- Changes to convergence criteria
- Custom agent types beyond the four defined

---

## Test Plan

### Manual Testing

1. **Basic Flow Test**
   - Run `/claude-learns.eliminate "test symptom"`
   - Verify HypothesisAgent launches and generates hypotheses
   - Verify orchestrator runs script gate
   - Verify iterative loop starts

2. **Subagent Isolation Test**
   - Verify each subagent returns control after its phase
   - Verify subagents don't skip ahead
   - Verify subagent outputs are captured

3. **Script Gate Test**
   - Verify `eliminate_init.py` runs first
   - Verify `eliminate_checkpoint.py` validates updates
   - Verify gate failures stop progression

4. **Convergence Test**
   - Run until convergence criteria met
   - Verify loop exits correctly
   - Verify archive runs at end

5. **Interruption Test**
   - Interrupt mid-session
   - Resume with `/claude-learns.eliminate-status`
   - Verify state preserved

---

## Implementation Notes

- Subagents are launched via Task tool with `subagent_type="general-purpose"`
- Alternative: Create custom subagent types registered in Claude Code config
- Orchestrator must parse subagent return values to extract structured data
- Consider using `model: "haiku"` for simple subagent tasks to reduce cost/latency
- ResearchAgent may need longer timeout for web fetches

---

## References

- Current `/claude-learns.eliminate` command: `.claude/commands/claude-learns.eliminate.md`
- Elimination scripts: `.claude/scripts/elimination/`
- Task tool documentation: Claude Code system prompt
- Decision DEC-004: Manifest-based template sync (similar orchestration pattern)

