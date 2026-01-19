# /claude-learns.eliminate-history - Review Past Elimination Sessions

**Syntax:** `/claude-learns.eliminate-history [--search query] [--limit N] [--outcome success|failure]`

Review archived elimination sessions to find similar past investigations.

## Usage

```bash
# List recent sessions
/claude-learns.eliminate-history

# Search for similar issues
/claude-learns.eliminate-history --search "timeout"

# Filter by outcome
/claude-learns.eliminate-history --outcome success --limit 5

# View specific session details
/claude-learns.eliminate-history --session 2026-01-15-001
```

## Output Format

### Session List

```
## 📚 Elimination History

| Date | Session | Problem | Outcome | Root Cause | Duration |
|------|---------|---------|---------|------------|----------|
| 2026-01-15 | 001 | API timeout errors | ✅ Success | Race condition | 45min |
| 2026-01-12 | 003 | Build failures | ✅ Success | Dep version | 20min |
| 2026-01-10 | 002 | Memory growth | ❌ Inconclusive | (multiple) | 2hr |
| 2026-01-08 | 001 | Auth failures | ✅ Success | Config drift | 30min |

**Total sessions:** 12 | **Success rate:** 83%
```

### Session Detail (--session)

```
## 📋 Session 2026-01-15-001: API Timeout Errors

**Problem:** Intermittent 500 errors on /api/v2/orders endpoint
**Duration:** 45 minutes
**Outcome:** ✅ Resolved

### Hypotheses Generated
1. H1: Database connection pool exhaustion → ❌ Eliminated (contradicting evidence)
2. H2: Memory leak causing OOM → ❌ Eliminated (stable memory)
3. H3: Race condition in request handler → ✅ Confirmed (root cause)
4. H4: Upstream service timeout → ❌ Eliminated (local timing)

### Key Evidence
- DB connections at 45% during errors → Eliminated H1
- Lock contention in SharedCache.get() → Confirmed H3

### Resolution
Replaced shared cache with request-scoped cache in OrderService

### Learnings Extracted
- Pattern added: "Errors correlating with RPS → prioritize concurrency"
- Heuristic updated: concurrency_load_pattern success rate 78%→82%

### Files
- Archive: `.elimination/archive/2026-01/session-001/`
- Trace: `traces/session-001-trace.json`
```

## Search Capabilities

The search matches against:
- Problem descriptions
- Hypothesis descriptions
- Root cause summaries
- Domain tags
- Evidence descriptions

This helps find relevant past investigations when facing similar issues.

## Learning Integration

When viewing history for a similar problem:
1. Note which hypotheses were most/least likely
2. See which evidence was most discriminating
3. Apply learned patterns to current investigation

```
User: /claude-learns.eliminate-history --search "connection timeout redis"

Claude: Found 3 relevant past sessions:

## Related Investigations

### 1. Session 2026-01-05-002 (92% match)
**Problem:** Redis connection timeouts under load
**Root cause:** Connection pool too small for concurrent requests
**Key insight:** Check pool size vs concurrent connection needs first

### 2. Session 2025-12-20-001 (78% match)
**Problem:** Intermittent Redis timeouts
**Root cause:** Network MTU mismatch causing packet fragmentation
**Key insight:** Check network config if timeouts are random, not load-correlated

### 3. Session 2025-11-15-003 (65% match)
**Problem:** Redis ETIMEDOUT errors
**Root cause:** Redis maxmemory reached, eviction causing delays
**Key insight:** Monitor INFO memory before assuming network issues

**Suggested starting hypotheses for current investigation:**
1. Connection pool sizing (based on session 1)
2. Memory limits (based on session 3)
3. Network configuration (based on session 2)
```
