# Quick Start (5 minutes)

Get Claude Code to remember your project and improve over time.

---

## What You'll Get

A self-learning Claude Code setup that:
- Remembers project context across sessions
- Uses structured workflows for common tasks
- Learns from your codebase and saves insights

---

## Install (2 minutes)

### Option 1: Copy Manually

```bash
# Clone the template
git clone https://github.com/danielcbright/claude-learns.git

# Copy to your project
cp -r claude-learns/template/.claude /path/to/your/project/
cp -r claude-learns/template/.serena /path/to/your/project/
cp claude-learns/template/CLAUDE.md /path/to/your/project/
```

### Option 2: Let Claude Do It

In your target project, tell Claude:

> "Install the claude-learns template from https://github.com/danielcbright/claude-learns"

Claude will read `INSTALL.md` and handle the rest.

---

## Customize (1 minute)

Edit `CLAUDE.md` in your project:

```markdown
## Project Overview
- **Project Name**: My Awesome App     # <-- Change this
- **Type**: Web App                    # <-- Change this
- **Primary Languages**: TypeScript    # <-- Change this
- **Key Frameworks**: React, Express   # <-- Change this
```

That's all you need to start.

---

## Did It Work? (Quick Check)

After setup, try these commands:

```
/mcp                           # Should show MCP server status
/go hello world               # Should respond with a plan
/claude-learns.learn                        # Should offer to save session insights
```

**Expected output:**
- `/mcp`: Shows connected servers or "No MCP servers configured" (both are normal)
- `/go`: Claude should acknowledge and start working on the task
- `/claude-learns.learn`: Should review the session and offer memory updates

**Pro tip**: Run `/claude-learns.learn` after your first few tasks to build up project knowledge for future sessions.

If commands aren't recognized, check that `.claude/commands/` was copied correctly.

---

## First Workflow (2 minutes)

Try a simple task:

```
/go fix the typo in README
```

Claude will:
1. Check for relevant memories
2. Find the typo
3. Fix it
4. Offer to save any insights

---

## Core Commands

| Command | What it does |
|---------|-------------|
| `/go [task]` | Start any task with best practices |
| `/debug [issue]` | Systematic debugging |
| `/explore [area]` | Understand code you're unfamiliar with |
| `/claude-learns.learn` | Save insights from current session |

---

## What to Try First

**For new projects:**
```
/go set up the basic project structure
/go add error handling patterns
```

**For existing projects:**
```
/explore the main application flow
/go document the API endpoints
```

**For debugging:**
```
/debug why the tests are failing
/claude-learns.eliminate intermittent login failures
```

---

## Optional: Add More Systems

When you need them, enable additional capabilities:

```bash
# Scientific elimination debugging (for complex bugs)
cp -r claude-learns/template/.elimination /path/to/your/project/

# Specification-driven development (for feature planning)
cp -r claude-learns/template/.specify /path/to/your/project/
```

---

## Next Steps

| Want to... | Read |
|------------|------|
| Understand the architecture | [README.md](README.md#architecture) |
| See real-world examples | [EXAMPLES.md](EXAMPLES.md) |
| Get answers to common questions | [FAQ.md](FAQ.md) |
| Learn all available commands | [README.md](README.md#available-slash-commands) |

---

## Troubleshooting

**Commands not recognized?**
Make sure `.claude/commands/` was copied to your project root.

**Claude not reading memories?**
Run `/mcp` to check if Serena MCP is connected. If not, memories still work but with limited functionality.

**Need to uninstall?**
```bash
rm -rf .claude .serena .elimination .specify CLAUDE.md
```

---

*That's it! Start with `/go` and let Claude learn your project.*
