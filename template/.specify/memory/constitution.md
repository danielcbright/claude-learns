# Project Constitution

> Non-negotiable principles and rules that govern all development in this project.

---

## Purpose

This constitution defines the absolute rules that must never be violated, regardless of
feature requirements or time constraints. These are the project's "invariants" - the
properties that must always remain true.

---

## Core Principles

### 1. [PRINCIPLE_NAME]

**Rule**: [Clear, unambiguous statement of the rule]

**Rationale**: [Why this rule exists]

**Enforcement**: [How violations are detected/prevented]

**Example Violation**: [What would break this rule]

**Example Compliance**: [What follows this rule]

---

### 2. [PRINCIPLE_NAME]

**Rule**: [Clear, unambiguous statement of the rule]

**Rationale**: [Why this rule exists]

**Enforcement**: [How violations are detected/prevented]

---

## Security Invariants

<!-- Rules that protect the system from security vulnerabilities -->

### S1. [SECURITY_RULE]

**Rule**: [Statement]

**Rationale**: [Why this protects security]

---

## Data Integrity Invariants

<!-- Rules that ensure data correctness and consistency -->

### D1. [DATA_RULE]

**Rule**: [Statement]

**Rationale**: [Why this protects data]

---

## Performance Invariants

<!-- Rules that ensure acceptable performance characteristics -->

### P1. [PERFORMANCE_RULE]

**Rule**: [Statement]

**Threshold**: [Measurable limit]

---

## API Contract Invariants

<!-- Rules about public interfaces and backwards compatibility -->

### A1. [API_RULE]

**Rule**: [Statement]

**Applies to**: [Which interfaces]

---

## When to Update This Document

- When establishing new non-negotiable rules
- When a previously flexible guideline becomes mandatory
- When security requirements change
- When compliance requirements are added
- After a major incident reveals missing invariants

---

## Relationship to CLAUDE.md

| Document | Purpose | Can Override |
|----------|---------|--------------|
| `constitution.md` | Absolute rules, never violated | No - these are invariants |
| `CLAUDE.md` | How Claude should work in this project | Yes - by user request |
| Spec files | Feature-specific requirements | Yes - through deviation process |

---

## Review Schedule

- **Quarterly**: Review all principles for relevance
- **After Incidents**: Add rules to prevent recurrence
- **Before Major Releases**: Verify all invariants still hold

---

*Last Updated: [DATE]*
*Next Review: [DATE]*
