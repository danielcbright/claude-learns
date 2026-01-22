# Install Template to Project

Install this Claude + Serena template into a target project.

## Important: Source Location

**Always copy from `template/` directory**, not from root-level files.

The root-level files (`.claude/`, `.serena/`, etc.) are working copies used for
developing the template itself. The `template/` directory contains the clean
distributable versions.

## Instructions

You are installing the claude-learns template into a user's project.

### Step 1: Gather Information

Ask the user for:
1. **Target project path** (absolute path to their project root)
2. **Project name** (for configurations)
3. **Primary programming language(s)** (e.g., typescript, go, python)

### Step 2: Read Installation Guide

Read `INSTALL.md` in this template repository for detailed instructions.

### Step 3: Execute Installation

**Source**: `template/` directory (NOT root-level files)

1. **Copy directories**:
   - Copy `template/.claude/commands/` to `[target]/.claude/commands/`
   - Copy `template/.claude/update-registry.yaml` to `[target]/.claude/update-registry.yaml`
   - Copy `template/.serena/memories/` to `[target]/.serena/memories/`
   - Copy `template/.elimination/` to `[target]/.elimination/`
   - Copy `template/.specify/` to `[target]/.specify/`

2. **Create configuration**:
   - Create `[target]/.serena/project.yml` with user's language settings
   - Update `[target]/.claude/update-registry.yaml` with installation date

3. **Copy and customize CLAUDE.md**:
   - Copy `template/CLAUDE.md` to target
   - Replace ALL `[PLACEHOLDER]` values with user's project info
   - Remove the YAML frontmatter (it's template-specific)
   - Remove the "TEMPLATE MODE DETECTION" comment block

4. **Verify existing files**:
   - If target already has CLAUDE.md, ask user: merge or replace?
   - If target already has .serena/project.yml, skip (don't overwrite)

### Step 4: Post-Installation Verification

Run health checks after copying files. **Output warnings but don't block installation.**

#### 4.1 Verify Commands Installed

Check that `.claude/commands/` contains expected files:

```
Expected commands (22 total):
- go.md
- explore.md
- debug.md
- refactor.md
- learn.md
- audit.md
- skills.md
- update.md
- install.md
- eliminate.md
- hypothesis.md
- evidence.md
- eliminate-status.md
- eliminate-history.md
- bisect.md
- spec-create.md
- spec-validate.md
- spec-debug.md
- spec-deviation.md
- spec-list.md
- spec-verify.md
- spec-correction.md
```

Output:
```
## Command Verification

✅ Found 22/22 expected commands
   OR
⚠️ Missing commands: [list missing]
```

#### 4.2 Check MCP Availability

Test if Serena MCP is available:

```python
# Try to call list_memories() or get_current_config()
```

Output:
```
## MCP Status

✅ Serena MCP connected - memories and symbols available
   OR
⚠️ Serena MCP not detected
   To install: claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project [target]

   Without Serena:
   - Memory tools won't work (use file reads instead)
   - Symbol navigation unavailable
   - Template still functional, just less powerful
```

#### 4.3 Prompt for Constitution

Prompt user to define 2-3 non-negotiable project rules:

```
## Project Constitution

The constitution (.specify/memory/constitution.md) defines non-negotiable rules.
These are checked during /claude-learns.spec-verify and debugging sessions.

Please provide 2-3 rules for your project. Examples:
- "All API endpoints must have authentication"
- "No direct database queries outside repository classes"
- "All user input must be validated before processing"

Your rules (or press Enter to skip for now):
```

If user provides rules, write them to `[target]/.specify/memory/constitution.md`.

#### 4.4 Dry Run /claude-learns.learn Routing

Simulate a learning to verify routing works:

```
## Learning Route Verification (Dry Run)

Testing routing logic with sample learnings...

Sample: "The auth module uses factory pattern"
  → Route: .serena/memories/ ✅

Sample: "Claimed login worked but validation was missing"
  → Route: .specify/memory/corrections.md ✅

Sample: "Chose PostgreSQL for ACID compliance"
  → Route: .serena/memories/decision-log.md ✅

Sample: "Timeout errors usually mean connection pool exhaustion"
  → Route: .elimination/learned/heuristics.yaml ✅

Routing verification: PASS
```

Check that destination files/directories exist:
- `.serena/memories/` exists? ✅/❌
- `.specify/memory/corrections.md` exists? ✅/❌
- `.serena/memories/decision-log.md` exists? ✅/❌
- `.elimination/learned/heuristics.yaml` exists? ✅/❌

### Step 5: Final Summary

```
## Installation Complete!

### Files Created
- [target]/.claude/commands/ (22 commands)
- [target]/.claude/update-registry.yaml (for /claude-learns.update command)
- [target]/.serena/memories/ (6 memory files)
- [target]/.elimination/ (debugging system)
- [target]/.specify/ (spec system)
- [target]/CLAUDE.md

### Health Check Results
- Commands: ✅ 22/22 installed
- Update Registry: ✅ Created
- Serena MCP: ✅ Connected / ⚠️ Not detected (see above)
- Constitution: ✅ Configured / ⚠️ Skipped (configure later)
- Routing: ✅ All paths verified

### Warnings
[List any warnings from verification steps]

### Next Steps
1. Review and customize CLAUDE.md for your project
2. [If Serena not connected] Install Serena MCP (command above)
3. [If constitution skipped] Edit .specify/memory/constitution.md
4. Test with: /claude-learns.go [small task]

### Quick Test
Run these to verify installation:
- /claude-learns.update --list      → Should show registered tools
- /claude-learns.learn              → Should show "No learnings to capture" or routing options
- /claude-learns.eliminate-status   → Should show "No active investigation"
- /claude-learns.spec-list          → Should show specs directory (may be empty)
```

## Output Format

Combine all verification outputs into a single summary. Use:
- ✅ for successful checks
- ⚠️ for warnings (non-blocking)
- ❌ for failures (still non-blocking, but emphasize)

## Handling Verification Failures

Even if verification finds issues:
1. **Complete the installation** - don't roll back
2. **List all warnings clearly** - so user can address them
3. **Provide fix commands** - actionable next steps
4. **Suggest /claude-learns.audit later** - to re-check after fixes
