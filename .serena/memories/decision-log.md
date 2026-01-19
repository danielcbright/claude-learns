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

### DEC-001: Spec-Kit Integration for Specification-Driven Development

**Date**: 2026-01-17
**Status**: accepted
**Context**: Need to formalize expected behavior before implementation to improve debugging
**Decision**: Integrate Spec-Kit with elimination debugging system
**Rationale**:
- Specs define expected behavior, making deviations clear
- Spec deviations become high-confidence hypotheses in debugging
- Creates closed feedback loop: spec → implement → validate → debug
**Alternatives Considered**:
1. Informal documentation only - rejected, too easy to drift from reality
2. Test-only specification - rejected, tests don't capture "why"
**Consequences**:
- More upfront work for new features (+)
- Clear source of truth for validation (+)
- Spec maintenance required (-)
- Better debugging when behavior doesn't match expectations (+)
**Review Date**: After 3 months of use, evaluate spec maintenance burden

---

### DEC-002: Dual-Location Architecture for Template Development

**Date**: 2026-01-18
**Status**: accepted
**Context**: Bootstrapping problem - when developing the template, Claude Code loads `.claude/commands/` which could modify template files, polluting distributable content
**Decision**: Keep two copies of template files - root level for development, `template/` folder for distribution
**Rationale**:
- Root files are loaded by Claude Code for active development and testing
- `template/` folder remains pristine with placeholder values
- `/install` command sources from `template/`, not root
- Allows natural development workflow while keeping distribution clean
**Alternatives Considered**:
1. Marker file detection - rejected, complex and fragile
2. Git hooks for cleanup - rejected, doesn't solve runtime pollution
3. Separate repos - rejected, too much friction for development
**Consequences**:
- Must sync root → template/ before releases (+discipline, -extra step)
- Clear separation of concerns (+)
- Can test commands naturally during development (+)
- `template/` always has clean placeholders for users (+)
**Review Date**: N/A - fundamental architecture decision

---

### DEC-003: Test Projects with Language-Specific Skeletons

**Date**: 2026-01-18
**Status**: accepted
**Context**: Need safe environments to test `/install` command without affecting template files
**Decision**: Create `test-projects/` directory with minimal skeletons for JS, Python, and Go
**Rationale**:
- Provides isolated targets for installation testing
- Language-specific skeletons ensure realistic testing
- `.gitignore` excludes installed template files to keep tests clean
- Can run `/install test-projects/minimal-go` without touching template/
**Alternatives Considered**:
1. Use external repos - rejected, requires network and separate maintenance
2. Single generic test project - rejected, doesn't test language detection
**Consequences**:
- Slightly larger repo size (-)
- Realistic multi-language testing (+)
- Installation validation before releases (+)
- Examples for contributors (+)
**Review Date**: N/A

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

### DEC-004: Manifest-Based Template Sync for /update Command

**Date**: 2026-01-19
**Status**: accepted
**Context**: `/claude-learns.update claude-learns` was only updating MCPs, not template files. Need a way for Claude to know which files to update, detect conflicts, and preserve user modifications.
**Decision**: Use manifest.yaml with SHA256 checksums and categorized update behaviors
**Rationale**:
- Checksums enable conflict detection (user-modified vs outdated vs up-to-date)
- Categories allow different behaviors: always_update, updateable, merge_only, protected
- Single manifest file contains all needed info (works offline after fetch)
- Generator script ensures maintainability
**Alternatives Considered**:
1. Git submodules - rejected, too complex for end users
2. Direct file comparison - rejected, can't detect user modifications vs outdated
3. Simple file list without checksums - rejected, no conflict detection
4. Full git diff approach - rejected, requires .git history which installed projects may not have
**Consequences**:
- Manifest must be regenerated when template files change (-)
- Reliable conflict detection (+)
- Clear categorization of update behavior (+)
- Backup system for user modifications (+)
- Self-updating: the update command itself is in always_update category (+)
**Review Date**: After 3 releases, evaluate if checksum approach scales

---

## Quick Reference

| ID | Decision | Date | Status |
|----|----------|------|--------|
| DEC-001 | Spec-Kit integration for specification-driven development | 2026-01-17 | accepted |
| DEC-002 | Dual-location architecture for template development | 2026-01-18 | accepted |
| DEC-003 | Test projects with language-specific skeletons | 2026-01-18 | accepted |
| DEC-004 | Manifest-based template sync for /update command | 2026-01-19 | accepted |

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

*Last Updated: 2026-01-19*
*Total Decisions: 4*
