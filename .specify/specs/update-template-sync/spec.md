# Specification: update-template-sync

**Created**: 2026-01-19
**Status**: Draft
**Author**: Claude (with user)

---

## Overview

Enable the `/claude-learns.update claude-learns` command to actually sync template files from the upstream repository to a project that has adopted the claude-learns template.

### Problem Statement

Currently, the `/claude-learns.update` command:
- ✅ Updates MCP servers (serena, context7) via `claude mcp remove/add`
- ❌ Does NOT update claude-learns template files (commands, scripts, configs)

The command documentation describes fetching a `manifest.yaml` to determine which files to update, but this manifest doesn't exist, causing template updates to silently fail or be skipped.

### Goals

1. Create a manifest that lists all updateable template files
2. Enable Claude to fetch and apply template updates during `/claude-learns.update claude-learns`
3. Preserve user customizations and protected files
4. Provide clear conflict resolution when user has modified files

---

## Requirements

### Functional Requirements

#### FR-1: Manifest File
- **FR-1.1**: Create `template/manifest.yaml` listing all files that can be updated
- **FR-1.2**: Manifest must categorize files by update behavior:
  - `always_update`: Core files that should always be replaced (e.g., `claude-learns.update.md` itself)
  - `updateable`: Files that can be updated with conflict detection
  - `merge_only`: Config files where new keys are added but existing preserved
  - `protected`: Files that are NEVER modified (listed for documentation)
- **FR-1.3**: Manifest must include file checksums/hashes for change detection
- **FR-1.4**: Manifest must include version information

#### FR-2: Update Detection
- **FR-2.1**: Fetch manifest from `https://raw.githubusercontent.com/danielcbright/claude-learns/main/template/manifest.yaml`
- **FR-2.2**: Compare local file checksums against manifest to detect which files need updates
- **FR-2.3**: Report summary of available updates before applying

#### FR-3: Conflict Detection
- **FR-3.1**: Detect when user has modified an updateable file (checksum differs from both original and latest)
- **FR-3.2**: Present user with options: keep local, take update, view diff
- **FR-3.3**: Backup conflicting files to `.claude-learns-backup/` before overwriting

#### FR-4: Update Application
- **FR-4.1**: Fetch updated files from GitHub raw URLs
- **FR-4.2**: Write files to correct local paths
- **FR-4.3**: For `merge_only` files, intelligently merge YAML (add new keys, preserve existing values)
- **FR-4.4**: Update local registry with new version after successful update

#### FR-5: Protected Files
- **FR-5.1**: NEVER modify files in protected paths:
  - `.serena/memories/*`
  - `.specify/specs/*`
  - `.specify/memory/constitution.md`
  - `.specify/memory/corrections.md`
  - `.elimination/active/*`
  - `.elimination/archive/*`
- **FR-5.2**: Log when protected files are encountered (for transparency)

### Non-Functional Requirements

#### NFR-1: Safety
- All updates must be preceded by git checkpoint (already implemented)
- Rollback must restore ALL changed files

#### NFR-2: Transparency
- User must see exactly which files will be modified before update applies
- User must confirm before destructive operations

#### NFR-3: Offline Graceful Degradation
- If WebFetch fails, report error clearly and abort (don't partially update)

---

## Acceptance Criteria

### AC-1: Manifest Exists and Is Valid
- [ ] `template/manifest.yaml` exists in repository
- [ ] Manifest contains all 22 command files (4 generic + 18 claude-learns prefixed)
- [ ] Manifest contains elimination scripts (6 files)
- [ ] Manifest contains config files
- [ ] Manifest includes version and checksums

### AC-2: Update Detection Works
- [ ] Running `/claude-learns.update claude-learns` fetches manifest from GitHub
- [ ] Command reports which files have updates available
- [ ] Command shows version difference (e.g., "1.0.0 → 1.1.0")

### AC-3: Conflict Detection Works
- [ ] Modified local file triggers conflict warning
- [ ] User can choose to keep local version
- [ ] User can choose to take update (with backup)
- [ ] Backup is created in `.claude-learns-backup/`

### AC-4: Update Application Works
- [ ] New command files are added when present in manifest but not locally
- [ ] Updated command files replace local versions (with conflict handling)
- [ ] Config files are merged (new keys added, existing preserved)
- [ ] Protected files are never touched

### AC-5: Version Tracking Works
- [ ] After update, `.claude/update-registry.yaml` shows new version
- [ ] Running `/claude-learns.update --list` shows correct installed version

### AC-6: Rollback Works
- [ ] `/claude-learns.update --rollback` restores all files to pre-update state
- [ ] Rollback removes any newly added files

---

## Design

### Manifest Structure

```yaml
# template/manifest.yaml
version: "1.1.0"
generated: "2026-01-19"
base_url: "https://raw.githubusercontent.com/danielcbright/claude-learns/main/template"

files:
  # Always update - critical for update mechanism itself
  always_update:
    - path: ".claude/commands/claude-learns.update.md"
      checksum: "sha256:abc123..."

  # Updateable with conflict detection
  updateable:
    # Commands
    - path: ".claude/commands/go.md"
      checksum: "sha256:..."
    - path: ".claude/commands/debug.md"
      checksum: "sha256:..."
    - path: ".claude/commands/explore.md"
      checksum: "sha256:..."
    - path: ".claude/commands/refactor.md"
      checksum: "sha256:..."
    - path: ".claude/commands/claude-learns.learn.md"
      checksum: "sha256:..."
    # ... all 22 commands

    # Scripts
    - path: ".claude/scripts/elimination/eliminate_init.py"
      checksum: "sha256:..."
    # ... all 6 scripts

    # Skills
    - path: ".claude/skills/skill-creator/SKILL.md"
      checksum: "sha256:..."

  # Merge only - add new keys, preserve existing
  merge_only:
    - path: ".elimination/config.yaml"
      checksum: "sha256:..."
    - path: ".elimination/learned/heuristics.yaml"
      checksum: "sha256:..."
    - path: ".specify/config.yaml"
      checksum: "sha256:..."

  # Protected - documented but never touched
  protected:
    - ".serena/memories/*"
    - ".specify/specs/*"
    - ".specify/memory/constitution.md"
    - ".specify/memory/corrections.md"
    - ".elimination/active/*"
    - ".elimination/archive/*"

# Original checksums for conflict detection
# (checksum of file as shipped in previous version)
original_checksums:
  ".claude/commands/go.md": "sha256:original_hash..."
```

### Update Flow

```
1. User runs: /claude-learns.update claude-learns

2. Git Safety (existing):
   - Check clean working directory
   - Create checkpoint commit

3. Fetch Manifest:
   - WebFetch manifest.yaml from GitHub
   - Parse and validate

4. Compare Versions:
   - Current: from .claude/update-registry.yaml
   - Latest: from manifest.version
   - If same, report "already up to date"

5. For each file in manifest:

   IF always_update:
     - Fetch and replace (no questions)

   IF updateable:
     - Compare local checksum to manifest checksum
     - If match: already up to date, skip
     - If differs:
       - Compare local to original_checksum
       - If local == original: user hasn't modified, safe to update
       - If local != original: CONFLICT - ask user

   IF merge_only:
     - Fetch latest
     - Merge new keys into local (preserve existing values)

6. Apply Updates:
   - Fetch files via WebFetch
   - Write to local paths
   - For conflicts where user chose "take update": backup first

7. Update Registry:
   - Set installed_version to manifest.version
   - Set last_update to today

8. Report Summary:
   - Files added
   - Files updated
   - Files skipped (conflicts kept local)
   - New version number
```

---

## Out of Scope

- Automatic updates (always requires user to run command)
- Partial rollback (rollback is all-or-nothing)
- Branch selection (always uses main branch)
- Custom manifest URLs (hardcoded to official repo)

---

## Test Plan

### Manual Testing

1. **Fresh Install Test**
   - Install template to new project
   - Run `/claude-learns.update claude-learns`
   - Verify "already up to date" message

2. **Update Available Test**
   - Modify manifest version in upstream
   - Run update command
   - Verify files are updated

3. **Conflict Test**
   - Modify a command file locally
   - Run update when upstream has changes
   - Verify conflict is detected
   - Test "keep local" option
   - Test "take update" option (verify backup created)

4. **Protected Files Test**
   - Verify memories are never touched
   - Verify specs are never touched

5. **Rollback Test**
   - Run update
   - Run rollback
   - Verify all files restored

---

## Implementation Notes

- The manifest generation should be automated (script to compute checksums)
- Consider adding a `manifest-generate.py` script for maintainers
- Checksums should be SHA256 for reliability
- WebFetch may have size limits - keep manifest concise

---

## References

- Current `/claude-learns.update` command: `.claude/commands/claude-learns.update.md`
- Update documentation: `UPDATE.md`
- Tool registry: `.claude/update-registry.yaml`
