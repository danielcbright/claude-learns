# /eliminate-status - View Current Elimination State

**Syntax:** `/eliminate-status [--verbose]`

Display the current state of the elimination investigation.

## Usage

```bash
# Standard view - hypothesis table and summary
/eliminate-status

# Verbose view - includes evidence details and reasoning
/eliminate-status --verbose
```

## Output Format

### Standard View

```
## 🔍 Elimination Session: API 500 Errors Investigation

**Started:** 2026-01-18 10:30:00 UTC
**Iteration:** 4 of 20 max
**Phase:** Evidence Gathering

### Hypothesis Status

| Rank | ID | Hypothesis | Confidence | Trend | Status |
|------|-----|------------|------------|-------|--------|
| 1 | H3 | Race condition in request handler | 0.78 | ↑ | 🟢 Active |
| 2 | H4 | Upstream service timeout | 0.42 | → | 🟢 Active |
| 3 | H1 | Database connection pool exhaustion | 0.18 | ↓ | 🟡 Unlikely |
| 4 | H5 | Configuration drift between instances | 0.12 | ↓ | 🟡 Unlikely |
| 5 | H2 | Memory leak causing OOM | 0.04 | ↓ | 🔴 Eliminated |

### Summary
- **Active:** 2 hypotheses
- **Unlikely:** 2 hypotheses  
- **Eliminated:** 1 hypothesis
- **Evidence collected:** 6 pieces
- **Leading hypothesis:** H3 (78% confidence)
- **Separation margin:** 0.36 (H3 vs H4)

### Convergence Status
- ⬜ Leading confidence > 90%: 78% (need 90%)
- ✅ Separation margin > 30%: 36% 
- ⬜ Max iterations: 4/20

**Suggested next action:** Gather more evidence for H3 to reach confirmation threshold
```

### Verbose View (--verbose)

Adds:

```
### Evidence Log

| Time | Evidence | For | Direction | Weight | Result |
|------|----------|-----|-----------|--------|--------|
| 10:35 | DB connections at 45/100 | H1 | ❌ | 0.85 | 0.70→0.28 |
| 10:42 | Memory stable 24hrs | H2 | ❌ | 0.90 | 0.40→0.04 |
| 10:48 | Errors correlate with RPS | H3 | ✅ | 0.70 | 0.35→0.58 |
| 10:55 | Lock contention in logs | H3 | ✅ | 0.80 | 0.58→0.78 |

### Elimination Decisions

| Time | Hypothesis | Action | Reason |
|------|------------|--------|--------|
| 10:42 | H2 | Hard eliminated | Confidence dropped to 0.04 |
| 10:35 | H1 | Soft eliminated | Confidence dropped to 0.28 |

### Reasoning Trace

**H3 Leading Because:**
1. Error rate correlates with concurrent request volume (weight: 0.7)
2. Lock contention observed in SharedCache access (weight: 0.8)
3. No contradicting evidence found

**H4 Still Active Because:**
1. Upstream latency spikes observed (weight: 0.5)
2. But: Local timing shows processing delay, not network (weight: -0.3)
```

## Status Indicators

| Icon | Status | Meaning |
|------|--------|---------|
| 🟢 | Active | Confidence > 0.25, under investigation |
| 🟡 | Unlikely | Confidence 0.05-0.25, soft eliminated |
| 🔴 | Eliminated | Confidence < 0.05, hard eliminated |
| ✅ | Confirmed | Confidence > 0.90, ready for verification |
| ↑ | Increasing | Confidence trending up |
| ↓ | Decreasing | Confidence trending down |
| → | Stable | No significant change |

## Integration

- Run anytime during `/eliminate` session
- Updates in real-time as evidence is added
- Use to decide which hypothesis to test next
- Helps identify when to proceed to verification
