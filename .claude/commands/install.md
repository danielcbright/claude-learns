# Install Template to Project

Install this Claude + Serena template into a target project.

## Instructions

You are installing the claude-serena-template into a user's project.

### Step 1: Gather Information

Ask the user for:
1. **Target project path** (absolute path to their project root)
2. **Project name** (for configurations)
3. **Primary programming language(s)** (e.g., typescript, go, python)

### Step 2: Read Installation Guide

Read `INSTALL.md` in this template repository for detailed instructions.

### Step 3: Execute Installation

1. **Copy directories**:
   - Copy `.claude/commands/` to `[target]/.claude/commands/`
   - Copy `.serena/memories/` to `[target]/.serena/memories/`

2. **Create configuration**:
   - Create `[target]/.serena/project.yml` with user's language settings

3. **Copy and customize CLAUDE.md**:
   - Copy `CLAUDE.md` to target
   - Replace ALL `[PLACEHOLDER]` values with user's project info
   - Remove the YAML frontmatter (it's template-specific)
   - Remove the "TEMPLATE MODE DETECTION" comment block

4. **Verify existing files**:
   - If target already has CLAUDE.md, ask user: merge or replace?
   - If target already has .serena/project.yml, skip (don't overwrite)

### Step 4: Post-Installation

1. Report what was created
2. List available slash commands
3. Remind user to:
   - Run `/mcp` to check Serena connection
   - Install Serena MCP if not connected
   - Customize CLAUDE.md further as needed

### Step 5: Verify (Optional)

If Serena is connected, run:
- `check_onboarding_performed()`
- `onboarding()` if needed
- Test with `find_symbol("[common_symbol]")`

## Output Format

After installation, provide a summary:

```
Installation complete!

Created:
- [target]/.claude/commands/ (7 commands)
- [target]/.serena/memories/claude_code_patterns.md
- [target]/.serena/project.yml
- [target]/CLAUDE.md

Next: Run /mcp to verify Serena, then /go [task] to test
```
