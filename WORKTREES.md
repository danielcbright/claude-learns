# Git Worktrees with Claude-Learns

This guide covers how to effectively use claude-learns in projects that use Git worktrees for parallel development.

## Quick Reference

| Scenario | Strategy | Command |
|----------|----------|---------|
| New worktree, isolated memory | Copy `.serena/` to worktree | `/claude-learns.worktree-init --mode isolated` |
| New worktree, shared memory | Symlink `.serena/` | `/claude-learns.worktree-init --mode shared` |
| Speed up indexing | Copy cache only | `/claude-learns.worktree-init --cache-only` |
| Check worktree status | Verify configuration | `git worktree list` |

---

## Understanding the Challenge

Git worktrees allow checking out multiple branches into separate directories simultaneously. This creates unique considerations for claude-learns:

```
main-repo/                    # Main working tree
├── .serena/                  # Memory + cache
├── .claude/                  # Commands
├── .elimination/             # Debug sessions
└── .specify/                 # Specifications

../feature-worktree/          # Worktree for feature branch
├── .serena/                  # ??? (shared or isolated?)
├── .claude/                  # ??? (copied or symlinked?)
└── ...
```

### Key Questions

1. **Memory sharing**: Should worktrees share the same learned memories, or have isolated context?
2. **Cache sharing**: Should Serena's index cache be shared to avoid re-indexing?
3. **Session isolation**: Should elimination/spec sessions be per-worktree or shared?
4. **Command consistency**: Should commands be identical across worktrees?

---

## Recommended Strategies

### Strategy 1: Isolated Worktrees (Default)

**Best for**: Independent features, different team members, experiments

Each worktree has its own complete claude-learns installation:

```bash
# Create worktree
git worktree add ../feature-x feature/x

# Initialize claude-learns in worktree
cd ../feature-x
/claude-learns.worktree-init --mode isolated
```

**What gets copied**:
- `.serena/memories/` - Full copy (can diverge)
- `.serena/cache/` - Full copy (speeds up first indexing)
- `.claude/` - Full copy
- `.elimination/` - Empty state (fresh debug sessions)
- `.specify/` - Empty state (fresh specs)

**Pros**:
- Complete isolation - changes in one worktree don't affect others
- Safe for experiments and risky changes
- Different worktrees can learn different patterns

**Cons**:
- Learning doesn't propagate across worktrees
- More disk space
- Must manually sync valuable learnings back

---

### Strategy 2: Shared Memory (Recommended for Solo Work)

**Best for**: Solo developer with multiple active branches

Memory is symlinked, other directories are copied:

```bash
# Create worktree
git worktree add ../feature-x feature/x

# Initialize with shared memory
cd ../feature-x
/claude-learns.worktree-init --mode shared
```

**What happens**:
- `.serena/memories/` → Symlink to main repo's memories
- `.serena/cache/` - Copied (each worktree indexes independently)
- `.claude/` - Full copy
- `.elimination/` - Isolated (per-worktree sessions)
- `.specify/` - Isolated (per-worktree specs)

**Pros**:
- Learning in any worktree benefits all worktrees
- Consistent memory across parallel work
- Less cognitive overhead

**Cons**:
- Conflicting learnings can cause confusion
- Changes to memories affect all active sessions
- Must be careful with `write_memory()` during experiments

---

### Strategy 3: Cache-Only Sharing (Speed Optimization)

**Best for**: Large codebases where re-indexing is slow

Only the Serena cache is shared; everything else is isolated:

```bash
# Create worktree with cache sharing
cd ../feature-x
/claude-learns.worktree-init --cache-only
```

**What happens**:
- `.serena/cache/` → Symlink to main repo's cache
- Everything else - Isolated (full copies)

**Pros**:
- Fastest startup - no re-indexing needed
- Serena docs recommend this for large projects
- Minimal risk of cross-worktree interference

**Cons**:
- Cache may become stale if main repo's code changes significantly
- Symlinked cache means disk I/O goes to main repo location

---

## Directory Layout Recommendations

### Standard Multi-Worktree Setup

```
~/projects/
├── my-project/              # Main repo (origin checkout)
│   ├── .git/                # Full git repository
│   ├── .serena/             # Primary memory + cache
│   ├── .claude/             # Commands
│   └── ...
│
├── my-project-feature-a/    # Worktree for feature-a
│   ├── .git                 # File pointing to main .git
│   ├── .serena/             # Isolated or symlinked
│   └── ...
│
└── my-project-hotfix/       # Worktree for hotfix
    ├── .git                 # File pointing to main .git
    ├── .serena/             # Isolated or symlinked
    └── ...
```

### Naming Convention

Use consistent naming for worktrees:

```bash
# Pattern: {project}-{branch-type}-{short-name}
git worktree add ../my-project-feature-auth feature/authentication
git worktree add ../my-project-fix-login hotfix/login-bug
git worktree add ../my-project-experiment-perf experiment/performance
```

---

## Working with Serena in Worktrees

### Cache Considerations

Serena's cache stores the semantic index of your codebase. Key points:

1. **First-time indexing**: Can take several minutes for large projects
2. **Incremental updates**: Usually fast after initial index
3. **Cache location**: `.serena/cache/` by default

**Optimization**: Copy cache when creating worktrees:

```bash
# Manual cache copy
cp -r ../main-repo/.serena/cache .serena/cache

# Or use the init command
/claude-learns.worktree-init --cache-only
```

### Memory Sharing Caveats

When using shared memory (symlinks):

1. **Concurrent writes**: Multiple Claude Code sessions writing to the same memory can cause conflicts
2. **Context bleed**: Learnings from one feature may not apply to another
3. **Rollback complexity**: Hard to undo memory changes across worktrees

**Best practice**: Use shared memory only when working solo on related features.

---

## Common Workflows

### Workflow 1: Feature Development with Worktrees

```bash
# 1. Create worktree for new feature
git worktree add ../project-feature-x feature/x

# 2. Navigate and initialize
cd ../project-feature-x
/claude-learns.worktree-init --mode isolated

# 3. Work on feature with Claude Code
# (memories, specs, debug sessions are isolated)

# 4. Before merging, sync valuable learnings
/claude-learns.worktree-sync-memories  # Coming soon

# 5. After merge, clean up worktree
cd ../project
git worktree remove ../project-feature-x
```

### Workflow 2: Parallel Bug Investigation

```bash
# Investigating a bug that might be in multiple places
git worktree add ../project-debug-auth main
git worktree add ../project-debug-api main

# Each worktree can run independent /claude-learns.eliminate sessions
# without interfering with each other
```

### Workflow 3: Code Review with Fresh Context

```bash
# Create worktree for reviewing a PR
git worktree add ../project-review-pr123 origin/pr-branch

# Use isolated mode to avoid polluting main memories
cd ../project-review-pr123
/claude-learns.worktree-init --mode isolated

# Review with fresh perspective, then clean up
```

---

## Troubleshooting

### Problem: Serena shows outdated symbols

**Cause**: Stale cache from shared/copied cache
**Solution**: Rebuild cache

```bash
# Force cache rebuild
rm -rf .serena/cache
# Serena will re-index on next operation
```

### Problem: Memory conflicts in shared mode

**Cause**: Multiple sessions writing to same memory file
**Solution**: Either use isolated mode, or coordinate sessions

```bash
# Check which worktrees are active
git worktree list

# Consider switching to isolated mode if conflicts persist
rm .serena/memories  # Remove symlink
cp -r ../main-repo/.serena/memories .serena/memories
```

### Problem: Commands behave differently across worktrees

**Cause**: Commands were modified in one worktree but not synced
**Solution**: Re-run `/claude-learns.update` in affected worktrees

### Problem: Can't find worktree's memory history

**Cause**: Using isolated mode - memories are worktree-local
**Solution**: Check the worktree's own `.serena/memories/` or sync from main

---

## Integration with Other Tools

### Git Operations

```bash
# List all worktrees
git worktree list

# Remove a worktree (keeps branch)
git worktree remove ../project-feature-x

# Prune stale worktree references
git worktree prune
```

### Claude Code Sessions

Each worktree should have its own Claude Code session. Don't share sessions across worktrees as this can cause:
- Path confusion
- Context bleed
- File modification conflicts

### Serena MCP

When running Serena in a worktree:
- Ensure `.serena/project.yml` exists in the worktree
- Verify Serena is pointing to the correct root
- Check that cache is populated for the worktree's code state

---

## Best Practices Summary

1. **Start with isolated mode** until you understand your workflow
2. **Share cache for speed** on large codebases
3. **Share memory for consistency** only in solo workflows
4. **Keep debug sessions isolated** - they reference specific code states
5. **Name worktrees consistently** - include branch type and short name
6. **Clean up worktrees promptly** - stale worktrees cause confusion
7. **Sync valuable learnings** back to main before removing worktrees
8. **One Claude Code session per worktree** - never share sessions

---

## See Also

- [Serena Additional Usage - Worktrees](https://oraios.github.io/serena/02-usage/999_additional-usage.html)
- [Claude Code Common Workflows](https://code.claude.com/docs/en/common-workflows)
- [Git Worktree Documentation](https://git-scm.com/docs/git-worktree)

---

*Last Updated: 2026-01-23*
