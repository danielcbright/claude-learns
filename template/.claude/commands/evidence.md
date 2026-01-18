# /evidence - Record Evidence for Hypothesis Evaluation

**Syntax:** `/evidence [hypothesis_id] [observation] [--supports|--contradicts] [--weight 0.X]`

Record evidence bearing on one or more hypotheses in the active investigation.

## Usage

```bash
# Evidence supporting a hypothesis
/evidence H3 "Lock contention detected in handler logs" --supports --weight 0.8

# Evidence contradicting a hypothesis  
/evidence H1 "Connection pool at 30% capacity during errors" --contradicts --weight 0.9

# Evidence affecting multiple hypotheses
/evidence H2,H5 "Memory stable at 2GB for 24 hours" --contradicts

# With source reference
/evidence H3 "Race condition in SharedCache.get()" --supports --source "src/cache.ts:142"
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `hypothesis_id` | Target hypothesis (H1, H2, etc.) or comma-separated list | Required |
| `observation` | Description of what was observed | Required |
| `--supports` | Evidence supports the hypothesis | - |
| `--contradicts` | Evidence contradicts the hypothesis | - |
| `--weight` | Strength of evidence (0.1-1.0) | 0.5 |
| `--source` | Reference to logs, code, docs | - |
| `--test` | Description of test performed | - |

## Behavior

1. **Validate hypothesis exists** in active session

2. **Create evidence file**
   ```yaml
   id: "ev-{timestamp}-{seq}"
   type: observation  # or: log_analysis, test_result, metric, user_report
   description: "{observation}"
   
   bearing:
     hypothesis_id: "{target}"
     direction: supports|contradicts
     weight: {0.1-1.0}
   
   source_ref: "{optional_source}"
   test_performed: "{optional_test_description}"
   
   metadata:
     recorded_at: "{timestamp}"
     recorded_by: user
   ```

3. **Update hypothesis confidence**
   - Supporting evidence: `new_confidence = old_confidence * (1 + weight * 0.5)`
   - Contradicting evidence: `new_confidence = old_confidence * (1 - weight * 0.7)`
   - Cap at 0.01 minimum, 0.99 maximum

4. **Check elimination thresholds**
   - If confidence < 0.05: Hard eliminate, log to elimination_log.yaml
   - If confidence < 0.25: Soft eliminate (mark as unlikely)
   - If confidence > 0.90: Flag for verification

5. **Report updated state**

## Example

```
User: /evidence H1 "Database connections at 45/100 during error spike" --contradicts --weight 0.85 --source "grafana:db-pool-dashboard"

Claude: 📊 Evidence recorded for H1 (Database Connection Pool Exhaustion)

**Observation:** Database connections at 45/100 during error spike
**Direction:** ❌ Contradicts hypothesis
**Weight:** 0.85 (strong)
**Source:** grafana:db-pool-dashboard

**Confidence Update:**
- Previous: 0.70
- After evidence: 0.70 × (1 - 0.85 × 0.7) = 0.28
- New confidence: **0.28**
- Status: ⚠️ SOFT ELIMINATED (unlikely)

**Remaining Active Hypotheses:**
| ID | Description | Confidence | Status |
|----|-------------|------------|--------|
| H3 | Race condition in request handler | 0.65 | Active |
| H4 | Upstream service timeout | 0.45 | Active |
| H1 | Database connection pool exhaustion | 0.28 | Unlikely |
| H2 | Memory leak causing OOM | 0.22 | Unlikely |

**Suggested next test:** Check H3 - Add logging around concurrent request handling
```

## Evidence Types

- `observation` - Direct observation of system behavior
- `log_analysis` - Pattern found in logs
- `test_result` - Result of explicit test
- `metric` - Quantitative measurement
- `code_inspection` - Finding from code review
- `user_report` - Information from user/stakeholder

## Bayesian Reasoning

The confidence update follows simplified Bayesian logic:

```
For supporting evidence:
  likelihood_ratio = 1 + (weight × 0.5)  # Range: 1.05 to 1.5
  new_confidence = old × likelihood_ratio

For contradicting evidence:
  likelihood_ratio = 1 - (weight × 0.7)  # Range: 0.93 to 0.3
  new_confidence = old × likelihood_ratio
```

This ensures:
- Strong contradicting evidence can nearly eliminate a hypothesis
- Supporting evidence increases confidence but never guarantees
- Multiple pieces of evidence compound appropriately
