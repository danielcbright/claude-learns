Perform a learning loop review for this session.

## Review Current Session

Analyze what happened in this session and identify learnings:

### 1. Pattern Recognition
- Did I use any approach multiple times that should be documented?
- Did I discover a code pattern that future sessions should know?
- Did I find a useful command sequence worth saving?

### 2. Gotchas & Pitfalls
- Did anything unexpected happen?
- Did I hit an error that was non-obvious to debug?
- Did I make an incorrect assumption?

### 3. Workflow Insights
- What took longer than expected? Why?
- What tool or skill would have helped?
- Was any CLAUDE.md guidance missing or wrong?

### 4. Architecture Knowledge
- Did I learn something about how this codebase works?
- Did I discover undocumented dependencies or relationships?
- Did I understand a design decision that should be captured?

### 5. Skill Update Opportunities

Skills are shared across projects - updates benefit everyone.

- Did a skill's instructions prove inadequate or misleading?
- Did I discover a pattern that would help OTHER projects using this skill?
- Did I have to repeatedly explain something the skill should cover?
- Did I work around a gap that should be documented?

**Check skill locations:** `~/.claude/skills/*/skill.md`

## Generate Recommendations

Based on the review, provide structured recommendations:

```
📚 **Learning Loop Results**

### Recommended New Memories
1. **[memory_name]** 
   - Type: [architecture/patterns/gotchas/workflows/history]
   - Content summary: [what to capture]
   - Rationale: [why this helps future sessions]

### Recommended CLAUDE.md Updates
1. **Section**: [which section]
   - Change: [what to add/modify/remove]
   - Rationale: [why this improves guidance]

### Recommended New Skills
1. **[skill_name]**
   - Would help with: [use case]
   - How to add: [command or instructions]

### Recommended Skill Updates
1. **[existing_skill_name]**
   - Location: `~/.claude/skills/[skill]/skill.md`
   - Change: [what to add/modify]
   - Rationale: [why this helps other projects too]

### Recommended Workflow Changes
1. **[workflow_name]**
   - Current issue: [what's suboptimal]
   - Proposed improvement: [how to fix]
```

## Execute Updates

After presenting recommendations, ask:
> "Would you like me to implement any of these updates?"

If approved:
1. Use `write_memory()` for new memories
2. Update CLAUDE.md directly for documentation changes
3. Add changelog entry with today's date
4. Confirm all changes made

---

Session context to review: $ARGUMENTS
