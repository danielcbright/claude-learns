# Frequently Asked Questions

---

## Getting Started

### Do I need all these systems?

**No.** Start with just the basics:

| System | Required? | When to add |
|--------|-----------|-------------|
| `.claude/` + `CLAUDE.md` | **Yes** | Always needed |
| `.serena/memories/` | **Yes** | Core memory system |
| `.elimination/` | No | When you have complex, multi-cause bugs |
| `.specify/` | No | When you want spec-driven development |

You can always add `.elimination/` and `.specify/` later.

### What's the minimum setup?

```bash
cp -r template/.claude your-project/
cp -r template/.serena your-project/
cp template/CLAUDE.md your-project/
```

Then edit `CLAUDE.md` with your project name and language.

### Does this work with any language/framework?

**Yes.** The template is language-agnostic. It works with:
- Any programming language
- Any framework
- Monorepos and single-project repos
- Frontend, backend, CLI tools, libraries

Customize `CLAUDE.md` to document your specific patterns.

### Can I use this without MCP servers?

**Yes, with reduced functionality:**

| Feature | Without MCP | With Serena MCP |
|---------|-------------|-----------------|
| Slash commands | Works | Works |
| Memory storage | Works (file-based) | Works (enhanced) |
| Symbol lookup | Manual file reads | Targeted lookups |
| Learning loop | Works | Works |

The core value works without MCPs. Serena MCP adds precise code navigation.

---

## Commands

### What's the difference between `/debug` and `/eliminate`?

| Aspect | `/debug` | `/eliminate` |
|--------|----------|--------------|
| Best for | Single likely cause | Multiple possible causes |
| Approach | Linear investigation | Parallel hypothesis testing |
| Tracking | Ad-hoc | Structured YAML files |
| When stuck | Switch to `/eliminate` | Keep gathering evidence |

**Use `/debug`** for straightforward bugs.
**Use `/eliminate`** when you've been stuck, the bug is intermittent, or multiple subsystems could be responsible.

### When should I use `/spec-create`?

Use `/spec-create` when:
- Starting a new feature with clear requirements
- You want to define "done" before starting
- Multiple people need to agree on expected behavior
- You'll need to validate the implementation later

Skip it for:
- Quick fixes
- Exploratory work
- Refactoring (existing behavior is the spec)

### How do I undo a Claude action?

Claude Code doesn't have built-in undo, but:

1. **Git**: If you committed before, `git checkout -- <file>` or `git reset`
2. **Editor**: Use your IDE's local history
3. **Memories**: Delete unwanted memories with `delete_memory("name")`

For updates specifically, use `/update --rollback`.

### What does `/learn` actually do?

`/learn` triggers Claude to:
1. Review insights from the current session
2. Propose updates to memories or CLAUDE.md
3. Wait for your approval before writing anything

It's a checkpoint to capture knowledge before it's lost.

---

## Memory System

### Where is data stored?

```
your-project/
├── .serena/memories/           # Persistent knowledge
│   ├── debugging-lessons.md    # Past bugs and fixes
│   ├── decision-log.md         # Architectural decisions
│   └── ...
├── .elimination/               # Debugging sessions
│   ├── active/                 # Current investigation
│   └── archive/                # Past investigations
└── .specify/                   # Specifications
    ├── specs/                  # Feature specs
    └── memory/                 # Spec-specific knowledge
```

All data stays in your project directory.

### How do I back up memories?

Memories are plain text files. Back them up with git:

```bash
git add .serena/memories/
git commit -m "Backup memories"
```

Or copy the folder anywhere you store backups.

### Can I edit memories manually?

**Yes.** Memories are Markdown files. Edit them in any text editor.

However, if Serena MCP is connected, prefer using:
- `edit_memory("name", needle, repl, mode)` for small changes
- `write_memory("name", content)` to overwrite

This ensures Claude stays in sync.

### How do I see what memories exist?

```
# With Serena MCP
list_memories()

# Without MCP
ls .serena/memories/
```

### Do memories persist after `/clear`?

**Yes.** `/clear` only clears the conversation context. Memories are stored in files and survive across sessions.

This is why you should run `/learn` before `/clear` to save important insights.

---

## Troubleshooting

### Commands not working

1. **Check file location**: `.claude/commands/` must be in your project root
2. **Verify file names**: Commands must match the pattern `<command>.md`
3. **Restart Claude Code**: Sometimes a restart is needed after adding commands

### MCP not connected

Run `/mcp` in Claude Code to see status.

If Serena isn't connected:
```bash
# Add Serena to Claude Code
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)
```

### Claude keeps re-reading the same files

This usually means memories aren't being used effectively:

1. Run `/learn` to save context that's being re-discovered
2. Check that `CLAUDE.md` has accurate entry points documented
3. Verify Serena MCP is connected for symbol-based navigation

### How do I uninstall completely?

```bash
# Remove all claude-learns files
rm -rf .claude .serena .elimination .specify CLAUDE.md

# If you committed changes
git checkout -- CLAUDE.md
git clean -fd .claude .serena .elimination .specify
```

### Can I use claude-learns in a monorepo?

**Yes.** You have two options:

1. **Single setup at root**: One `CLAUDE.md` covering all packages
2. **Per-package setup**: Copy the template into each package that needs it

For monorepos, document package-specific patterns in memories.

---

## Best Practices

### How often should I run `/learn`?

- **After discovering something non-obvious** about the codebase
- **Before `/clear`** to preserve important context
- **After completing a complex task** that taught you something
- **At the end of a session** as a general checkpoint

### Should I commit memories to git?

**Recommended yes** for:
- Team projects (shared knowledge)
- Projects you'll return to later
- Anything you don't want to lose

**Optional** for:
- Solo experiments
- Temporary projects

Add to `.gitignore` if you prefer not to commit:
```
.serena/memories/
.elimination/archive/
```

### How do I keep memories from getting stale?

Run `/audit` periodically. It checks:
- CLAUDE.md accuracy
- Memory relevance
- Outdated information

Review and update memories when your project evolves significantly.

---

## Performance

### Does this slow down Claude Code?

**Minimal impact.** The systems add:
- ~100ms for memory lookups (cached after first read)
- ~50ms for command loading
- Negligible overhead for file operations

Benefits outweigh costs for projects worked on for more than a week.

### What's the memory/storage footprint?

Typical usage:
- `.serena/memories/`: 50KB - 500KB (plain text)
- `.elimination/`: 10KB - 100KB per active investigation
- `.specify/`: 20KB - 200KB for specs and deviations

All stored as readable Markdown/YAML files.

### Can I exclude files from backups/version control?

Yes, add to `.gitignore`:
```
.serena/memories/auto-generated/
.elimination/archive/
```

Keep important memories committed for team sharing.

---

## Customization

### Can I modify the commands?

**Yes.** Edit `.claude/commands/*.md` files:
- Change command behavior by editing the Markdown
- Add new commands by creating new `.md` files
- Remove unwanted commands by deleting files

Restart Claude Code after changes.

### How do I customize for my team's workflow?

1. **Edit CLAUDE.md** with team-specific patterns
2. **Create team memories** for shared knowledge
3. **Customize commands** for your processes
4. **Set up project constitution** in `.specify/memory/constitution.md`

### Can I integrate with CI/CD?

**Partially.** Some workflows can be scripted:

```bash
# Validate specs exist for features
ls .specify/specs/

# Check for unresolved elimination sessions
ls .elimination/active/
```

Full automation requires Claude Code CLI integration, which is evolving.

### Does this work in other editors/IDEs?

**Claude Code specific**, but concepts apply to:
- VS Code + Claude extension
- Cursor (similar MCP architecture)
- Other AI-assisted editors

The template structure could be adapted for other tools.

---

## Still have questions?

- Check [EXAMPLES.md](EXAMPLES.md) for concrete usage scenarios
- Read the full [README.md](README.md) for detailed documentation
- Open an issue at [github.com/danielcbright/claude-learns](https://github.com/danielcbright/claude-learns/issues)
