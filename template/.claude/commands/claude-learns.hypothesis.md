# /hypothesis - Add Hypothesis to Active Investigation

**Syntax:** `/claude-learns.hypothesis [description] [--confidence 0.X] [--domain category]`

Manually add a hypothesis to the current elimination investigation.

## Usage

```bash
# Basic usage - auto-assigns domain and default confidence
/hypothesis "Memory leak in image processing module"

# With explicit confidence
/hypothesis "Redis connection timeout" --confidence 0.65

# With domain categorization
/hypothesis "Version mismatch in lodash" --domain dependencies --confidence 0.4
```

## Valid Domains

- `code` - Logic errors, algorithm bugs, type issues
- `config` - Environment variables, settings, feature flags
- `dependencies` - Version conflicts, API changes, missing packages
- `data` - Invalid input, state corruption, edge cases
- `infrastructure` - Resource exhaustion, network, services
- `concurrency` - Race conditions, deadlocks, timing

## Behavior

1. **Check for active session**
   - If no session exists, prompt to start `/claude-learns.eliminate` first
   - If session exists, add hypothesis to `.elimination/active/hypotheses/`

2. **Generate hypothesis file**
   ```yaml
   id: "hyp-{timestamp}-{seq}"
   description: "{user_provided_description}"
   domain: {auto_detected_or_specified}
   source: user_suggested
   status: active
   
   confidence:
     initial: {specified_or_0.5}
     current: {same_as_initial}
     trend: neutral
   
   evidence:
     supporting: []
     contradicting: []
   
   metadata:
     created_at: "{timestamp}"
     context_tags: ["{extracted_keywords}"]
   ```

3. **Update session** to include new hypothesis in active set

4. **Suggest discriminating test** based on hypothesis domain

## Example

```
User: /hypothesis "Async job queue not processing due to Redis memory limit" --confidence 0.6 --domain infrastructure

Claude: Added hypothesis to active investigation:

📋 **H7: Redis Memory Limit Blocking Job Queue**
- Domain: Infrastructure
- Initial confidence: 0.60
- Source: User suggested

**Suggested discriminating tests:**
1. Check Redis INFO memory output for maxmemory status
2. Monitor SLOWLOG for blocked operations
3. Compare job enqueue rate vs processing rate

**If confirmed, this would explain:**
- Jobs queued but not processed
- Intermittent failures during high-load periods

Run `/claude-learns.evidence` after testing to record results.
```

## Integration

- Works with active `/claude-learns.eliminate` session
- Hypothesis appears in `/claude-learns.eliminate-status` output
- Evidence recorded via `/claude-learns.evidence` updates this hypothesis
