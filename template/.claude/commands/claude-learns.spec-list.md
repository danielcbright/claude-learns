# /claude-learns.spec-list - List All Specifications

**Syntax:** `/claude-learns.spec-list [--status=<status>] [--type=<type>] [--verbose]`

Display all specifications in the project with their status and metadata.

## Overview

Provides a quick overview of all documented specifications, their current status,
and links to detailed spec files. Useful for understanding project scope and
finding specs to reference or update.

## Before Using This Command

Fetch latest documentation if unsure about API/behavior:
- Spec-Kit: `mcp__context7__resolve-library-id("github spec-kit")`

## Workflow

### Phase 1: Scan Specifications

1. **Scan spec directory**
   - List all subdirectories in `.specify/specs/`
   - Read `spec.md` from each

2. **Extract metadata**
   - Spec ID
   - Status (draft, approved, implemented, deprecated)
   - Type (feature, bug-fix, refactor)
   - Last updated date

3. **Count deviations**
   - Check `.specify/deviations/` for related deviations
   - Count approved vs temporary

### Phase 2: Generate Summary

1. **Overview stats**
   ```
   ## Specification Overview

   | Metric | Count |
   |--------|-------|
   | Total Specs | X |
   | Draft | X |
   | Approved | X |
   | Implemented | X |
   | Deprecated | X |
   | With Deviations | X |
   ```

2. **Spec listing**
   ```
   ## Specifications

   | Name | Type | Status | Deviations | Last Updated |
   |------|------|--------|------------|--------------|
   | [name] | feature | approved | 2 | 2026-01-15 |
   ```

3. **Verbose mode** (with `--verbose`)
   - Include spec summaries
   - Show acceptance criteria count
   - List deviation details

### Phase 3: Filtering

Apply filters if specified:

| Flag | Filter |
|------|--------|
| `--status=draft` | Only draft specs |
| `--status=implemented` | Only implemented specs |
| `--type=feature` | Only feature specs |
| `--type=bug-fix` | Only bug fix specs |

## Example

```
User: /claude-learns.spec-list

Claude: Scanning specifications...

## Specification Overview

| Metric | Count |
|--------|-------|
| Total Specs | 5 |
| Draft | 1 |
| Approved | 2 |
| Implemented | 2 |
| Deprecated | 0 |
| With Deviations | 1 |

## Specifications

| Name | Type | Status | Deviations | Last Updated |
|------|------|--------|------------|--------------|
| user-authentication | feature | implemented | 1 | 2026-01-15 |
| payment-processing | feature | approved | 0 | 2026-01-10 |
| api-rate-limiting | feature | implemented | 0 | 2026-01-08 |
| login-bug-fix | bug-fix | approved | 0 | 2026-01-12 |
| database-refactor | refactor | draft | 0 | 2026-01-16 |

## Deviations Summary

| Feature | Deviation | Status |
|---------|-----------|--------|
| user-authentication | Session token 15min vs 1hr | approved |

---

Use `/claude-learns.spec-validate [name]` to check implementation against spec.
Use `/claude-learns.spec-create [name]` to create a new specification.
```

```
User: /claude-learns.spec-list --status=draft --verbose

Claude: Filtering for draft specifications...

## Draft Specifications (1)

### database-refactor

**Type**: refactor
**Created**: 2026-01-16
**Location**: .specify/specs/database-refactor/spec.md

**Summary**: Migrate from PostgreSQL to CockroachDB for horizontal scaling

**Acceptance Criteria**: 8 defined

**Key Changes**:
- Replace pg driver with crdb driver
- Update connection pooling strategy
- Migrate existing data

**Open Questions**: 2 unresolved

---

This spec is ready for review before implementation.
```

## Output Formats

### Default
Compact table view with key metadata.

### Verbose (`--verbose`)
Expanded view with summaries and details.

### JSON (`--json`)
Machine-readable output for scripting (if needed).

## Integration Points

- **Links to `/claude-learns.spec-validate`**: Suggests validation for implemented specs
- **Links to `/claude-learns.spec-create`**: Offers to create new specs
- **Reads deviations**: Shows deviation counts per spec
