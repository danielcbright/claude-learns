# claude-learns

A template for creating self-learning Claude Code projects with persistent memory and context management.

---

## What is claude-learns?

claude-learns helps Claude Code remember context across sessions and continuously improve its understanding of your codebase. It provides:

- **Persistent Memory**: Store and retrieve project knowledge across sessions
- **Self-Learning System**: Claude identifies patterns and insights, then offers to save them
- **Slash Commands**: Pre-built workflows for common development tasks
- **MCP Integration Ready**: Works with Serena, Context7, and other MCP servers

## Quick Start

### For Users

1. Clone this template:
   ```bash
   git clone https://github.com/danielcbright/claude-learns.git
   cd claude-learns
   ```

2. Copy to your project:
   ```bash
   cp -r .claude /path/to/your/project/
   cp -r .serena /path/to/your/project/
   cp CLAUDE.md /path/to/your/project/
   ```

3. Customize `CLAUDE.md` with your project details

### For AI Agents (Claude Code)

> **If you're Claude Code** and a user wants to install this template:

1. **Read `INSTALL.md`** - Contains step-by-step installation instructions
2. **Key files to copy**: `.claude/`, `.serena/`, `CLAUDE.md`
3. **Customize placeholders**: Replace `[PROJECT_NAME]`, `[PRIMARY_LANGUAGE]`, etc.
4. **Don't copy**: `README.md`, `INSTALL.md`, `.git/`

---

## What's Included

```
claude-learns/
├── CLAUDE.md                    # Main config (customize per project)
├── INSTALL.md                   # AI agent installation guide
├── README.md                    # This file
├── .claude/
│   ├── settings.local.json      # Local permissions
│   └── commands/                # Slash commands
│       ├── install.md           # /install - Install template
│       ├── go.md                # /go [task] - Start with best practices
│       ├── explore.md           # /explore [area] - Explore codebase
│       ├── debug.md             # /debug [issue] - Systematic debugging
│       ├── refactor.md          # /refactor [target] - Safe refactoring
│       ├── learn.md             # /learn - Learning loop review
│       ├── audit.md             # /audit - Documentation audit
│       └── skills.md            # /skills - Discover skills
└── .serena/
    └── memories/
        └── claude_code_patterns.md  # Session quick reference
```

## Available Slash Commands

| Command | Purpose |
|---------|---------|
| `/install` | Install this template to a target project |
| `/go [task]` | Start task following best practices |
| `/explore [area]` | Systematically explore codebase area |
| `/debug [issue]` | Debug issue with structured approach |
| `/refactor [target]` | Safe refactoring workflow |
| `/learn` | Trigger learning loop review |
| `/audit` | Audit documentation for staleness |
| `/skills` | Re-discover and update skills |

## Learning Loop System

The template includes a continuous improvement system:

1. **During work**: Claude identifies patterns, gotchas, insights
2. **At breakpoints**: Claude offers structured recommendations
3. **On approval**: Updates are written to memories and CLAUDE.md

This creates an ever-improving knowledge base for your project.

## MCP Integration

claude-learns works well with these MCP servers:

- **Serena**: Code navigation and symbol lookup
- **Context7**: External library documentation
- **Sequential Thinking**: Complex architectural decisions

Configure MCP servers in your Claude Code settings as needed.

## Customization

### CLAUDE.md

Edit these sections for your project:

1. **Project Overview** - Fill in project details
2. **Key Entry Points** - Document commonly searched symbols
3. **Current Memories** - Update after creating memories
4. **Project-Specific Patterns** - Document coding conventions
5. **Active Skills** - Add relevant skills

### Memories

Edit `.serena/memories/claude_code_patterns.md`:

1. Update test/lint/build commands
2. Add project-specific gotchas
3. Document your architecture

## Requirements

- Claude Code CLI

## License

MIT - Use freely in your projects.
