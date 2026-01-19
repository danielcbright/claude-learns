# /claude-learns.learn - Learning Loop with Intelligent Memory Routing

Perform a learning loop review for this session, routing learnings to the correct memory locations.

**Modes:**
- `/claude-learns.learn` → Quick mode: identify learnings, show routing, ask before writing
- `/claude-learns.learn --deep` → Full mode: comprehensive analysis with all templates
- `/claude-learns.learn --skills` → Skills mode: check for applicable Anthropic skills only
- `/claude-learns.learn --claude` → CLAUDE.md mode: fetch best practices and update CLAUDE.md only

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

## Quick Mode (`/claude-learns.learn`)

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

## CLAUDE.md Updates

Fetching latest best practices from Anthropic...
→ **Key Entry Points** - Add `OrderService` at `src/services/order.ts`
→ **Health Check** - ⚠️ Missing "Code Conventions" section

## Skill Suggestions

Checking anthropics/claude-learns.skills for applicable skills...
→ **webapp-testing** may help (you worked on form validation)
  Install: `/plugin install webapp-testing@anthropic-agent-skills`

---

Want me to apply these? (y = all / n = none / numbers = select specific)
```

If **yes/y**: Write memories, update CLAUDE.md, install accepted skills.
If **no/n**: End without writing.
If **numbers** (e.g., "1,3,5"): Apply only selected items.
If **skills-only**: Skip memories/CLAUDE.md, only install skills.
If **claude-only**: Skip memories/skills, only update CLAUDE.md.

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

## Deep Mode (`/claude-learns.learn --deep`)

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
- Were any debugging sessions completed using `/claude-learns.eliminate`?
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

## CLAUDE.md Updates (fetched latest best practices from Anthropic)

### Additions
→ Key Entry Points
  - Added: `{Symbol}` at `{path}`

→ Current Memories
  - Added: `{memory-name}` - {purpose}

→ Active Skills
  - Added: {skill-name} - {purpose}

### Health Check
  - ✅ {passing check}
  - ⚠️ {suggestion}

## Skill Suggestions
→ {skill-name} may help ({reason})
  Install: `/plugin install {skill}@anthropic-agent-skills`

## No Destination (Need Input)
  - "{learning that didn't fit}" → Where should this go?
```

### Step 4: CLAUDE.md Updates

Apply the **CLAUDE.md Updates** process (see full section below):

1. **Fetch latest best practices** from Anthropic docs
2. **Analyze session** for CLAUDE.md-worthy learnings:
   - New entry points discovered? → Key Entry Points table
   - New memories created? → Current Memories table
   - New skills installed? → Active Skills section
   - Workflow improvements? → Common Workflows section
   - Code conventions discovered? → Code Conventions section
   - Bash commands worth saving? → Quick Reference section
3. **Run health check** against Anthropic guidelines
4. **Present updates** with specific edits
5. **Apply if approved** using Edit tool

### Step 5: Anthropic Skills Discovery

Check if any official Anthropic skills would benefit this project. See the full **Anthropic Skills Discovery** section below.

---

## Anthropic Skills Discovery

**Always run this check** as part of `/claude-learns.learn` and `/claude-learns.learn --deep`. This step fetches the latest skills from the official Anthropic repository and suggests applicable ones based on session patterns.

### Available Anthropic Skills

Fetch the current skill list from: `https://github.com/anthropics/skills/tree/main/skills`

As of last update, available skills include:

| Skill | Purpose | Suggested When |
|-------|---------|----------------|
| `algorithmic-art` | Generate algorithmic/generative art | Session involved creative coding, canvas, SVG generation |
| `brand-guidelines` | Apply brand consistency | Session involved branding, style guides, design systems |
| `canvas-design` | Create canvas-based designs | Session involved HTML canvas, visualizations |
| `doc-coauthoring` | Collaborative document editing | Session involved document workflows, content creation |
| `docx` | Word document processing | Session involved .docx files, Word documents |
| `frontend-design` | Build frontend interfaces | Session involved UI development, web components |
| `internal-comms` | Internal communications | Session involved company communications, announcements |
| `mcp-builder` | Build MCP servers | Session involved creating MCP integrations |
| `pdf` | PDF processing | Session involved PDF files, extraction, manipulation |
| `pptx` | PowerPoint processing | Session involved presentations, slides |
| `skill-creator` | Create new skills | Session involved building custom skills |
| `slack-gif-creator` | Create Slack GIFs | Session involved Slack content, animated images |
| `theme-factory` | Generate themes/styling | Session involved theming, color schemes, CSS |
| `web-artifacts-builder` | Build web artifacts | Session involved web components, embeddable content |
| `webapp-testing` | Test web applications | Session involved testing, QA, browser automation |
| `xlsx` | Excel processing | Session involved spreadsheets, .xlsx files |

### Skill Matching Process

1. **Analyze Session Patterns**: What types of tasks were performed?
   - Document processing? → Check `docx`, `pdf`, `pptx`, `xlsx`
   - Frontend/UI work? → Check `frontend-design`, `canvas-design`, `theme-factory`
   - Testing? → Check `webapp-testing`
   - Building integrations? → Check `mcp-builder`
   - Creating skills? → Check `skill-creator`

2. **Check Currently Installed Skills**:
   ```bash
   ls ~/.claude/skills/  # User-level skills
   ls .claude/skills/    # Project-level skills
   ```

3. **Fetch Latest Descriptions**: For any matching skills, fetch the current SKILL.md from:
   ```
   https://raw.githubusercontent.com/anthropics/skills/main/skills/{skill-name}/SKILL.md
   ```

4. **Present Recommendations**:
   ```
   ## Skill Recommendations

   Based on this session, these Anthropic skills may help:

   1. **frontend-design** - You worked on UI components
      → Provides: Design patterns, component templates, accessibility guidelines
      → Install: `/plugin install frontend-design@anthropic-agent-skills`

   2. **webapp-testing** - You discussed testing approaches
      → Provides: Testing workflows, browser automation patterns
      → Install: `/plugin install webapp-testing@anthropic-agent-skills`

   Would you like me to install any of these? (specify by number or 'all')
   ```

### Installation Methods

**Via Claude Code Plugin System (Recommended):**
```bash
# Register the Anthropic skills marketplace (one-time)
/plugin marketplace add anthropics/skills

# Install specific skills
/plugin install {skill-name}@anthropic-agent-skills
```

**Via Direct Copy (for customization):**
```bash
# Fetch skill to project
mkdir -p .claude/skills/{skill-name}
curl -o .claude/skills/{skill-name}/SKILL.md \
  https://raw.githubusercontent.com/anthropics/skills/main/skills/{skill-name}/SKILL.md

# Also fetch any bundled resources if needed
# Check the skill's directory structure at:
# https://github.com/anthropics/skills/tree/main/skills/{skill-name}
```

### Post-Installation

After installing a skill:

1. **Update CLAUDE.md**: Add the skill to the "Active Skills" section
2. **Test the skill**: Run a task that should trigger it
3. **Capture learnings**: Note any project-specific customizations needed

### Skills Mode (`/claude-learns.learn --skills`)

Run skill discovery only (skip memory routing):

```
## Skill Discovery Results

### Session Analysis
- Tasks performed: {list of task types}
- Technologies used: {list of techs}
- Pain points: {what was difficult}

### Recommended Skills
{numbered list with install commands}

### Already Installed
{list of matching installed skills}

Would you like to install any recommended skills?
```

---

## CLAUDE.md Updates

**Always run this check** as part of `/claude-learns.learn` and `/claude-learns.learn --deep`. This step ensures CLAUDE.md stays current with learnings and follows Anthropic's latest best practices.

### Fetch Latest Best Practices

Before suggesting updates, fetch current Anthropic guidance:

```
Primary sources (check in order):
1. https://code.claude.com/docs/en/memory
2. https://www.anthropic.com/engineering/claude-code-best-practices
```

**Current Best Practices Summary** (fetch latest to verify):

| Principle | Guidance |
|-----------|----------|
| **Be specific** | "Use 2-space indentation" not "Format code properly" |
| **Keep concise** | Context window is shared; justify each token |
| **Iterate** | Treat CLAUDE.md like production prompts—refine over time |
| **Use emphasis** | Add "IMPORTANT" or "YOU MUST" for critical rules |
| **Structure well** | Bullet points under descriptive markdown headings |

**Recommended Sections** (per Anthropic docs):
- Bash commands with descriptions
- Core files and utility functions
- Code style guidelines
- Testing instructions
- Repository etiquette (branches, merges)
- Developer environment setup
- Project-specific quirks
- Workflow preferences

### CLAUDE.md Update Routing Map

| Learning Type | CLAUDE.md Section | Template |
|---------------|-------------------|----------|
| New entry point discovered | **Key Entry Points** table | `\| {Pattern} \| {path} \| {Purpose} \|` |
| New skill installed | **Active Skills** section | See skill template below |
| New memory created | **Current Memories** table | `\| {name} \| {purpose} \| {when to read} \|` |
| Workflow improvement | **Common Workflows** section | Add/claude-learns.update workflow steps |
| New bash command | **Quick Reference** or new section | `- \`{command}\`: {description}` |
| Code convention discovered | **Code Conventions** section | Add bullet point |
| Architecture insight | **Architecture Overview** section | Update description |
| Gotcha/quirk found | **Troubleshooting** or new section | Add to common issues table |

### Update Templates

#### For Key Entry Points:
```markdown
| `{SymbolName}` | `{path/to/file.ts}` | {Brief purpose description} |
```

#### For Active Skills:
```markdown
#### Skill: {skill-name}
- **Purpose**: {What this skill does}
- **Use when**: {Specific scenarios that trigger it}
- **Notes**: {Any project-specific configuration}
```

#### For Current Memories:
```markdown
| `{memory-name}` | {What it contains} | {When Claude should read it} |
```

#### For Bash Commands:
```markdown
- `{command}`: {What it does}
```

#### For Workflow Updates:
```markdown
### {Workflow Name}

\`\`\`
1. {Step 1}
2. {Step 2}
...
\`\`\`
```

### CLAUDE.md Update Process

1. **Analyze session** for CLAUDE.md-worthy learnings
2. **Check current CLAUDE.md** for existing content (avoid duplicates)
3. **Fetch latest best practices** from Anthropic docs
4. **Generate updates** using templates above
5. **Present to user**:

```
## CLAUDE.md Updates

Based on this session and Anthropic's latest best practices:

### Additions
1. **Key Entry Points** - Add:
   | `AuthService` | `src/services/auth.ts` | Authentication and token management |

2. **Current Memories** - Add:
   | `api-patterns` | REST API conventions | Before implementing endpoints |

3. **Active Skills** - Add:
   #### Skill: frontend-design
   - **Purpose**: Build frontend interfaces with high design quality
   - **Use when**: Creating UI components, pages, or web applications
   - **Notes**: Installed via /claude-learns.learn skill suggestion

### Modifications
4. **Common Workflows > Debugging** - Update step 3:
   - Old: "Form hypothesis"
   - New: "Form hypothesis, verify with targeted reads"

### Best Practice Suggestions
5. **Code Conventions** - Section is missing (Anthropic recommends including this)
   → Add section with discovered conventions?

---

Apply these updates? (y/n/select by number)
```

6. **If approved**: Apply edits to CLAUDE.md using Edit tool
7. **Verify**: Confirm updates were applied correctly

### Best Practice Compliance Check

During `/claude-learns.learn --deep`, also check if CLAUDE.md follows Anthropic guidelines:

```
## CLAUDE.md Health Check

Checking against Anthropic best practices...

✅ Has bash commands section
✅ Uses bullet points under headings
⚠️  Missing: Code style guidelines section
⚠️  Missing: Testing instructions
✅ Concise (under 500 lines)
⚠️  Could add emphasis: No "IMPORTANT" markers for critical rules

Suggestions:
1. Add "## Code Conventions" section
2. Add "## Testing" section with test commands
3. Add "IMPORTANT:" prefix to critical workflow rules

Apply suggestions? (y/n)
```

### File Hierarchy Awareness

Remember CLAUDE.md can exist at multiple levels:

| Location | Scope | When to Update |
|----------|-------|----------------|
| `./CLAUDE.md` | Project team | Project-specific learnings |
| `./.claude/CLAUDE.md` | Project team | Alternative location |
| `~/.claude/CLAUDE.md` | Personal | Cross-project preferences |
| `./CLAUDE.local.md` | Personal + project | Personal project prefs |

**Default**: Update `./CLAUDE.md` (or `./.claude/CLAUDE.md` if that's the project pattern)

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
/claude-learns.learn                    → Quick: identify, route, ask before writing
/claude-learns.learn --deep             → Full: comprehensive with templates
/claude-learns.learn --skills           → Skills only: check for applicable Anthropic skills
/claude-learns.learn --claude           → CLAUDE.md only: fetch best practices, update CLAUDE.md
/claude-learns.learn "auth refactor"    → Focus on specific context
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
