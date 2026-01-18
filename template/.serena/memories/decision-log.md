# Decision Log

> Architectural and design decisions with rationale. Why we chose X over Y.

---

## Purpose

This memory records significant decisions to:
- Provide context for future changes
- Avoid re-debating settled decisions
- Document trade-offs that were considered
- Track when decisions should be revisited

## When to Read

- Before proposing architectural changes
- When encountering code that seems "wrong" but might be intentional
- When spec deviations reference decision rationale

## When to Update

- After making significant architectural decisions
- When `/spec-deviation` logs an intentional deviation
- When choosing between multiple valid approaches
- After design discussions or reviews

---

## Decision Format

```markdown
### DEC-{number}: {Title}

**Date**: YYYY-MM-DD
**Status**: accepted | deprecated | superseded by DEC-{n}
**Context**: [What prompted this decision]
**Decision**: [What was decided]
**Rationale**: [Why this option was chosen]
**Alternatives Considered**:
1. [Alternative 1] - rejected because [reason]
2. [Alternative 2] - rejected because [reason]
**Consequences**: [Positive and negative outcomes]
**Review Date**: [When to reconsider, if applicable]
```

---

## Decisions by Category

### Architecture

<!-- Major structural decisions -->

### DEC-001: [Example Decision Title]

**Date**: [DATE]
**Status**: accepted | deprecated | superseded by DEC-{n}
**Context**: [What prompted this decision - describe the problem or need]
**Decision**: [What was decided - the actual choice made]
**Rationale**:
- [Key reason 1]
- [Key reason 2]
- [Key reason 3]
**Alternatives Considered**:
1. [Alternative 1] - rejected because [reason]
2. [Alternative 2] - rejected because [reason]
**Consequences**:
- [Positive outcome 1] (+)
- [Positive outcome 2] (+)
- [Negative tradeoff] (-)
**Review Date**: [When to reconsider, if applicable]

---

### Authentication & Security

<!-- Auth-related decisions -->

---

### Data & Storage

<!-- Database and data model decisions -->

---

### API Design

<!-- API and interface decisions -->

---

### Tooling & Infrastructure

<!-- Build, deploy, monitoring decisions -->

---

## Quick Reference

| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-001 | [Example decision title] | [DATE] | accepted |

---

## Superseded Decisions

Decisions that have been replaced:

| Original | Replaced By | Date | Reason |
|----------|-------------|------|--------|
| DEC-{n} | DEC-{m} | [Date] | [Why changed] |

---

## Pending Decisions

Decisions under discussion:

| Topic | Options | Deadline | Owner |
|-------|---------|----------|-------|
| [Topic] | [Options being considered] | [Date] | [Who decides] |

---

## Integration with Specs

When a decision affects specifications:
1. Reference the decision ID in the spec
2. Log spec deviations with decision rationale
3. Update this log if spec changes require decision review

---

*Last Updated: [DATE]*
*Total Decisions: 0 (template ready)*
