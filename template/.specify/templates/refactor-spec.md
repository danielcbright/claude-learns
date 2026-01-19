# Refactoring Specification: [REFACTOR_NAME]

> [One-line description of what is being refactored and why]

---

## Metadata

| Field | Value |
|-------|-------|
| **Spec ID** | `refactor-[id]` |
| **Status** | `proposed` / `approved` / `in-progress` / `completed` / `abandoned` |
| **Author** | [Author name] |
| **Created** | [YYYY-MM-DD] |
| **Target Completion** | [YYYY-MM-DD] |

---

## Motivation

### Why refactor now?

[Clear explanation of the pain points driving this refactor]

### Current Problems

1. [Problem 1 - specific, measurable if possible]
2. [Problem 2]
3. [Problem 3]

### What happens if we don't refactor?

[Consequences of maintaining status quo]

---

## Scope

### In Scope

- [Component/file/area 1]
- [Component/file/area 2]

### Out of Scope

- [What we're explicitly NOT changing]
- [Adjacent code that stays unchanged]

### Boundaries

[Clear definition of where the refactor starts and stops]

---

## Current State

### Architecture

```
[Diagram or description of current structure]
```

### Key Files

| File | Purpose | Issues |
|------|---------|--------|
| [path] | [what it does] | [what's wrong with it] |

### Metrics (Before)

| Metric | Current Value |
|--------|---------------|
| Lines of code | [number] |
| Cyclomatic complexity | [number] |
| Test coverage | [percentage] |
| Build time impact | [duration] |

---

## Target State

### Architecture

```
[Diagram or description of target structure]
```

### Key Changes

| Before | After | Rationale |
|--------|-------|-----------|
| [Old pattern] | [New pattern] | [Why this is better] |

### Expected Metrics (After)

| Metric | Target Value | Improvement |
|--------|--------------|-------------|
| Lines of code | [number] | [delta] |
| Cyclomatic complexity | [number] | [delta] |
| Test coverage | [percentage] | [delta] |

---

## Migration Strategy

### Approach

[ ] Big Bang - Replace all at once
[ ] Strangler Fig - Gradually replace
[ ] Branch by Abstraction - Abstract, switch, remove

### Phases

#### Phase 1: [Name]

- [ ] [Task 1]
- [ ] [Task 2]
- **Checkpoint**: [How to verify phase is complete]

#### Phase 2: [Name]

- [ ] [Task 1]
- [ ] [Task 2]
- **Checkpoint**: [How to verify phase is complete]

### Rollback Points

| After Phase | How to Rollback |
|-------------|-----------------|
| Phase 1 | [Rollback steps] |
| Phase 2 | [Rollback steps] |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | `low/medium/high` | [Impact] | [How to mitigate] |
| [Risk 2] | `low/medium/high` | [Impact] | [How to mitigate] |

---

## Testing Strategy

### Existing Tests

- [ ] All existing tests pass before starting
- [ ] Run tests after each phase

### New Tests

- [ ] [New test 1]
- [ ] [New test 2]

### Behavioral Verification

[How to verify behavior hasn't changed]

---

## Dependencies

### Blocked By

- [What needs to happen before this refactor]

### Blocks

- [What is waiting on this refactor]

### External Dependencies

- [Libraries, services, etc. affected]

---

## Communication Plan

### Stakeholders

| Who | What they need to know |
|-----|------------------------|
| [Team/person] | [Information] |

### Announcements

- [ ] Before starting: [What to communicate]
- [ ] After completion: [What to communicate]

---

## Success Criteria

- [ ] All tests pass
- [ ] No regression in functionality
- [ ] Metrics meet targets
- [ ] Documentation updated
- [ ] Team sign-off

---

## Post-Refactor Tasks

- [ ] Update CLAUDE.md if patterns changed
- [ ] Update relevant memories
- [ ] Archive old documentation
- [ ] Update dependent specs

---

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|------|----------|-----------|------------------------|
| [Date] | [Decision made] | [Why] | [Other options] |

---

*Template Version: 1.0*
