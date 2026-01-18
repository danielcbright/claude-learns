# Elimination System Sample Files

This directory contains example YAML files that demonstrate the structure
and content expected for each file type in the elimination system.

**These are reference templates, not active data.**

## Files

| File | Purpose |
|------|---------|
| `session-example.yaml` | Example active session with hypotheses tracking |
| `hypotheses/hypothesis-example.yaml` | Example hypothesis with confidence tracking |
| `evidence/evidence-example.yaml` | Example evidence with Bayesian weight |
| `elimination_log-example.yaml` | Example log of elimination decisions |

## Usage

When creating new elimination sessions, Claude should reference these files
to understand the expected YAML structure:

```yaml
# Read samples to understand format
read_file(".elimination/samples/session-example.yaml")
read_file(".elimination/samples/hypotheses/hypothesis-example.yaml")
read_file(".elimination/samples/evidence/evidence-example.yaml")
```

## Key Fields

### Session
- `session.id`: Unique session identifier
- `session.status`: active, paused, resolved, abandoned
- `session.phase`: hypothesis_generation, evidence_gathering, verification, learning
- `hypotheses.active/unlikely/eliminated`: Lists of hypothesis IDs

### Hypothesis
- `confidence.initial/current`: Bayesian confidence scores (0.0-1.0)
- `status`: active, unlikely, eliminated, confirmed, verified
- `domain`: code, config, dependencies, data, infrastructure, concurrency
- `evidence.supporting/contradicting`: Evidence IDs and their impact

### Evidence
- `bearing[].direction`: supports, contradicts, neutral
- `bearing[].weight`: Strength of evidence (0.1-1.0)
- `quality.reliability`: high, medium, low

## Thresholds (from config.yaml)

- Hard eliminate: confidence < 0.05
- Soft eliminate: confidence < 0.25
- Confirm: confidence > 0.90
