---
type: template
name: claude-learns
version: "1.0"
purpose: Self-learning Claude Code template with persistent memory
install_guide: INSTALL.md
repository: https://github.com/danielcbright/claude-learns
---

# CLAUDE.md - [PROJECT_NAME]

> **READ THIS FILE FIRST** before starting any task in this project.

<!--
=============================================================================
TEMPLATE MODE DETECTION
=============================================================================
You are in the claude-learns REPOSITORY (the template source), not a project
that has adopted this template.

FOR INSTALLATION TASKS:
  If the user asks you to "install", "use", "copy", or "incorporate" this
  template into another project, read INSTALL.md for detailed instructions.

FOR DEVELOPMENT TASKS:
  If the user asks you to modify, sync, or improve the template itself,
  read DEVELOPMENT.md first. Key points:
  - Dual-location architecture: root files (dev) vs template/ (distribution)
  - NEVER rsync blindly - follow Category A/B/C sync procedures
  - template/ must keep [PLACEHOLDERS], not real values
  - Educational samples in template/.specify/ are intentional

Quick reference for installation:
1. Read INSTALL.md for full installation guide
2. Copy template/ contents to target project
3. Customize CLAUDE.md with project-specific values
4. Optionally configure MCP servers for enhanced functionality
=============================================================================
-->

## Project Overview

<!-- Customize this section for your specific project -->
- **Project Name**: [PROJECT_NAME]
- **Type**: [e.g., Web App, CLI Tool, Library, Microservice]
- **Primary Languages**: [e.g., TypeScript, Python, Go]
- **Key Frameworks**: [e.g., React, FastAPI, Express]

---

## Memory Management

This project uses a persistent memory system to help Claude learn and improve over time.

### Tool Priority Order

**IMPORTANT:** Always follow this order to minimize token usage:

1. **First**: Check `list_memories()` for relevant context
2. **Then**: Use `get_symbols_overview()` for file structure (if using Serena MCP)
3. **Then**: Use `find_symbol()` for targeted lookups (if using Serena MCP)
4. **Fallback**: Use `search_for_pattern()` for non-code files or unknown names
5. **Last resort**: Full file reads (avoid unless strictly necessary)

### Before Starting Any Task

- [ ] Run `/mcp` to verify MCP servers are connected (if applicable)
- [ ] Read relevant memories (`list_memories()` → `read_memory()`)
- [ ] Check git status for clean working state

### After Completing Tasks

- [ ] Write memory if architectural decision was made
- [ ] Update memory if existing info became stale
- [ ] Run tests/linting as appropriate

### Token Efficiency

**IMPORTANT:** Context window is a shared resource. Every token counts.

- **NEVER** read entire files unless absolutely necessary
- Use targeted symbol lookups over full file reads
- Leverage memories to avoid re-exploring the same areas
- Prefer `find_symbol()` with `include_body=True` over `read_file()`

---

## Memory Guidelines

### When to Write Memories

- After discovering codebase patterns worth preserving
- After making architectural decisions
- Before `/clear` to preserve important context
- When documenting workarounds or gotchas

### Naming Conventions

- Use kebab-case: `auth-architecture`, `api-design-decisions`
- Be descriptive—avoid generic names like "notes" or "temp"
- Include dates for temporal tracking if needed: `auth-fix-2025-01`

### Memory Maintenance

- Review `.serena/memories/` periodically for stale content
- Consolidate redundant memories
- Delete obsolete information
- Update CLAUDE.md if memory purposes change

### Current Memories

<!-- Claude: Populate this after onboarding -->
| Memory | Purpose | When to Read |
|--------|---------|--------------|
| `claude_code_patterns` | Session quick reference | Start of any task |
| `elimination_patterns` | Elimination debugging quick reference | Before `/claude-learns.eliminate` sessions |
| `debugging-lessons` | Past bugs and resolutions | Before debugging sessions |
| `common-bugs` | Recurring patterns by feature | When debugging known areas |
| `decision-log` | Why we chose X over Y | Before architectural changes |
| `tool-documentation` | Links to latest docs for all tools | Before implementing with external tools |

**Spec Memory** (`.specify/memory/`):
| Memory | Purpose | When to Read |
|--------|---------|--------------|
| `constitution.md` | Non-negotiable project rules | Before any implementation |
| `corrections.md` | Past premature completion claims | During `/claude-learns.spec-verify` |
<!-- Add more memories as created -->

---

## MCP Integration (Optional)

This template works with various MCP servers for enhanced functionality:

### Recommended MCPs

| Need | Tool | When to Use |
|------|------|-------------|
| Code navigation & editing | **Serena** | Finding symbols, relationships, precise edits |
| External library docs | **Context7** | Looking up API usage, framework patterns |
| Complex reasoning | **Sequential Thinking** | Architecture decisions, debugging strategies |
| File operations | **Built-in** | Simple reads when MCPs aren't needed |

### Installing MCPs

If a task would benefit from an unavailable MCP, suggest it:
- **Serena**: `claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)`
- **Context7**: Fetch up-to-date library documentation
- **Sequential Thinking**: Break down complex decisions

---

## Serena MCP Tools Reference

When Serena MCP is connected, use these tools instead of direct file operations.

### Project Activation

Before using any Serena tools, activate the project:
```
activate_project("/path/to/project")
```

Check if onboarding is needed:
```
check_onboarding_performed()
```

### Memory Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `list_memories()` | See available memories | Returns list of memory names |
| `read_memory("name")` | Read memory content | `read_memory("decision-log")` |
| `write_memory("name", content)` | Create/overwrite memory | `write_memory("new-feature", "# Notes\n...")` |
| `edit_memory("name", needle, repl, mode)` | Edit existing memory | See below |
| `delete_memory("name")` | Remove memory | Only on user request |

**Editing memories** (preferred over overwriting):
```python
# Literal replacement
edit_memory("decision-log",
    needle="*Total Decisions: 1*",
    repl="*Total Decisions: 2*",
    mode="literal")

# Regex replacement (for complex edits)
edit_memory("decision-log",
    needle="### DEC-001:.*?Review Date\\*\\*: [^\\n]+",
    repl="### DEC-001: ... (new content)",
    mode="regex")
```

### Code Navigation Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `get_symbols_overview(path)` | File structure overview | `get_symbols_overview("src/auth.ts")` |
| `find_symbol(pattern)` | Find symbol by name | `find_symbol("AuthService")` |
| `find_symbol(pattern, depth=1)` | Include children | `find_symbol("AuthService", depth=1)` |
| `find_symbol(pattern, include_body=True)` | Get implementation | Full source code |
| `find_referencing_symbols(name, path)` | Who uses this? | `find_referencing_symbols("validateToken", "src/auth.ts")` |

**Name path patterns**:
```python
find_symbol("method")              # Any symbol named "method"
find_symbol("Class/method")        # Method within Class
find_symbol("/Class/method")       # Exact path (absolute)
find_symbol("Class/method[0]")     # First overload
```

### Code Editing Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `replace_symbol_body(path, file, body)` | Replace implementation | Entire function/class |
| `insert_after_symbol(path, file, body)` | Add after symbol | New method after existing |
| `insert_before_symbol(path, file, body)` | Add before symbol | Import before first symbol |
| `rename_symbol(path, file, new_name)` | Rename everywhere | Refactor across codebase |

**Example: Replace a method**:
```python
replace_symbol_body(
    name_path="AuthService/validateToken",
    relative_path="src/auth.ts",
    body="async validateToken(token: string): Promise<boolean> {\n  // new implementation\n}"
)
```

### Search Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `search_for_pattern(pattern)` | Regex search in files | `search_for_pattern("TODO.*auth")` |
| `search_for_pattern(pattern, relative_path="src/")` | Scoped search | Only in src/ |
| `search_for_pattern(pattern, restrict_search_to_code_files=True)` | Code only | Skip config/docs |

### File Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `read_file(path)` | Read file content | When symbols won't help |
| `create_text_file(path, content)` | Create new file | New modules |
| `replace_content(path, needle, repl, mode)` | Edit file content | Non-symbol edits |
| `list_dir(path, recursive)` | List directory | Exploring structure |
| `find_file(mask, path)` | Find files by pattern | `find_file("*.test.ts", ".")` |

### Tool Selection Guide

```
Need to...                          → Use this tool
────────────────────────────────────────────────────
Read/write project knowledge        → Memory tools
Find a class/function               → find_symbol()
See what's in a file                → get_symbols_overview()
Find who calls a function           → find_referencing_symbols()
Replace a function body             → replace_symbol_body()
Search for text patterns            → search_for_pattern()
Edit non-code files                 → replace_content() or edit_memory()
Read config/docs                    → read_file()
```

### When NOT to Use Serena

- Simple one-off file reads → Built-in Read tool is faster
- Files Serena can't parse → Use built-in tools
- Quick grep-style searches → Built-in Grep may suffice

---

## Key Entry Points

<!-- Claude: Document commonly searched symbols for efficient lookups -->

| Pattern | Location | Purpose |
|---------|----------|---------|
| `[MAIN_ENTRY]` | [path] | Application entry point |
| `[KEY_CLASS]` | [path] | Core business logic |
| `[CONFIG]` | [path] | Configuration handling |
<!-- Add project-specific entry points -->

---

## Learning Loop System

### Learning Triggers

**Recommend updates when you encounter:**

| Trigger | Action |
|---------|--------|
| Repeated pattern across 2+ tasks | Suggest new memory |
| Gotcha or non-obvious behavior | Add to gotchas memory |
| CLAUDE.md guidance was wrong | Suggest CLAUDE.md update |
| Workflow inefficiency discovered | Suggest improvement |
| Architecture insight gained | Update relevant memory |

### At Natural Breakpoints

Proactively offer learning loop check:

```
Based on this session, I recommend:
1. **New Memory**: [name] - [reason]
2. **CLAUDE.md Update**: [section] - [what to change]

Would you like me to make these updates?
```

---

## Project-Specific Patterns

<!-- Customize this section for your project -->

### Architecture Overview

```
[Document your project's key architectural patterns]
- How modules communicate
- State management approach
- Error handling conventions
```

### Code Conventions

<!-- IMPORTANT: Customize these for your project. Be specific per Anthropic guidance. -->

**Naming:**
- Variables/functions: `camelCase` (JS/TS) or `snake_case` (Python)
- Classes/types: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Files: `kebab-case.ts` or `snake_case.py`

**Imports:**
- Group by: stdlib → external packages → internal modules
- Sort alphabetically within groups
- Prefer named imports over default imports

**File Organization:**
- One component/class per file (exceptions: closely related utilities)
- Co-locate tests with source: `foo.ts` → `foo.test.ts`
- Keep files under 300 lines; split if larger

**Code Style:**
- [INDENTATION]: [e.g., 2 spaces for JS/TS, 4 spaces for Python]
- [LINE_LENGTH]: [e.g., 100 characters max]
- [QUOTES]: [e.g., single quotes for JS, double for Python]
- Trailing commas: yes (for cleaner diffs)
- Semicolons: [yes/no based on project]

**Comments:**
- Explain "why", not "what"
- Use JSDoc/docstrings for public APIs
- TODO format: `// TODO(username): description`

### Testing Strategy

```
[Document testing approach]
- Test location/naming
- How to run tests
- Coverage expectations
```

---

## Common Workflows

### Adding a New Feature

```
1. /claude-learns.spec-create [feature]  → Define requirements and acceptance criteria
2. Review spec with stakeholder if needed
3. /go implement                         → Build per spec
4. /claude-learns.spec-validate [feature]→ Check implementation matches spec
5. /claude-learns.spec-verify [feature]  → Verify with evidence before claiming done
6. /claude-learns.learn                  → Capture insights
```

### Debugging an Issue

```
1. Understand symptom
2. Find relevant code
3. Trace call chain
4. Form hypothesis, verify with targeted reads
5. Fix with minimal, precise edits
6. Add test to prevent regression
7. Document gotcha if non-obvious
```

### Scientific Elimination Debugging

For complex bugs with multiple possible causes, use the elimination system:

```
1. /claude-learns.eliminate [symptom]     → Generate hypotheses
2. /claude-learns.eliminate-status        → Review current state
3. /claude-learns.hypothesis [new idea]   → Add hypothesis if needed
4. /claude-learns.evidence [H#] [result]  → Record evidence
5. /claude-learns.eliminate-status        → Check convergence
6. Repeat 3-5 until confirmed
7. Verify fix works
8. Run /claude-learns.learn to capture debugging insights
```

> "When you have eliminated the impossible, whatever remains, however improbable,
> must be the truth." — Sherlock Holmes

### Spec-Driven Debugging

For bugs in features with specifications:

```
1. /claude-learns.spec-debug [feature] [symptom]  → Load spec, compare to reality
2. Hypotheses generated from deviations (elevated confidence)
3. Evidence gathering continues via /claude-learns.eliminate
4. If spec deviation caused bug:
   - Fix implementation to match spec, OR
   - /claude-learns.spec-deviation if behavior change is intentional
5. Update debugging-lessons memory
```

### Refactoring

```
1. Map impact of changes
2. Plan approach (write to memory if complex)
3. Make incremental changes
4. Run full test suite
5. Update affected memories
```

---

## Completion Standards

### Verification Before Claiming Done

**IMPORTANT: YOU MUST run `/claude-learns.spec-verify` before claiming any implementation is complete.**

Requirements before saying "done":
1. Run `/claude-learns.spec-verify [feature]`
2. All acceptance criteria show ✅ PASS
3. Evidence is concrete (test output, screenshots, logs) not "I believe it works"

If ANY criterion fails:
- Do NOT claim completion
- Fix the issue
- Re-run `/claude-learns.spec-verify`
- Repeat until all pass

### Evidence Quality

**IMPORTANT:** Evidence must be concrete and verifiable, not assumptions.

**Good Evidence (Concrete)**:
```
✅ "Test output: PASS - 15 assertions, 0 failures"
✅ "curl -X POST /api/login returned 200 with token"
✅ "Error message 'Invalid credentials' displayed in .error-banner"
```

**Bad Evidence (Assumptions)**:
```
❌ "I believe this works"
❌ "Should be fine based on the implementation"
❌ "Tests would pass"
```

### When Corrected

If user says "this isn't working" after you claimed done:
1. Run `/claude-learns.spec-correction` immediately
2. Capture what was claimed vs reality
3. Identify what verification would have caught it
4. Fix the issue
5. Re-run `/claude-learns.spec-verify` with full evidence

### Correction Loop

```
Implement → /claude-learns.spec-verify (with evidence) → If user corrects → /claude-learns.spec-correction
                ↑                                                                          ↓
                └──────────────── Future /claude-learns.spec-verify checks corrections ←───┘
```

Corrections are stored in `.specify/memory/corrections.md` and checked during
future verifications to prevent repeating the same mistakes.

---

## Quick Reference

### Slash Commands

**Generic Commands:**
| Command | Purpose |
|---------|---------|
| `/go [task]` | Start task following best practices |
| `/explore [area]` | Systematically explore codebase area |
| `/debug [issue]` | Debug issue with structured approach |
| `/refactor [target]` | Safe refactoring workflow |

**Claude-Learns Commands** (template-specific):
| Command | Purpose |
|---------|---------|
| `/claude-learns.learn` | Trigger learning loop review |
| `/claude-learns.audit` | Audit CLAUDE.md and memories for staleness |
| `/claude-learns.skills` | Re-discover and update skills |
| `/claude-learns.install` | Install template into target project |
| `/claude-learns.update [tool]` | Update tools and template with git safety |
| `/claude-learns.eliminate [symptom]` | Start elimination-based debugging session |
| `/claude-learns.hypothesis [desc]` | Add hypothesis to active investigation |
| `/claude-learns.evidence [H#] [obs]` | Record evidence for hypothesis evaluation |
| `/claude-learns.eliminate-status` | View current investigation state |
| `/claude-learns.eliminate-history` | Search past debugging sessions |
| `/claude-learns.bisect` | Git bisect integration for commit-level elimination |
| `/claude-learns.spec-create [name]` | Create feature specification |
| `/claude-learns.spec-validate [name]` | Validate implementation against spec |
| `/claude-learns.spec-debug [name] [symptom]` | Debug using spec as source of truth |
| `/claude-learns.spec-deviation [name]` | Log intentional spec deviation |
| `/claude-learns.spec-list` | List all specifications |
| `/claude-learns.spec-verify [name]` | Verify with evidence before claiming done |
| `/claude-learns.spec-correction` | Capture correction when claim was wrong |

### Claude Code Commands

```bash
/mcp                    # Check MCP server status
/clear                  # Clear conversation context
/compact                # Compress context
```

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| Memory not found | Check `.serena/memories/` for file existence |
| MCP not connected | Run `/mcp` and verify server status |
| Context overflow | Clear and use memories to preserve state |

### Performance Issues

- **Large file reads**: Use targeted lookups instead
- **Too many results**: Narrow search with filters
- **Context overflow**: Clear and use memories to preserve state

---

## Skills Integration

### Active Skills

<!-- Claude: Populate after exploring available skills -->

#### Skill: [SKILL_NAME]
- **Purpose**: [What this skill does]
- **Use when**: [Specific scenarios]
- **Notes**: [Any project-specific configuration]

<!-- Add more skills as discovered -->

### Skill Discovery

To explore available skills:
> "Please explore available skills and update CLAUDE.md with relevant ones"

---

## Specification-Driven Development

This project uses Spec-Kit for specification-driven development, integrating
with the elimination debugging system.

### Core Concept

Define expected behavior in specifications before implementation. Specifications
serve as the source of truth for validation and debugging.

### Key Files

```
.specify/
├── config.yaml                    # Spec-kit settings
├── memory/
│   ├── constitution.md            # Non-negotiable project principles
│   └── corrections.md             # Premature completion claims log
├── specs/                         # Feature specifications
│   └── {feature}/spec.md
├── templates/                     # Spec templates
│   ├── feature-spec.md
│   ├── bug-fix-spec.md
│   └── refactor-spec.md
├── reports/                       # Verification/validation reports
└── deviations/                    # Intentional deviations from specs
```

### Spec Workflow

```
1. /claude-learns.spec-create [feature]     → Define expected behavior
2. Implement feature                        → Follow the spec
3. /claude-learns.spec-validate [feature]   → Verify implementation matches spec
4. If issues found:
   - Bug? → Fix implementation
   - Intentional? → /claude-learns.spec-deviation to document
5. /claude-learns.spec-debug [feature] [symptom] → Debug with spec context
```

### Integration with Elimination Debugging

When `/claude-learns.spec-debug` is used:
1. Loads the feature specification
2. Compares actual vs expected behavior
3. Generates hypotheses from spec deviations (confidence: 0.70)
4. User can run `/claude-learns.eliminate` after analysis for systematic debugging
5. Uses spec as evidence source

### When to Use Specs

| Scenario | Use |
|----------|-----|
| New feature implementation | `/claude-learns.spec-create` first |
| Debugging specced feature | `/claude-learns.spec-debug` |
| Validating implementation | `/claude-learns.spec-validate` |
| Intentional behavior change | `/claude-learns.spec-deviation` |
| Overview of all specs | `/claude-learns.spec-list` |

---

## Scientific Elimination Debugging System

This project includes a scientific process of elimination approach for debugging,
based on modus tollens logic and Bayesian confidence tracking.

### Core Principle

> "When you have eliminated the impossible, whatever remains, however improbable,
> must be the truth." — Sherlock Holmes

The system generates hypotheses, gathers discriminating evidence, updates confidence
scores via Bayesian reasoning, and eliminates falsified hypotheses until the root
cause is identified.

### Key Files

```
.elimination/
├── config.yaml                    # Thresholds and settings
├── active/                        # Current investigation
│   ├── session.yaml              # Session metadata
│   ├── hypotheses/               # Active hypotheses (YAML)
│   └── evidence/                 # Collected evidence (YAML)
├── logs/
│   └── elimination_log.yaml      # Elimination decisions
├── learned/
│   ├── heuristics.yaml           # Learned patterns
│   └── templates/                # Hypothesis templates
│       └── debugging.yaml        # Common debugging hypothesis templates
├── samples/                       # Example investigations for reference
└── archive/                      # Past investigations
```

### Confidence Thresholds

- **Confirmed**: > 0.90 (proceed to verification)
- **Active**: 0.25 - 0.90 (continue investigation)
- **Unlikely**: 0.05 - 0.25 (soft eliminated)
- **Eliminated**: < 0.05 (hard eliminated, can resurrect)

### When to Use Elimination

Use `/claude-learns.eliminate` instead of `/debug` when:
- Multiple possible causes exist and simple debugging isn't converging
- Initial debugging hasn't found the root cause
- Issue is intermittent or hard to reproduce
- You need structured tracking of hypotheses and evidence

---

## Changelog

<!-- Track CLAUDE.md evolution here -->
- **[DATE]**: Added Code Conventions section with specific guidelines per Anthropic best practices
- **[DATE]**: Added IMPORTANT markers to critical rules (token efficiency, verification, evidence)
- **[DATE]**: Added /update command for safe tool and template updates with git checkpoints
- **[DATE]**: Added comprehensive Serena MCP Tools Reference section
- **[DATE]**: Initial CLAUDE.md created from claude-learns template
<!-- Add entries as updates are made -->

---

*Last Updated: [DATE]*
*Template: claude-learns v1.0*
