Audit CLAUDE.md and project memories for accuracy and completeness.

## Audit Scope

Review **all documentation and memory systems** for:
- **Accuracy**: Is the information still correct?
- **Completeness**: Are important topics missing?
- **Relevance**: Is outdated information still present?
- **Consistency**: Do memories and CLAUDE.md align?

## Audit Process

### 1. CLAUDE.md Review

Check each section:

```
[ ] Project Overview - Still accurate?
[ ] Memory Management - Tool priority still correct?
[ ] Current Memories table - All memories listed?
[ ] MCP Integration - Tools still relevant?
[ ] Key Entry Points - Symbols still exist?
[ ] Common Workflows - Still the right approach?
[ ] Completion Standards - Being followed?
[ ] Quick Reference - All commands listed?
[ ] Spec-Driven Development - Paths accurate?
[ ] Elimination Debugging - Thresholds appropriate?
[ ] Changelog - Up to date?
```

### 2. Serena Memory Audit (.serena/memories/)

```
list_memories()

For each memory:
- read_memory("[name]")
- Check: Is this still accurate?
- Check: Is this still useful?
- Check: Should this be updated or archived?
```

**Expected memories:**
| Memory | Purpose | Check |
|--------|---------|-------|
| `claude_code_patterns` | Session quick reference | Patterns still valid? |
| `elimination_patterns` | Debugging quick reference | Patterns still useful? |
| `debugging-lessons` | Past debugging insights | Lessons still relevant? |
| `common-bugs` | Recurring bug patterns | Bugs still occurring? |
| `decision-log` | Architectural decisions | Decisions still valid? |
| `tool-documentation` | External tool docs | Links still work? |

### 3. Spec Memory Audit (.specify/memory/)

```bash
cat .specify/memory/constitution.md
cat .specify/memory/corrections.md
```

**Check:**
| File | Check |
|------|-------|
| `constitution.md` | Are rules still non-negotiable? Any new rules needed? |
| `corrections.md` | Are patterns still relevant? Any resolved patterns to archive? |

### 4. Elimination System Audit (.elimination/)

```bash
cat .elimination/config.yaml
cat .elimination/learned/heuristics.yaml
ls .elimination/archive/
```

**Check:**
| Item | Check |
|------|-------|
| `config.yaml` | Thresholds appropriate? (confirmed: >0.90, eliminated: <0.05) |
| `heuristics.yaml` | Heuristics still valid? Statistics accurate? Any deprecated? |
| `archive/` | Old sessions properly archived? Any learnings not extracted? |
| `learned/templates/` | Hypothesis templates still relevant? |

### 5. Cross-System Consistency

Verify alignment between systems:

```
[ ] Commands table in CLAUDE.md matches .claude/commands/*.md
[ ] Memories table in CLAUDE.md matches actual memory files
[ ] File paths in CLAUDE.md tree diagrams match actual structure
[ ] Workflows in CLAUDE.md match what commands actually do
[ ] Routing in /claude-learns.learn matches actual file locations
```

### 6. Codebase Alignment

Verify documentation matches reality:

```
# Check documented patterns exist
find_symbol("[documented_pattern]")

# Verify documented entry points
get_symbols_overview("[documented_path]")

# Confirm documented commands work
[run documented test/build commands]
```

### 7. Gap Analysis

Identify missing documentation:
- Important modules without memory coverage
- Common tasks without workflow documentation
- Frequently-used patterns not captured
- Memory files never read by any command (orphans)
- Commands with missing memory connections

## Audit Report

Generate a structured report:

```
## Documentation Audit Report

### CLAUDE.md Status
| Section | Status | Notes |
|---------|--------|-------|
| Project Overview | ?/!/X | [notes] |
| Memory Management | ?/!/X | [notes] |
| Workflows | ?/!/X | [notes] |
| Quick Reference | ?/!/X | [notes] |
| ... | ... | ... |

### Serena Memory Status (.serena/memories/)
| Memory | Status | Recommendation |
|--------|--------|----------------|
| [name] | Current / Stale / Incorrect | [action needed] |
| ... | ... | ... |

### Spec Memory Status (.specify/memory/)
| File | Status | Recommendation |
|------|--------|----------------|
| constitution.md | ?/!/X | [action needed] |
| corrections.md | ?/!/X | [action needed] |

### Elimination System Status (.elimination/)
| Component | Status | Recommendation |
|-----------|--------|----------------|
| config.yaml | ?/!/X | [action needed] |
| heuristics.yaml | ?/!/X | [action needed] |
| Archived sessions | ?/!/X | [action needed] |

### Cross-System Issues
| Issue | Location | Fix |
|-------|----------|-----|
| [discrepancy] | [where] | [how to fix] |

### Gaps Identified
1. [Missing documentation area]
2. [Undocumented pattern]
3. [Orphaned memory file]
4. ...

### Recommended Actions
1. **High Priority**: [action]
2. **Medium Priority**: [action]
3. **Low Priority**: [action]
```

## Execute Fixes

After presenting the report:
> "Would you like me to fix any of these issues?"

Priority order:
1. Incorrect information (fix immediately)
2. Cross-system inconsistencies (align documentation)
3. Stale information (update or archive)
4. Missing information (create new content)
5. Minor improvements (nice to have)

---

Audit focus (optional): $ARGUMENTS
