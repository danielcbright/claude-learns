# Real-World Examples

Concrete scenarios showing how to use claude-learns effectively.

---

## Example 1: Debugging a Failing API Endpoint

**Scenario**: Your `/api/users/:id` endpoint intermittently returns 500 errors. Simple debugging hasn't found the cause.

### Step 1: Start Elimination Debugging

```
/eliminate "GET /api/users/:id returns 500 errors intermittently"
```

Claude generates hypotheses:

```
Session: elim-2024-01-15-api-500

Hypotheses Generated:
  H1: Database connection pool exhaustion (0.65)
  H2: Race condition in user cache (0.55)
  H3: Invalid user ID format not caught (0.40)
  H4: Memory leak in request handler (0.35)
  H5: Upstream auth service timeout (0.30)
```

### Step 2: Add a Hypothesis You Suspect

```
/hypothesis "Redis session lookup failing silently"
```

```
Added H6: Redis session lookup failing silently (0.50)
```

### Step 3: Gather Evidence

You check the logs and find high connection pool usage:

```
/evidence H1 "DB pool at 95% capacity during errors" --supports
```

```
H1 confidence updated: 0.65 -> 0.78
```

You also find Redis is healthy:

```
/evidence H6 "Redis latency <2ms, no errors in logs" --contradicts
```

```
H6 confidence updated: 0.50 -> 0.18 (soft eliminated)
```

### Step 4: Check Status

```
/eliminate-status
```

```
Session: elim-2024-01-15-api-500

Active Hypotheses:
  H1: Database connection pool exhaustion (0.78) <-- LEADING
  H2: Race condition in user cache (0.55)
  H4: Memory leak in request handler (0.35)
  H5: Upstream auth service timeout (0.30)

Eliminated:
  H3: Invalid user ID format not caught (0.08)
  H6: Redis session lookup failing silently (0.18)

Next suggested action: Test H1 by increasing pool size temporarily
```

### Step 5: Confirm and Fix

You increase the pool size, errors stop. Mark as confirmed:

```
/evidence H1 "Increased pool from 10 to 25, errors stopped" --confirms
```

Claude marks H1 as confirmed (>0.90) and suggests the fix.

### Step 6: Save the Learning

```
/learn
```

Claude offers to save:
- A debugging lesson about connection pool monitoring
- A heuristic pattern for "intermittent 500 = check resource pools first"

---

## Example 2: Adding User Authentication

**Scenario**: You need to add JWT-based authentication to an Express API.

### Step 1: Create a Specification

```
/spec-create user-authentication
```

Claude asks clarifying questions and creates `.specify/specs/user-authentication/spec.md`:

```markdown
# Specification: User Authentication

## Overview
JWT-based authentication for the Express API.

## Acceptance Criteria

### AC-1: Login Endpoint
- POST /api/auth/login accepts email and password
- Returns JWT token on success (200)
- Returns 401 on invalid credentials
- Token expires in 24 hours

### AC-2: Protected Routes
- Routes under /api/protected/* require valid JWT
- Invalid/expired tokens return 401
- Token passed via Authorization: Bearer header

### AC-3: Token Refresh
- POST /api/auth/refresh accepts valid token
- Returns new token with extended expiry
- Rejects expired tokens

## Out of Scope
- OAuth/social login (future)
- Password reset flow (separate spec)
```

### Step 2: Implement with /go

```
/go implement the user-authentication spec
```

Claude:
1. Reads the spec
2. Checks relevant memories for auth patterns
3. Creates the implementation:
   - `src/middleware/auth.ts`
   - `src/routes/auth.ts`
   - `src/services/jwt.ts`
4. Adds tests

### Step 3: Validate Against Spec

```
/spec-validate user-authentication
```

```
Validating: user-authentication

AC-1: Login Endpoint
  [PASS] POST /api/auth/login exists
  [PASS] Returns 200 with token on valid credentials
  [PASS] Returns 401 on invalid credentials
  [PASS] Token expiry set to 24h

AC-2: Protected Routes
  [PASS] Middleware applied to /api/protected/*
  [FAIL] Missing 401 response for expired tokens

AC-3: Token Refresh
  [PASS] POST /api/auth/refresh exists
  [PASS] Returns new token
  [PASS] Rejects expired tokens

Result: 8/9 criteria passing
Action needed: Fix expired token handling in AC-2
```

### Step 4: Fix and Re-validate

Claude fixes the expired token handling, then:

```
/spec-verify user-authentication
```

```
Verification: user-authentication

Evidence collected:
  AC-1: curl test output showing 200/401 responses
  AC-2: Test suite output - all auth tests passing
  AC-3: Postman collection results attached

All acceptance criteria: PASS

Ready to mark complete.
```

### Step 5: Save Insights

```
/learn
```

Claude suggests saving:
- JWT implementation pattern to `decision-log`
- Auth middleware placement to `claude_code_patterns`

---

## Example 3: Understanding Legacy Code

**Scenario**: You've inherited a codebase and need to understand how the payment system works.

### Step 1: Explore the Area

```
/explore payment processing
```

Claude systematically explores:

```
Exploring: payment processing

Found entry points:
  - src/services/PaymentService.ts (main service)
  - src/routes/payments.ts (API routes)
  - src/models/Transaction.ts (data model)

Call graph for processPayment():
  PaymentService.processPayment()
    -> validatePaymentMethod()
    -> StripeGateway.charge()
    -> TransactionRepository.save()
    -> NotificationService.sendReceipt()

Key patterns discovered:
  - Uses Strategy pattern for payment gateways
  - Transactions are immutable after creation
  - Webhook handlers in src/webhooks/stripe.ts

Shall I save this as a memory?
```

### Step 2: Deep Dive on Specific Symbol

You want to understand the webhook handling:

```
/go explain how stripe webhooks are processed
```

Claude reads the specific files and explains:

```
Stripe Webhook Flow:

1. POST /webhooks/stripe hits stripeWebhookHandler()
2. Signature verified via stripe.webhooks.constructEvent()
3. Event type routed to specific handlers:
   - payment_intent.succeeded -> handlePaymentSuccess()
   - payment_intent.failed -> handlePaymentFailure()
   - charge.refunded -> handleRefund()
4. Each handler updates Transaction status
5. Sends notification via NotificationService

Key gotcha: Webhooks are idempotent via event_id check
```

### Step 3: Build a Memory

```
/learn
```

Claude creates `.serena/memories/payment-system.md`:

```markdown
# Payment System Architecture

## Entry Points
- PaymentService.processPayment() - main processing
- stripeWebhookHandler() - async updates

## Key Patterns
- Strategy pattern for gateways (Stripe, PayPal stubs)
- Immutable transactions
- Idempotent webhooks via event_id

## Gotchas
- Must verify webhook signatures
- Refunds create new transactions, don't modify originals
- Test mode uses different API keys (see .env.example)
```

Now future sessions start with this context.

---

## Example 4: Safe Refactoring

**Scenario**: You need to rename `UserService` to `AccountService` across the codebase.

### Step 1: Plan the Refactor

```
/refactor rename UserService to AccountService
```

Claude analyzes impact:

```
Refactoring: UserService -> AccountService

Files affected:
  - src/services/UserService.ts (rename file)
  - src/routes/users.ts (import)
  - src/controllers/UserController.ts (import + usage)
  - src/tests/UserService.test.ts (rename + update)
  - src/index.ts (import)

References found: 23 total
  - Class references: 8
  - Import statements: 5
  - Type annotations: 6
  - Test descriptions: 4

Proceed with refactoring?
```

### Step 2: Execute with Verification

You approve, Claude:
1. Renames the file
2. Updates all imports
3. Updates class references
4. Renames the test file
5. Runs tests to verify nothing broke

```
Refactoring complete.

Changes made:
  - Renamed UserService.ts -> AccountService.ts
  - Updated 23 references across 5 files

Test results: 47 passed, 0 failed
```

### Step 3: Record the Decision

```
/learn
```

Claude adds to `decision-log.md`:

```markdown
### DEC-007: Renamed UserService to AccountService
- **Date**: 2024-01-15
- **Reason**: Service handles accounts, not just users
- **Impact**: 5 files, 23 references
- **Verified**: All tests passing
```

---

## Example 5: Debugging with Specifications

**Scenario**: The login feature was working, but now returns wrong error messages.

### Step 1: Debug with Spec Context

```
/spec-debug user-authentication "wrong error messages on login failure"
```

Claude loads the spec and compares:

```
Analyzing: user-authentication spec vs current behavior

Spec says (AC-1):
  "Returns 401 on invalid credentials"

Current behavior:
  Invalid email: Returns 400 "Bad Request"
  Invalid password: Returns 401 "Unauthorized"

Deviation detected: Email validation returns 400 instead of 401

Hypothesis generated:
  H1: Email validation moved to request validation layer (0.70)
      (elevated confidence - spec deviation)
```

### Step 2: Continue with Evidence

```
/evidence H1 "Found Joi validation in routes/auth.ts returning 400" --supports
```

```
H1 confirmed: Joi schema added for email format, returns 400 before auth check

Fix options:
  1. Remove Joi email validation (match spec)
  2. Update spec to allow 400 for malformed emails

Which approach?
```

### Step 3: Document Intentional Deviation

You decide the 400 is actually correct:

```
/spec-deviation user-authentication
```

Claude records in `.specify/deviations/user-authentication/`:

```markdown
# Spec Deviation: AC-1 Error Codes

## Original Spec
Returns 401 on invalid credentials

## Actual Behavior
- Returns 400 for malformed email format
- Returns 401 for valid email with wrong password

## Rationale
400 is more appropriate for malformed input (client error)
401 reserved for authentication failures specifically

## Approved By
Developer decision, 2024-01-15
```

---

## Example 6: Team Knowledge Sharing

**Scenario**: Your team needs to maintain shared knowledge about a complex microservices architecture.

### Step 1: Document Shared Patterns

Team lead runs:
```
/go document the service communication patterns
/learn
```

This creates shared memories about:
- Service discovery patterns
- Circuit breaker configurations
- Event-driven messaging flows

Claude creates `.serena/memories/service-architecture.md`:

```markdown
# Service Architecture

## Communication Patterns
- Sync: REST via API Gateway (Kong)
- Async: RabbitMQ for events
- Service mesh: Istio for internal traffic

## Key Services
- user-service: Authentication, profiles
- order-service: Cart, checkout, history
- payment-service: Stripe integration
- notification-service: Email, SMS, push

## Circuit Breaker Config
- Timeout: 3s for all internal calls
- Retry: 3x with exponential backoff
- Fallback: Cached response when available
```

### Step 2: New Team Member Onboarding

New developer gets instant context:
```
/explore how services communicate
```

Claude loads shared memories and explains:

```
Service Communication Overview (from team memories):

Synchronous (REST):
  Client -> API Gateway (Kong) -> Target Service
  - Auth handled at gateway level
  - Rate limiting: 1000 req/min per user

Asynchronous (Events):
  Producer -> RabbitMQ -> Consumer(s)
  - order.created -> payment-service, notification-service
  - payment.completed -> order-service, notification-service

Key files to understand:
  - src/common/messaging/publisher.ts
  - src/common/http/client.ts (with circuit breaker)
```

### Step 3: Collaborative Debugging

When a cross-service issue occurs:
```
/eliminate "payment service timeouts during checkout"
```

```
Session: elim-2024-01-20-payment-timeout

Hypotheses (informed by service-architecture memory):
  H1: Circuit breaker tripping on payment-service (0.60)
  H2: RabbitMQ queue backlog (0.55)
  H3: Stripe API latency spike (0.50)
  H4: Database connection pool exhaustion (0.45)
```

Team members add evidence from their areas:
```
/evidence H1 "Circuit breaker logs show 0 trips in last hour" --contradicts
/evidence H3 "Stripe dashboard shows 2s avg latency (normal: 200ms)" --supports
```

### Step 4: Knowledge Evolution

After resolution:
```
/learn
```

Claude updates team memories:

```markdown
# Added to debugging-lessons.md

## Payment Timeouts (2024-01-20)
**Symptom**: Checkout failing with payment timeout
**Root Cause**: Stripe API degradation (external)
**Detection**: Check Stripe status page first
**Mitigation**: Increased timeout to 5s, added retry with backoff
```

Now the team has persistent knowledge preventing future confusion.

**Team Memory Conflicts**: If multiple team members update the same memory simultaneously, Claude will show both versions and ask which to keep. Use `/learn` after team discussions to consolidate insights.

---

## Example 7: Migrating from Manual Claude Usage

**Scenario**: You've been using Claude Code manually and want to upgrade to structured workflows.

### Step 1: Install Template

In your existing project:
```
/install
```

Or manually:
```bash
git clone https://github.com/danielcbright/claude-learns.git
cp -r claude-learns/template/.claude ./
cp -r claude-learns/template/.serena ./
cp claude-learns/template/CLAUDE.md ./
```

### Step 2: Import Existing Knowledge

Move your mental model into structured memories:

```
/go create a memory documenting our API design decisions
```

Claude asks clarifying questions and creates:

```markdown
# API Design Decisions

## Versioning
- URL-based: /api/v1/, /api/v2/
- Breaking changes require new version
- Deprecated versions supported for 6 months

## Authentication
- JWT tokens in Authorization header
- Refresh tokens via httpOnly cookies
- API keys for service-to-service

## Response Format
- Always JSON
- Standard envelope: { data, error, meta }
- HTTP status codes match response state
```

```
/go document the database schema patterns
```

### Step 3: Convert Ad-hoc Workflows

Replace manual processes with commands:

**Before (manual):**
> "Debug this issue step by step, check the logs first, then the database, then the code..."

**After (structured):**
```
/eliminate "user registration failures"
```

**Before (manual):**
> "Add this feature carefully, make sure to test it..."

**After (structured):**
```
/spec-create user-profiles
/go implement the user-profiles spec
/spec-verify user-profiles
```

### Step 4: Train the System

Run `/learn` after significant sessions:

```
/learn
```

Claude reviews the session:

```
Session Review:

Insights discovered:
1. The UserRepository uses soft deletes (gotcha)
2. Email validation happens at API gateway level
3. Profile images stored in S3, URLs in database

Recommended memory updates:
1. Add "soft deletes" to database-patterns memory
2. Create new "data-storage" memory for S3 patterns

Shall I create these updates?
```

Approve the updates, and future sessions start with this knowledge.

### Step 5: Gradual Adoption

You don't need everything at once:

| Week 1 | Week 2+ | When Needed |
|--------|---------|-------------|
| `/go` | `/explore` | `/eliminate` |
| `/learn` | `/debug` | `/spec-create` |
| | `/audit` | `/spec-verify` |

Start with `/go` and `/learn`. Add more commands as you encounter situations where they help.

**Rollback Plan**: If you want to return to manual Claude usage, simply delete the added directories:
```bash
rm -rf .claude .serena .elimination .specify CLAUDE.md
```
Your project code remains unchanged.

---

## Key Takeaways

| Scenario | Commands Used | Key Benefit |
|----------|---------------|-------------|
| Complex debugging | `/eliminate`, `/evidence` | Systematic hypothesis tracking |
| New features | `/spec-create`, `/go`, `/spec-verify` | Clear definition of done |
| Understanding code | `/explore`, `/learn` | Persistent knowledge |
| Refactoring | `/refactor`, `/learn` | Safe changes with verification |
| Spec debugging | `/spec-debug`, `/spec-deviation` | Spec as source of truth |
| Team collaboration | `/go`, `/learn`, `/eliminate` | Shared persistent knowledge |
| Manual migration | `/install`, `/go`, `/learn` | Gradual structured adoption |

---

## Next Steps

- [QUICKSTART.md](QUICKSTART.md) - Get set up
- [FAQ.md](FAQ.md) - Common questions
- [README.md](README.md) - Full documentation
