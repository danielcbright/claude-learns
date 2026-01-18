# Test Projects

These minimal project skeletons are used to test claude-learns template installation and command behavior.

## Usage

### 1. Test Template Installation

```bash
cd test-projects/minimal-js
# Then ask Claude: "Install the claude-learns template here"
```

### 2. Test Commands in Isolation

After installing, test commands without affecting the main template:

```bash
cd test-projects/minimal-js
/learn
/eliminate "test symptom"
/spec-create test-feature
```

### 3. Reset After Testing

```bash
cd test-projects/minimal-js
rm -rf .claude .serena .elimination .specify CLAUDE.md
```

## Project Types

| Project | Language | Purpose |
|---------|----------|---------|
| `minimal-js` | JavaScript/Node.js | Test JS/TS project installation |
| `minimal-py` | Python | Test Python project installation |
| `minimal-go` | Go | Test Go project installation |

## Maintenance

These are intentionally minimal. Do not add:
- Real application code
- Complex dependencies
- Actual project content

The goal is testing template behavior, not building applications.

## What Gets Installed

When the template is installed to a test project:

```
minimal-js/
├── .claude/commands/        # From template/
├── .serena/memories/        # From template/
├── .elimination/            # From template/
├── .specify/                # From template/
├── CLAUDE.md                # From template/ (customized)
├── package.json             # Original (unchanged)
└── src/index.js             # Original (unchanged)
```

The `.gitignore` in this directory ensures installed template files are not committed.
