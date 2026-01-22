Analyze and optimize the project's Claude Code configuration for context window efficiency.

## Purpose

This command performs a comprehensive analysis of CLAUDE.md, commands, skills, and memories to:
- Identify context window inefficiencies
- Detect redundancy and bloat
- Recommend optimizations
- Optionally apply safe fixes

## Optimization Targets

### Quantitative Guidelines

| Component | Optimal | Warning | Critical |
|-----------|---------|---------|----------|
| CLAUDE.md lines | < 300 | 300-500 | > 500 |
| CLAUDE.md size | < 10KB | 10-15KB | > 15KB |
| Instruction count | < 150 | 150-200 | > 200 |
| Command file | < 300 lines | 300-500 | > 500 |
| SKILL.md words | < 3000 | 3000-5000 | > 5000 |
| Total commands | < 200KB | 200-300KB | > 300KB |
| Total memories | < 80KB | 80-120KB | > 120KB |

### Key Principles

1. **Progressive Disclosure**: Load details on-demand, not upfront
2. **Trigger Tables**: Map phrases to actions, not verbose explanations
3. **Lazy Loading**: Reference files instead of embedding content
4. **Hierarchical Organization**: Most specific context wins
5. **Memory Routing**: Categorize by when-to-read

---

## Analysis Process

### Phase 1: Metrics Collection

**CLAUDE.md Analysis:**
```bash
# Get metrics
wc -l CLAUDE.md                    # Line count
wc -c CLAUDE.md                    # Byte size
```

Count these patterns:
- `MUST` / `NEVER` / `ALWAYS` / `CRITICAL` (hard rules)
- `PREFER` / `AVOID` / `SHOULD` (soft rules)
- `---` (section dividers)
- Code blocks (```)
- Tables (`|`)

**Commands Analysis:**
```bash
# Total size
du -ch .claude/commands/*.md | tail -1

# Individual sizes
for f in .claude/commands/*.md; do
  echo "$(wc -l < "$f") lines - $(du -h "$f" | cut -f1) - $(basename "$f")"
done | sort -rn
```

**Skills Analysis:**
```bash
# Check skills structure
find .claude/skills -name "*.md" -exec wc -w {} \;

# Check for references folders
find .claude/skills -type d -name "references"
```

**Memories Analysis:**
```bash
# Total size
du -ch .serena/memories/*.md | tail -1

# Individual sizes with metadata check
for f in .serena/memories/*.md; do
  echo "--- $(basename "$f") ---"
  wc -l "$f"
  head -10 "$f" | grep -E "^(type|purpose|read_at):"
done
```

---

### Phase 2: Content Analysis

**CLAUDE.md Structure Check:**
Read CLAUDE.md and evaluate:

| Check | Issue | Action |
|-------|-------|--------|
| Redundant sections | Content repeated in memories | Move to memory, add pointer |
| Embedded code blocks | Long examples in-line | Move to references file |
| Verbose explanations | > 3 sentences per rule | Condense to single line |
| Missing pointers | Full content instead of references | Add "See: [memory]" |
| Outdated content | References deleted files/symbols | Update or remove |
| Generic rules | Claude already knows these | Remove entirely |

**Command Analysis:**
For each command > 300 lines:

| Check | Issue | Action |
|-------|-------|--------|
| Duplicate content | Same instructions in multiple commands | Extract to shared reference |
| Embedded examples | Long code blocks | Move to external file |
| Step-by-step verbosity | Could be condensed | Use numbered lists |
| Missing progressive disclosure | All content loads at once | Split into phases |

**Skill Analysis:**
For each SKILL.md:

| Check | Issue | Action |
|-------|-------|--------|
| Over 3000 words | Too verbose | Split into SKILL.md + references/ |
| No references folder | Missing progressive disclosure | Create references/ |
| Vague triggers | "When needed" type conditions | Add specific trigger phrases |
| Embedded examples | Long code in skill body | Move to references/ |

**Memory Analysis:**
For each memory:

| Check | Issue | Action |
|-------|-------|--------|
| Missing metadata | No type/purpose/read_at | Add YAML frontmatter |
| Always-read content | Large memory read every session | Split or make conditional |
| Redundant with CLAUDE.md | Same content in both | Remove from one location |
| Template not marked | Template memory without read_at: never | Mark as template |

---

### Phase 3: Redundancy Detection

**Cross-Component Redundancy:**
Search for duplicated content across:
- CLAUDE.md ↔ Memories
- Commands ↔ Commands
- Commands ↔ CLAUDE.md
- Memories ↔ Memories

Use pattern matching:
```python
# Conceptual - look for similar content
search_for_pattern("Tool Priority", relative_path=".")
search_for_pattern("When to Read", relative_path=".")
search_for_pattern("decision tree", relative_path=".")
```

**Instruction Overlap:**
Identify instructions that appear in multiple places with slight variations.

---

### Phase 4: Context Load Estimation

**Base Context Load:**
Estimate tokens loaded at session start:
- System prompt: ~5,000 tokens (Claude Code base)
- CLAUDE.md: `wc -c CLAUDE.md` / 4 (rough token estimate)
- MCP tool definitions: ~500 tokens per MCP

**Per-Command Context:**
When a command is invoked:
- Command file: `wc -c file.md` / 4
- Referenced memories: Sum of memory sizes / 4
- Any linked files: Sum of linked file sizes / 4

**Calculate Available Context:**
```
200,000 tokens (standard) - base_load = available_for_work
```

If available < 150,000 tokens → Warning
If available < 100,000 tokens → Critical

---

## Optimization Report

Generate this report structure:

```
## Claude Code Optimization Report

### Executive Summary
- **Overall Status**: [Optimal / Needs Attention / Critical]
- **Estimated Base Context**: [X] tokens ([Y]% of 200K)
- **Primary Issues**: [count] found
- **Quick Wins**: [count] available

### CLAUDE.md Analysis
| Metric | Value | Status | Recommendation |
|--------|-------|--------|----------------|
| Lines | [X] | [OK/WARN/CRIT] | [action if needed] |
| Size | [X KB] | [OK/WARN/CRIT] | [action if needed] |
| Hard Rules | [X] | [OK/WARN/CRIT] | [action if needed] |
| Soft Rules | [X] | [OK/WARN/CRIT] | [action if needed] |
| Embedded Code | [X blocks] | [OK/WARN/CRIT] | [action if needed] |

**Content Issues:**
1. [Issue]: [Location] → [Fix]
2. ...

### Commands Analysis
| Command | Lines | Size | Status | Issue |
|---------|-------|------|--------|-------|
| [name] | [X] | [Y KB] | [OK/WARN/CRIT] | [issue if any] |
| ... | ... | ... | ... | ... |

**Optimization Opportunities:**
1. [Command]: [Issue] → [Fix]
2. ...

### Skills Analysis
| Skill | Words | Has References | Status |
|-------|-------|----------------|--------|
| [name] | [X] | [Yes/No] | [OK/WARN/CRIT] |

**Issues:**
1. [Issue] → [Fix]

### Memories Analysis
| Memory | Size | Has Metadata | Read-At | Status |
|--------|------|--------------|---------|--------|
| [name] | [X KB] | [Yes/No] | [value] | [OK/WARN/CRIT] |

**Issues:**
1. [Issue] → [Fix]

### Redundancy Report
| Content | Location 1 | Location 2 | Recommendation |
|---------|------------|------------|----------------|
| [description] | [file:section] | [file:section] | [which to keep] |

### Context Budget
| Component | Estimated Tokens | % of Budget |
|-----------|-----------------|-------------|
| System Prompt | ~5,000 | 2.5% |
| CLAUDE.md | [X] | [Y]% |
| MCP Tools | [X] | [Y]% |
| **Base Total** | [X] | [Y]% |
| **Available** | [X] | [Y]% |

### Prioritized Recommendations

**High Priority (Do Now):**
1. [ ] [Action with expected impact]
2. [ ] ...

**Medium Priority (This Week):**
1. [ ] [Action with expected impact]
2. [ ] ...

**Low Priority (Nice to Have):**
1. [ ] [Action with expected impact]
2. [ ] ...

### Auto-Fix Available
The following optimizations can be applied automatically:
1. [ ] Add missing memory metadata
2. [ ] Create references/ folders for large skills
3. [ ] Add "See: [memory]" pointers to CLAUDE.md
4. [ ] Condense verbose instructions

Run with `--fix` to apply safe optimizations.
```

---

## Execution Options

**Analysis only (default):**
```
/claude-learns.optimize
```

**Focus on specific component:**
```
/claude-learns.optimize claude.md
/claude-learns.optimize commands
/claude-learns.optimize skills
/claude-learns.optimize memories
```

**Apply safe fixes:**
```
/claude-learns.optimize --fix
```

**Generate detailed report file:**
```
/claude-learns.optimize --report
```
Creates `.claude/optimization-report.md` with full analysis.

---

## Safe Auto-Fix Rules

Only these changes can be auto-applied:

| Fix | Criteria | Action |
|-----|----------|--------|
| Add memory metadata | Missing YAML frontmatter | Add standard metadata block |
| Create references folder | Skill > 3000 words, no references/ | Create empty references/ |
| Condense duplicate empty lines | Multiple consecutive blank lines | Reduce to single blank |
| Add pointer comments | Content exists in both CLAUDE.md and memory | Add "See: [memory]" |

**Never auto-fix:**
- Content removal (always ask first)
- Structural reorganization
- Memory merging
- Command splitting

---

## Post-Optimization

After optimization:

1. **Verify functionality** - Test key commands still work
2. **Update manifest** - If template files changed:
   ```bash
   python .claude/scripts/generate-manifest.py --version [X.Y.Z]
   ```
3. **Commit changes** - Group related optimizations
4. **Monitor impact** - Check if sessions feel more responsive

---

## Related Commands

- `/claude-learns.audit` - Check accuracy and completeness (not optimization)
- `/claude-learns.learn` - Route new knowledge to appropriate locations
- `/claude-learns.update` - Sync with template updates

---

Focus area (optional): $ARGUMENTS
