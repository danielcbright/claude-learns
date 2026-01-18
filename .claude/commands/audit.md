Audit CLAUDE.md and project memories for accuracy and completeness.

## Audit Scope

Review all project documentation for:
- **Accuracy**: Is the information still correct?
- **Completeness**: Are important topics missing?
- **Relevance**: Is outdated information still present?
- **Consistency**: Do memories and CLAUDE.md align?

## Audit Process

### 1. CLAUDE.md Review

Check each section:

```
[ ] Project Overview - Still accurate?
[ ] MCP & Plugin Strategy - Tools still relevant?
[ ] Active Skills - Skills still available and useful?
[ ] Serena Usage Guide - Patterns still best practice?
[ ] Project-Specific Patterns - Match current codebase?
[ ] Common Workflows - Still the right approach?
[ ] Quick Reference - Commands still work?
[ ] Troubleshooting - Issues still relevant?
[ ] Changelog - Up to date?
```

### 2. Memory Audit

For each memory in `.serena/memories/`:

```
list_memories()

For each memory:
- read_memory("[name]")
- Check: Is this still accurate?
- Check: Is this still useful?
- Check: Should this be updated or archived?
```

### 3. Codebase Alignment

Verify documentation matches reality:

```
# Check documented patterns exist
find_symbol("[documented_pattern]")

# Verify documented entry points
get_symbols_overview("[documented_path]")

# Confirm documented commands work
[run documented test/build commands]
```

### 4. Gap Analysis

Identify missing documentation:
- Important modules without memory coverage
- Common tasks without workflow documentation
- Frequently-used patterns not captured

## Audit Report

Generate a structured report:

```
📋 **Documentation Audit Report**

### CLAUDE.md Status
| Section | Status | Notes |
|---------|--------|-------|
| Project Overview | ✅/⚠️/❌ | [notes] |
| MCP Strategy | ✅/⚠️/❌ | [notes] |
| Active Skills | ✅/⚠️/❌ | [notes] |
| ... | ... | ... |

### Memory Status
| Memory | Status | Recommendation |
|--------|--------|----------------|
| [name] | ✅ Current / ⚠️ Stale / ❌ Incorrect | [action needed] |
| ... | ... | ... |

### Gaps Identified
1. [Missing documentation area]
2. [Undocumented pattern]
3. ...

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
2. Stale information (update or archive)
3. Missing information (create new content)
4. Minor improvements (nice to have)

---

Audit focus (optional): $ARGUMENTS
