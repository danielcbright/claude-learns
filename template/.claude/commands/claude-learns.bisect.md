# /claude-learns.bisect - Git Bisect Integration for Commit-Level Elimination

**Syntax:** `/claude-learns.bisect [bad_ref] [good_ref] [test_command]`

Use git bisect's binary search to identify the exact commit that introduced a bug.

## Overview

Git bisect is elimination applied to version control. It uses binary search to efficiently
find the commit that introduced a regression, testing O(log n) commits instead of O(n).

## Usage

```bash
# Interactive mode - Claude guides you through
/bisect

# Specify known states
/claude-learns.bisect HEAD v1.2.0

# Fully automated with test command
/claude-learns.bisect HEAD v1.2.0 "npm test -- --grep 'order processing'"
```

## Workflow

### Phase 1: Setup

1. **Identify bad state** (where bug exists)
   - Usually `HEAD` or current branch
   - Can be a specific commit, tag, or branch

2. **Identify good state** (where bug didn't exist)
   - A previous release tag
   - A known-working commit
   - "Last time it worked" date → find commit

3. **Define test** for bug presence
   - Specific test command that fails when bug present
   - Manual verification prompt

### Phase 2: Binary Search

Git bisect automatically:
1. Checks out middle commit between good and bad
2. You/script tests if bug exists at this commit
3. Marks commit as good or bad
4. Repeats with narrowed range

```
Start: 128 commits between good and bad
After 1 test: 64 commits
After 2 tests: 32 commits
After 3 tests: 16 commits
After 4 tests: 8 commits
After 5 tests: 4 commits
After 6 tests: 2 commits
After 7 tests: 1 commit → FOUND
```

### Phase 3: Analysis

Once found:
1. Display the offending commit
2. Show the diff
3. Analyze what changed
4. Link to elimination session if debugging further needed

## Example Session

```
User: /claude-learns.bisect HEAD v2.1.0 "npm test -- --grep 'API returns correct status'"

Claude: Starting git bisect to find bug-introducing commit...

## Setup
- Bad: HEAD (abc1234 - 2026-01-18)
- Good: v2.1.0 (def5678 - 2026-01-05)
- Test: npm test -- --grep 'API returns correct status'
- Commits to search: 47
- Estimated tests needed: 6

## Bisecting...

**Test 1/~6**: Checking commit 789abc0 (2026-01-12)
Running: npm test -- --grep 'API returns correct status'
Result: ✅ PASS → Marking as GOOD
Remaining: 24 commits

**Test 2/~6**: Checking commit 321def0 (2026-01-15)
Running: npm test -- --grep 'API returns correct status'
Result: ❌ FAIL → Marking as BAD
Remaining: 12 commits

**Test 3/~6**: Checking commit 654ghi0 (2026-01-13)
Running: npm test -- --grep 'API returns correct status'
Result: ✅ PASS → Marking as GOOD
Remaining: 6 commits

**Test 4/~6**: Checking commit 987jkl0 (2026-01-14)
Running: npm test -- --grep 'API returns correct status'
Result: ❌ FAIL → Marking as BAD
Remaining: 3 commits

**Test 5/~6**: Checking commit aaa111 (2026-01-14 09:30)
Running: npm test -- --grep 'API returns correct status'
Result: ✅ PASS → Marking as GOOD
Remaining: 1 commit

## 🎯 Bug-Introducing Commit Found!

**Commit:** bbb222
**Author:** developer@example.com
**Date:** 2026-01-14 11:45:00
**Message:** "Optimize order validation for performance"

### Changed Files
- src/services/OrderValidator.ts (+45, -12)
- src/utils/validation.ts (+8, -3)

### Key Changes
```diff
- if (order.status === 'pending' || order.status === 'processing') {
+ if (order.status === 'pending') {  // Removed processing check
```

### Analysis
The commit removed the `processing` status check from validation,
causing orders in `processing` state to fail validation.

### Next Steps
1. Revert this commit: `git revert bbb222`
2. Or fix forward: restore the removed condition
3. Add regression test to prevent recurrence

Run `/claude-learns.eliminate` if you need to investigate why this change was made
or if there are additional related issues.
```

## Commands During Bisect

| Input | Action |
|-------|--------|
| `good` | Mark current commit as good (bug not present) |
| `bad` | Mark current commit as bad (bug present) |
| `skip` | Skip current commit (can't test, e.g., won't build) |
| `reset` | Abort bisect and return to original HEAD |
| `log` | Show bisect log so far |
| `visualize` | Open gitk to visualize remaining range |

## Integration with /eliminate

When bisect finds the commit but root cause unclear:

```bash
# Bisect found the commit, now investigate the change
/eliminate "Change in OrderValidator.ts causing validation failures"
```

The elimination session can use the bisect result as strong evidence:
- Hypothesis: "Bug is in OrderValidator.ts changes" → confidence 0.95
- Narrows hypothesis space to specific files/functions

## Automated Testing Tips

Good test commands for `/claude-learns.bisect`:
```bash
# Specific test
"npm test -- --grep 'specific test name'"
"pytest tests/test_orders.py::test_validation -x"

# Build check
"npm run build && npm test"

# Custom script
"./scripts/check_bug.sh"
```

Test script requirements:
- Exit 0 = good (bug not present)
- Exit 1-127 = bad (bug present)
- Exit 125 = skip (can't test this commit)
