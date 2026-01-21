# /claude-learns.update - Update Tools and Template

Update claude-learns template and associated tools (Serena, Context7, etc.) safely with git checkpoints and rollback capability.

## Syntax

```
/claude-learns.update                     Check all tools for updates (dry run)
/claude-learns.update --list              List registered tools and their status
/claude-learns.update [tool-name]         Update specific tool (e.g., serena, context7, claude-learns)
/claude-learns.update --all               Update all registered tools
/claude-learns.update --rollback          Rollback to last checkpoint
```

## Arguments

- `$ARGUMENTS` - Tool name or flag

---

## CRITICAL: Git Safety Protocol

**MANDATORY before ANY update operation:**

### Step 1: Check Working Directory

```bash
git status --porcelain
```

**If output is NOT empty (uncommitted changes exist):**

```
## Uncommitted Changes Detected

Before updating, you must save your current work:

Option 1 - Commit changes:
  git add -A && git commit -m "save work before update"

Option 2 - Stash changes:
  git stash

Then run /claude-learns.update again.
```

**STOP - Do not proceed with update until working directory is clean.**

### Step 2: Create Checkpoint Commit

```bash
# Stage everything
git add -A

# Create checkpoint commit
git commit -m "checkpoint: before update - $(date +%Y-%m-%d-%H%M)" --allow-empty

# Record the checkpoint SHA
git rev-parse HEAD > .claude/update-checkpoint.txt
```

Display to user:
```
## Git Checkpoint Created

Commit: [SHA]
Message: checkpoint: before update - [date]

If anything goes wrong, rollback with:
  /claude-learns.update --rollback
```

### Step 3: Proceed with Update

Only after checkpoint is confirmed, proceed to update phase.

---

## Phase 1: Load Tool Registry

Read the tool registry:

```yaml
# .claude/update-registry.yaml
```

If registry doesn't exist, create it with defaults (see "Initialize Registry" section below).

---

## Phase 2: Handle Command Arguments

### If `--list`:

Display all registered tools:

```
## Registered Tools

| Tool | Type | Source | Installed |
|------|------|--------|-----------|
| claude-learns | template | github.com/danielcbright/claude-learns | 1.0.0 |
| serena | mcp-server | github.com/oraios/serena | (check /mcp) |
| context7 | mcp-server | context7.dev | (check /mcp) |
```

### If `--rollback`:

See "Rollback" section below.

### If `--all`:

Process all tools in registry.

### If `[tool-name]`:

Process only the specified tool.

### If no arguments:

Dry run - check for updates but don't apply.

---

## Phase 3: For Each Tool - Fetch Latest Instructions

**CRITICAL: Always fetch from web - never hardcode update steps.**

### For claude-learns template:

```
WebFetch: https://raw.githubusercontent.com/danielcbright/claude-learns/main/UPDATE.md

Look for:
- Version information
- Changelog since installed version
- Breaking changes
- Update instructions
```

### For MCP servers (Serena, Context7, etc.):

```
WebFetch: {tool.docs_url from registry}

Look for:
- "## Installation" or "## Update" sections
- Version information
- Install/claude-learns.update commands
```

Display to user:

```
## Update Available: [tool-name]

Current: [installed_version]
Latest: [latest_version from web]

From official documentation:
> [paste relevant update instructions from fetched docs]

Proceed with update? (yes/no)
```

---

## Phase 4: Execute Update

### For claude-learns template:

1. **Fetch and parse manifest**:
   ```
   WebFetch: https://raw.githubusercontent.com/danielcbright/claude-learns/main/template/manifest.yaml
   ```

   The manifest contains:
   - `version`: Latest template version
   - `files.always_update`: Files that are always replaced
   - `files.updateable`: Files with conflict detection
   - `files.merge_only`: Config files (add new keys, preserve values)
   - `files.protected`: Paths that are NEVER touched
   - `original_checksums`: Checksums for conflict detection

2. **Process each file category**:

   **ALWAYS UPDATE** (from `files.always_update`):
   - Fetch and replace without asking
   - Currently: `.claude/commands/claude-learns.update.md`

   **UPDATEABLE** (from `files.updateable`):
   For each file:
   ```
   1. Calculate local file SHA256 checksum
   2. Compare to manifest checksum:
      - If match: File is up-to-date, skip
      - If differs: Check for user modifications
   3. If local != manifest checksum:
      - Compare local to original_checksums[path]
      - If local == original: User hasn't modified, safe to update
      - If local != original: CONFLICT - ask user (see below)
   ```

   **MERGE ONLY** (from `files.merge_only`):
   - Fetch latest version
   - Parse YAML: add new keys from remote, preserve existing local values
   - Write merged result

   **PROTECTED** (from `files.protected`):
   - NEVER modify these paths
   - Log when encountered for transparency:
     - `.serena/memories/*` - User's learned knowledge
     - `.specify/specs/*` - User's specifications
     - `.specify/memory/constitution.md` - User's project rules
     - `.specify/memory/corrections.md` - User's correction history
     - `.elimination/active/*` - Active debugging session
     - `.elimination/archive/*` - Historical debugging data

3. **Conflict handling**:

   When user has modified an updateable file (local != original AND local != latest):
   ```
   Conflict detected: [filename]
   You have local modifications.

   Local checksum:    [sha256:abc...]
   Original checksum: [sha256:def...]
   Latest checksum:   [sha256:ghi...]

   Options:
   1. Keep local (skip update for this file)
   2. Take update (backup local to .claude-learns-backup/)
   3. View diff

   Choice:
   ```

   If user chooses "Take update":
   - Create `.claude-learns-backup/` if needed
   - Copy local file to `.claude-learns-backup/[path]`
   - Then fetch and apply update

4. **Apply updates**:
   ```
   For each file to update:
     WebFetch: {manifest.base_url}/{path}
     Write to local path
   ```

### For MCP servers:

1. **Remove current installation**:
   ```bash
   claude mcp remove [server-name]
   ```

2. **Install latest** (using command from fetched docs):
   ```bash
   [install command from documentation]
   ```

3. **Verify**:
   ```bash
   # Check MCP status
   /mcp
   ```

---

## Phase 5: Update Registry

After successful update:

```yaml
# Update .claude/update-registry.yaml
tools:
  [tool-name]:
    installed_version: "[new version]"
    installed_date: "[today's date]"
    last_update: "[today's date]"
```

---

## Phase 6: Post-Update Summary

```
## Update Complete

### Applied Updates
- claude-learns: 1.0.0 -> 1.1.0
  - 2 new commands added
  - 3 commands updated
- serena: reinstalled with latest

### Conflicts (kept local)
- .claude/commands/debug.md (your modifications preserved)

### Checkpoint
Commit: [SHA]
Rollback: /claude-learns.update --rollback

### Recommended Next Steps
1. Run /claude-learns.audit to verify documentation consistency
2. Run /mcp to verify MCP servers
3. Test key commands: /claude-learns.go, /learn, /eliminate
```

---

## Rollback

When user runs `/claude-learns.update --rollback`:

### Step 1: Read Checkpoint

```bash
# Check if checkpoint exists
if [ -f .claude/update-checkpoint.txt ]; then
  SHA=$(cat .claude/update-checkpoint.txt)
else
  echo "No checkpoint found. Nothing to rollback."
  exit
fi
```

### Step 2: Confirm with User

```
## Rollback Confirmation

This will reset to commit: [SHA]
All changes since the checkpoint will be lost.

Are you sure you want to rollback? (yes/no)
```

### Step 3: Execute Rollback

```bash
git reset --hard [SHA]
```

### Step 4: Verify

```bash
git log -1 --oneline
```

### Step 5: Clean Up

```bash
rm .claude/update-checkpoint.txt
```

Display:
```
## Rollback Complete

Restored to: [SHA]
Current state: [git log output]
```

---

## Initialize Registry

If `.claude/update-registry.yaml` doesn't exist, create it:

```yaml
# Tool Update Registry
# Created by /claude-learns.update command
#
# This file tracks installed tools and their update sources.
# Add new tools here to include them in /claude-learns.update checks.

registry_version: "1.0"
created_date: "[today]"

tools:
  claude-learns:
    type: template
    source: https://github.com/danielcbright/claude-learns
    docs_url: https://raw.githubusercontent.com/danielcbright/claude-learns/main/UPDATE.md
    install_docs: https://raw.githubusercontent.com/danielcbright/claude-learns/main/INSTALL.md
    installed_version: "1.0.0"
    installed_date: "[today]"

  serena:
    type: mcp-server
    source: https://github.com/oraios/serena
    docs_url: https://raw.githubusercontent.com/oraios/serena/main/README.md
    install_command: "claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project $(pwd)"
    installed_version: null

  context7:
    type: mcp-server
    source: https://github.com/upstash/context7
    docs_url: https://raw.githubusercontent.com/upstash/context7/main/README.md
    install_command: null
    installed_version: null

# Add additional tools as needed:
#
#   new-tool:
#     type: mcp-server | template | cli-tool
#     source: https://github.com/org/repo
#     docs_url: https://raw.githubusercontent.com/org/repo/main/README.md
#     install_command: "installation command" (optional)
#     installed_version: null
```

---

## Adding New Tools

To add a new tool to the update system:

1. Edit `.claude/update-registry.yaml`
2. Add entry under `tools:`:
   ```yaml
   new-tool:
     type: mcp-server  # or template, cli-tool
     source: https://github.com/org/repo
     docs_url: https://raw.githubusercontent.com/org/repo/main/README.md
     install_command: "optional install command"
     installed_version: null
   ```
3. Run `/claude-learns.update new-tool` to fetch and install

---

## Protected Paths (Never Modified)

These paths are SACRED and will NEVER be modified by /update:

| Path | Reason |
|------|--------|
| `.serena/memories/*` | User's learned knowledge |
| `.specify/specs/*` | User's specifications |
| `.specify/memory/constitution.md` | User's project rules |
| `.specify/memory/corrections.md` | User's correction history |
| `.elimination/active/*` | Active debugging session |
| `.elimination/archive/*` | Historical debugging data |

---

## Troubleshooting

### "No checkpoint found"

Run `/claude-learns.update` first to create a checkpoint before trying to rollback.

### "Uncommitted changes detected"

Commit or stash your changes before running /update:
```bash
git add -A && git commit -m "save work"
# OR
git stash
```

### "Tool not in registry"

Add the tool to `.claude/update-registry.yaml` manually, then run `/claude-learns.update [tool-name]`.

### "WebFetch failed"

Check internet connection. The update system requires web access to fetch latest documentation.

---

## Example Session

```
User: /update

Claude: ## Git Safety Check
Working directory is clean. Creating checkpoint...

Checkpoint created: abc123f
Rollback available: /claude-learns.update --rollback

## Checking for Updates

### claude-learns
Current: 1.0.0
Fetching latest from github.com/danielcbright/claude-learns...
Latest: 1.1.0

Changes:
- New command: /foo
- Updated: /claude-learns.learn (improved routing)
- Updated: /eliminate (better heuristics)

### serena
Current: (checking MCP status)
Fetching latest from github.com/oraios/serena...
Update available.

Proceed with updates? (yes to update all, or specify tool name)

User: yes

Claude: Updating claude-learns...
- Added: .claude/commands/foo.md
- Updated: .claude/commands/learn.md
- Skipped: .serena/memories/* (protected)

Updating serena...
- Removing current installation...
- Installing latest...
- Verifying with /mcp...

## Update Complete

All tools updated successfully.
Checkpoint: abc123f
Rollback: /claude-learns.update --rollback
```
