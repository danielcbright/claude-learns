# /learn - Learning Loop with Intelligent Memory Routing

Perform a learning loop review for this session, routing learnings to the correct memory locations.

**Modes:**
- `/learn` → Quick mode: identify learnings, show routing, ask before writing
- `/learn --deep` → Full mode: comprehensive analysis with all templates

---

## Memory Routing Map

| Learning Type | Destination | Example |
|---------------|-------------|---------|
| Code patterns, navigation tips, codebase gotchas | `.serena/memories/` | "The auth module uses a factory pattern" |
| Spec corrections, what was claimed vs reality | `.specify/memory/corrections.md` | "Claimed login worked, but error handling was missing" |
| Architectural decisions, why we chose X | `.serena/memories/decision-log.md` | "Chose Redis over Memcached because..." |
| Debugging heuristics, what hypotheses worked | `.elimination/learned/heuristics.yaml` | "Timeout errors usually mean connection pool" |
| Bug patterns specific to features | `.serena/memories/common-bugs.md` | "Auth feature often has token expiry edge cases" |
| General session insights, quick reference | `.serena/memories/claude_code_patterns.md` | "Run npm test before commits" |

**Key distinction:**
- `.serena/memories/` → General codebase knowledge, patterns, decisions
- `.specify/memory/` → Spec-specific: constitution (rules) and corrections (claim vs reality)
- `.elimination/learned/` → Debugging heuristics (YAML format)

---

## Quick Mode (`/learn`)

Fast identification and routing. Scan session and output:

```
## Session Learnings

1. **[Type: Code Pattern]** OrderService uses repository pattern
   → .serena/memories/claude_code_patterns.md

2. **[Type: Correction]** Claimed validation complete, but email regex missed edge case
   → .specify/memory/corrections.md

3. **[Type: Decision]** Chose PostgreSQL over MongoDB for transactions
   → .serena/memories/decision-log.md

4. **[Type: Heuristic]** Import errors in this project usually mean circular deps
   → .elimination/learned/heuristics.yaml

5. **[Type: Bug Pattern]** Auth tokens often expire during long form submissions
   → .serena/memories/common-bugs.md

---

Want me to write these? (y/n)
```

If **yes**: Write each learning to its destination with minimal formatting.
If **no**: End without writing.

### Quick Mode Categorization

For each potential learning, quickly ask:

| Question | Route To |
|----------|----------|
| How does code work? | `.serena/memories/` |
| Claimed done but wasn't? | `.specify/memory/corrections.md` |
| Why did we choose X? | `.serena/memories/decision-log.md` |
| What debugging pattern worked? | `.elimination/learned/heuristics.yaml` |
| What bug keeps happening? | `.serena/memories/common-bugs.md` |
| General tip? | `.serena/memories/claude_code_patterns.md` |
| Doesn't fit? | Ask user |

---

## Deep Mode (`/learn --deep`)

Comprehensive analysis with full templates and CLAUDE.md review.

### Step 1: Gather Learnings

Analyze what happened in this session:

#### Pattern Recognition
- Did I use any approach multiple times that should be documented?
- Did I discover a code pattern that future sessions should know?
- Did I find a useful command sequence worth saving?

#### Gotchas & Pitfalls
- Did anything unexpected happen?
- Did I hit an error that was non-obvious to debug?
- Did I make an incorrect assumption?

#### Workflow Insights
- What took longer than expected? Why?
- What tool or skill would have helped?
- Was any CLAUDE.md guidance missing or wrong?

#### Architecture Knowledge
- Did I learn something about how this codebase works?
- Did I discover undocumented dependencies or relationships?
- Did I understand a design decision that should be captured?

#### Spec & Verification Learnings
- Did I claim something was done that wasn't? → **Correction**
- Did the user correct my understanding? → **Correction**
- Did spec deviations reveal missing acceptance criteria? → **Correction**

#### Elimination Debugging Review

Check for completed elimination sessions in `.elimination/archive/`:
- Were any debugging sessions completed using `/eliminate`?
- What patterns emerged from hypothesis generation?
- Which heuristics proved most useful?
- Were any false positives eliminated (lessons to remember)?

#### Skill Update Opportunities
- Did a skill's instructions prove inadequate or misleading?
- Did I discover a pattern that would help OTHER projects using this skill?

### Step 2: Write with Full Templates

#### For `.serena/memories/` entries:

```markdown
### {Date}: {Brief Title}

**Context**: {What feature/task this relates to}

**Learning**: {The actual insight}

**Source**: {How we learned this - debugging session, user correction, discovery, etc.}
```

#### For `.specify/memory/corrections.md` entries:

```markdown
### CORR-{id}: {Feature} - {Date}

**Feature Type**: {category}

**Claimed**: "{exact claim made}"

**Actually**: {what actually happened}

**Would Have Caught It**:
- Test: {specific verification}
- Check: {what to look for}

**Pattern**: {generalized for future}
```

#### For `.serena/memories/decision-log.md` entries:

```markdown
### {Date}: {Decision Title}

**Context**: {What problem we were solving}

**Decision**: {What we chose}

**Alternatives Considered**:
- {Option A}: {why rejected}
- {Option B}: {why rejected}

**Rationale**: {Why this choice was made}

**Implications**: {What this means going forward}
```

#### For `.elimination/learned/heuristics.yaml` entries:

```yaml
- id: "heur-{next_id}"
  name: "{pattern_name_snake_case}"
  description: "{when to apply this pattern}"

  trigger_conditions:
    - condition: "{symptom that suggests this pattern}"

  hypothesis_template:
    domain: "{Code|Config|Data|Infrastructure|Concurrency|Dependencies}"
    description_template: "{hypothesis text with {symptom} placeholder}"
    initial_confidence: 0.{xx}
    suggested_evidence:
      - type: "{evidence_type}"
        description: "{what to check}"
        priority: high

  statistics:
    times_triggered: 0
    successful_predictions: 0
    success_rate: 0.0
    last_updated: "{date}"
```

#### For `.serena/memories/common-bugs.md` entries:

```markdown
### {Feature}: {Bug Pattern}

**Date Added**: {date}

**Pattern**: {What tends to go wrong}

**Root Cause**: {Why this happens}

**Prevention**: {How to avoid it}

**Detection**: {How to catch it early}
```

### Step 3: Output Summary

```
## Learnings Captured

→ .serena/memories/claude_code_patterns.md
  - Added: "{brief description}"

→ .specify/memory/corrections.md
  - Added: CORR-{id}: {brief description}

→ .serena/memories/decision-log.md
  - Added: "{decision title}"

→ .elimination/learned/heuristics.yaml
  - Added: {heuristic_name} (prior: 0.{x})

→ .serena/memories/common-bugs.md
  - Added: {feature}: {bug pattern}

## CLAUDE.md Updates
  - {section}: {what changed}

## No Destination (Need Input)
  - "{learning that didn't fit}" → Where should this go?
```

### Step 4: CLAUDE.md and Skill Updates

- Does any guidance need correction?
- Should new memories be added to the "Current Memories" table?
- Were any entry points discovered?
- Would any learning help OTHER projects? → Update skill at `~/.claude/skills/*/skill.md`

---

## Tool Usage

Use Serena's memory tools when available:
- `list_memories()` → See what memories exist
- `read_memory("name")` → Read existing memory content
- `write_memory("name", "content")` → Create or overwrite memory
- `edit_memory("name", ...)` → Modify existing memory

For `.specify/` and `.elimination/` files, use standard file operations (Read/Edit).

---

## Quick Reference

```
/learn                    → Quick: identify, route, ask before writing
/learn --deep             → Full: comprehensive with templates
/learn "auth refactor"    → Focus on specific context
```

**Routing Decision Tree (check in order, stop at first match):**

```
ROUTING PRIORITY
════════════════
1. Was it "claimed done but wasn't"?
   → corrections.md ONLY (never common-bugs.md)

2. Is it a quantifiable pattern with confidence data?
   → heuristics.yaml (machine-readable statistics)

3. Has this exact bug occurred 2+ times?
   → common-bugs.md (recurring patterns by feature)

4. Is it a quick reference for elimination sessions?
   → elimination_patterns.md (human-readable)

5. Is it a detailed insight from ONE debugging session?
   → debugging-lessons.md (narrative insights)

6. Is it a general tip or codebase pattern?
   → claude_code_patterns.md (catch-all)

7. Is it a decision with rationale?
   → decision-log.md (why we chose X)

8. Doesn't fit any above?
   → Ask user
```

---

Session context to review: $ARGUMENTS
