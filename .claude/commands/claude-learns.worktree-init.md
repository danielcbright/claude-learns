# Initialize Worktree for Claude-Learns

Initialize a git worktree with claude-learns configuration. This command sets up memory, cache, and session directories appropriately based on the chosen mode.

## Usage

```
/claude-learns.worktree-init [--mode <mode>] [--cache-only] [--main-repo <path>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--mode` | Memory sharing mode: `isolated`, `shared` | `isolated` |
| `--cache-only` | Only share Serena cache (fastest startup) | false |
| `--main-repo` | Path to main repository | Auto-detected |

## Instructions

You are initializing claude-learns in a Git worktree.

### Step 1: Detect Worktree Context

First, verify we're in a worktree and find the main repository:

```bash
# Check if in a worktree
git rev-parse --is-inside-work-tree

# Get the main repository path (where .git directory lives)
git worktree list --porcelain | head -1 | sed 's/worktree //'

# Get current worktree info
pwd
git branch --show-current
```

**If not in a worktree**, inform the user:

```
This directory is not a git worktree.

To create a worktree:
  git worktree add ../[name] [branch]

To run this in the main repository, use /claude-learns.install instead.
```

### Step 2: Verify Main Repo Has Claude-Learns

Check that the main repository has claude-learns installed:

```bash
# Check for required directories in main repo
ls -la [main-repo]/.serena/
ls -la [main-repo]/.claude/
ls -la [main-repo]/.elimination/
ls -la [main-repo]/.specify/
```

**If main repo doesn't have claude-learns**:

```
The main repository doesn't appear to have claude-learns installed.

Please run in the main repository first:
  cd [main-repo]
  /claude-learns.install

Then return here and run /claude-learns.worktree-init again.
```

### Step 3: Determine Mode

Ask user to confirm mode if not specified:

```
## Worktree Initialization Mode

Current worktree: [current-path]
Main repository: [main-repo-path]
Branch: [branch-name]

Choose a mode:

1. **isolated** (recommended for independent work)
   - Memory: Copied (changes stay in this worktree)
   - Cache: Copied (fast, no shared state)
   - Sessions: Fresh (new elimination/spec sessions)

2. **shared** (recommended for solo work on related features)
   - Memory: Symlinked (learning benefits all worktrees)
   - Cache: Copied (each worktree indexes independently)
   - Sessions: Fresh (per-worktree debug/spec sessions)

3. **cache-only** (fastest for large codebases)
   - Memory: Copied (isolated learning)
   - Cache: Symlinked (instant Serena startup)
   - Sessions: Fresh (per-worktree sessions)

Enter choice (1/2/3) or mode name:
```

### Step 4: Execute Initialization

Based on the chosen mode, execute the appropriate setup:

#### Mode: isolated (default)

```bash
# Copy all directories
cp -r [main-repo]/.serena/ .serena/
cp -r [main-repo]/.claude/ .claude/
cp -r [main-repo]/.elimination/ .elimination/
cp -r [main-repo]/.specify/ .specify/

# Copy CLAUDE.md if it exists
cp [main-repo]/CLAUDE.md ./CLAUDE.md 2>/dev/null || true

# Copy WORKTREES.md if it exists
cp [main-repo]/WORKTREES.md ./WORKTREES.md 2>/dev/null || true

# Clear active sessions (start fresh)
rm -rf .elimination/active/*
rm -rf .specify/reports/*
```

#### Mode: shared

```bash
# Symlink memories, copy everything else
mkdir -p .serena
ln -s [main-repo]/.serena/memories .serena/memories
cp -r [main-repo]/.serena/cache .serena/cache 2>/dev/null || mkdir -p .serena/cache
cp [main-repo]/.serena/project.yml .serena/project.yml 2>/dev/null || true

# Copy commands (don't symlink - allows worktree-specific customization)
cp -r [main-repo]/.claude/ .claude/

# Copy elimination and specify (fresh sessions)
cp -r [main-repo]/.elimination/ .elimination/
cp -r [main-repo]/.specify/ .specify/

# Clear active sessions
rm -rf .elimination/active/*
rm -rf .specify/reports/*

# Copy docs
cp [main-repo]/CLAUDE.md ./CLAUDE.md 2>/dev/null || true
cp [main-repo]/WORKTREES.md ./WORKTREES.md 2>/dev/null || true
```

#### Mode: cache-only

```bash
# Copy memories (isolated)
cp -r [main-repo]/.serena/ .serena/

# Replace cache with symlink
rm -rf .serena/cache
ln -s [main-repo]/.serena/cache .serena/cache

# Copy everything else (isolated)
cp -r [main-repo]/.claude/ .claude/
cp -r [main-repo]/.elimination/ .elimination/
cp -r [main-repo]/.specify/ .specify/

# Clear active sessions
rm -rf .elimination/active/*
rm -rf .specify/reports/*

# Copy docs
cp [main-repo]/CLAUDE.md ./CLAUDE.md 2>/dev/null || true
cp [main-repo]/WORKTREES.md ./WORKTREES.md 2>/dev/null || true
```

### Step 5: Update Configuration

Update worktree-specific configuration:

```bash
# Update .serena/project.yml to point to this worktree
# (Only if not symlinked)
```

Create a `.worktree-config` file to track initialization:

```yaml
# .worktree-config - Created by /claude-learns.worktree-init
initialized: [ISO-DATE]
mode: [mode]
main_repo: [main-repo-path]
branch: [branch-name]
serena_memory: [copied|symlinked]
serena_cache: [copied|symlinked]
```

### Step 6: Verification

Verify the initialization:

```
## Worktree Initialization Complete

### Configuration
- Mode: [mode]
- Main repo: [main-repo]
- Branch: [branch]

### Directory Status
| Directory | Status | Type |
|-----------|--------|------|
| .serena/memories | ✅ | [copied/symlinked] |
| .serena/cache | ✅ | [copied/symlinked] |
| .claude/commands | ✅ | copied |
| .elimination | ✅ | copied (fresh) |
| .specify | ✅ | copied (fresh) |

### Serena Status
[Check if Serena can access this worktree]

### Recommendations

**For this worktree:**
- Start a fresh Claude Code session (don't share with main repo)
- Run `/mcp` to verify Serena connectivity
- Check `git worktree list` to see all active worktrees

**Memory handling:**
[If isolated]: Learnings in this worktree stay here. Sync valuable insights to main repo manually.
[If shared]: Learnings affect all worktrees. Be careful with experimental patterns.
[If cache-only]: Cache is shared but memories are isolated. Best for large codebases.

### Quick Commands
- `/claude-learns.go [task]` - Start working
- `git worktree list` - See all worktrees
- `git worktree remove [path]` - Clean up when done
```

## Troubleshooting

### "Serena cache out of date"

If Serena shows stale symbols after initialization:

```bash
# Remove and let Serena re-index
rm -rf .serena/cache
# Serena will rebuild on next operation
```

### "Memory conflicts in shared mode"

Multiple Claude Code sessions writing to shared memory can cause conflicts:

```bash
# Option 1: Switch to isolated mode
rm .serena/memories  # Remove symlink
cp -r [main-repo]/.serena/memories .serena/memories

# Option 2: Coordinate sessions (only one writes at a time)
```

### "Permission denied on symlinks"

Some environments don't support symlinks well:

```bash
# Fall back to copying
rm .serena/memories  # or .serena/cache
cp -r [main-repo]/.serena/memories .serena/memories
```

## See Also

- `WORKTREES.md` - Full worktree guidance
- `/claude-learns.install` - Install template in main repository
- Git worktree documentation: https://git-scm.com/docs/git-worktree
