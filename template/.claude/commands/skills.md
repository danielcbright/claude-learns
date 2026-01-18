Discover, evaluate, and document available skills for this project.

## Skill Discovery Process

### 1. Scan Available Skills

Check all skill sources:

```bash
# Check MCP-provided skills
/mcp

# Check local skill directories
ls -la .claude/skills/ 2>/dev/null
ls -la /mnt/skills/ 2>/dev/null

# Check for skill manifests
find . -name "SKILL.md" -o -name "skill.json" 2>/dev/null
```

### 2. Inventory Current Skills

List skills currently documented in CLAUDE.md "Active Skills" section.

### 3. Evaluate Each Discovered Skill

For each skill found:

```
Skill: [NAME]
Location: [PATH]
Documentation: [Read SKILL.md or equivalent]

Evaluation:
- Stack compatibility: [Yes/No/Partial] - [explanation]
- Workflow fit: [High/Medium/Low] - [explanation]
- Quality assessment: [based on docs/testing]
- Overlap with existing: [None/Some/Significant] - [what overlaps]

Verdict: [ADD / SKIP / REPLACE existing]
Reason: [justification]
```

### 4. Test Promising Skills

For skills worth adding, perform a quick test:

```
1. Read the skill documentation thoroughly
2. Identify a simple test case relevant to this project
3. Execute the skill with test input
4. Evaluate output quality
5. Note any configuration needed for this project
```

## Project Context for Evaluation

Consider this project's needs:

```
Languages: [FROM PROJECT OVERVIEW]
Frameworks: [FROM PROJECT OVERVIEW]
Architecture: [FROM PROJECT OVERVIEW]

Common tasks:
- [List frequent development activities]
- [List common pain points]
- [List areas where automation helps]
```

## Skill Documentation Template

For each skill to add to CLAUDE.md:

```markdown
#### Skill: [SKILL_NAME]
- **Purpose**: [One-line description]
- **Location**: [Path to SKILL.md or how to invoke]
- **Use when**: 
  - [Scenario 1 specific to this project]
  - [Scenario 2 specific to this project]
  - [Scenario 3 specific to this project]
- **Example**:
  ```
  [Actual example using this project's context]
  ```
- **Configuration**: [Any project-specific setup needed]
- **Gotchas**: [Known limitations or issues]
- **Alternatives**: [Other ways to accomplish the same thing]
```

## Skills Report

Generate a comprehensive report:

```
🔧 **Skills Discovery Report**

### Discovered Skills
| Skill | Source | Relevant | Status |
|-------|--------|----------|--------|
| [name] | [location] | ✅/⚠️/❌ | New/Existing/Deprecated |
| ... | ... | ... | ... |

### Recommended Additions
1. **[Skill Name]**
   - Why: [how it helps this project]
   - Test result: [what happened when tested]

### Recommended Removals
1. **[Skill Name]**
   - Why: [no longer relevant/superseded/broken]

### Skills Needing Update
1. **[Skill Name]**
   - What changed: [new version/config change/etc]

### Missing Capabilities
1. **[Capability]**
   - Would help with: [use case]
   - Possible solutions: [skills/tools to investigate]
```

## Execute Updates

After presenting the report:

1. Update CLAUDE.md "Active Skills" section
2. Remove deprecated skills
3. Add new skill documentation with examples
4. Update changelog with skills changes

Ask:
> "I've identified [N] skills to add, [M] to remove, and [P] to update. Shall I update CLAUDE.md?"

---

Focus area (optional): $ARGUMENTS
