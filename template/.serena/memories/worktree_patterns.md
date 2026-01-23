---
type: serena-memory
name: worktree_patterns
purpose: Git worktree patterns and best practices for parallel development
read_at: when-using-worktrees
customize: true
---

# Git Worktree Patterns

> This memory contains patterns for working with git worktrees and claude-learns.
> Read this when initializing worktrees or troubleshooting worktree-related issues.

## Quick Reference

### Worktree Commands

```bash
# Create a new worktree
git worktree add ../project-feature-x feature/x

# List all worktrees
git worktree list

# Remove a worktree (keeps branch)
git worktree remove ../project-feature-x

# Prune stale worktree references
git worktree prune
```

### Claude-Learns Worktree Initialization

```bash
# In a worktree directory:
/claude-learns.worktree-init --mode isolated   # Independent memory
/claude-learns.worktree-init --mode shared     # Symlinked memory
/claude-learns.worktree-init --cache-only      # Fastest for large repos
```

## Mode Selection Guide

| Scenario | Recommended Mode | Reason |
|----------|------------------|--------|
| Independent feature development | `isolated` | Changes don't affect other work |
| Solo dev, multiple related branches | `shared` | Learning propagates everywhere |
| Large codebase (>100k LOC) | `cache-only` | Avoid re-indexing overhead |
| Experimental/risky changes | `isolated` | Safe to mess up |
| Code review of someone's PR | `isolated` | Fresh perspective, no pollution |
| Hotfix while feature in progress | `isolated` | Clean separation |

## Directory Layout

### Recommended Naming

```
~/projects/
├── my-project/              # Main repo
├── my-project-feature-auth/ # Feature worktree
├── my-project-fix-login/    # Hotfix worktree
└── my-project-review-pr42/  # Review worktree
```

### Pattern: `{project}-{type}-{short-name}`

Types: `feature`, `fix`, `review`, `experiment`, `release`

## Serena + Worktree Integration

### Cache Sharing (from Serena docs)

Serena recommends copying `.serena/cache` to worktrees to avoid re-indexing:

```bash
# Copy cache to new worktree
cp -r main-repo/.serena/cache worktree/.serena/cache
```

This is what `--cache-only` mode does automatically.

### Memory Sharing Caveats

When using `--mode shared`:
- `.serena/memories/` is symlinked to main repo
- Multiple sessions writing to same memory can conflict
- Use only for solo work or with coordination

### Rebuilding Stale Cache

If Serena shows outdated symbols:

```bash
rm -rf .serena/cache
# Serena will re-index on next operation
```

## Common Workflows

### Workflow 1: Feature Development

```bash
# 1. Create worktree
git worktree add ../project-feat-auth feature/authentication

# 2. Initialize claude-learns
cd ../project-feat-auth
/claude-learns.worktree-init --mode isolated

# 3. Work on feature...

# 4. Before merging, sync valuable learnings
# (Manual: copy insights from worktree memories to main)

# 5. Clean up
cd ../project
git worktree remove ../project-feat-auth
```

### Workflow 2: Parallel Investigation

```bash
# Create multiple worktrees to investigate different hypotheses
git worktree add ../project-debug-auth main
git worktree add ../project-debug-api main

# Each can run independent /claude-learns.eliminate sessions
```

### Workflow 3: PR Review

```bash
# Create worktree for reviewing
git worktree add ../project-review-pr123 origin/pr-123-branch

# Initialize with isolation (don't pollute main memories)
cd ../project-review-pr123
/claude-learns.worktree-init --mode isolated

# Review with fresh context, then clean up
```

## Troubleshooting Checklist

### Serena Not Working in Worktree

1. Check `.serena/project.yml` exists
2. Verify Serena MCP is pointing to worktree root
3. Rebuild cache if stale: `rm -rf .serena/cache`

### Memory Conflicts

1. Check if using shared mode: `cat .worktree-config`
2. Ensure only one session writes at a time
3. Consider switching to isolated mode

### Commands Behave Differently

1. Check `.claude/commands/` is populated
2. Re-run `/claude-learns.worktree-init` if needed
3. Run `/claude-learns.update` to sync

### Lost Learnings After Worktree Removal

1. If using isolated mode, learnings are in worktree's `.serena/memories/`
2. Before removal, copy valuable patterns to main repo
3. Consider `--mode shared` for future worktrees

## Safety Rules

1. **One Claude Code session per worktree** - Never share sessions
2. **Check branch before commits** - `git branch --show-current`
3. **Verify worktree path** - `pwd` before destructive operations
4. **Sync before cleanup** - Copy valuable learnings to main

## Related Memories

- `claude_code_patterns` - General Claude Code patterns
- `decision-log` - Architectural decisions (may be shared across worktrees)
- `debugging-lessons` - Past bugs (consider syncing across worktrees)

## External Resources

- [Serena Worktree Docs](https://oraios.github.io/serena/02-usage/999_additional-usage.html)
- [Claude Code Workflows](https://code.claude.com/docs/en/common-workflows)
- [Git Worktree Manual](https://git-scm.com/docs/git-worktree)
