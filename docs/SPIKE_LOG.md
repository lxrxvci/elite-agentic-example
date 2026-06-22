# Architecture Spike Log

*Proposed and completed spikes. Each spike is time-boxed and produces a go/no-go recommendation and a decision record if needed.*

---

## Proposed Spikes

### Spike 1: Payment Provider Integration

**Goal:** Validate that we can embed invoice payments end-to-end with a proven provider, including checkout, webhooks, idempotency, and fee accounting.

- **Time-box:** 3 engineering days
- **Owner:** Tech Lead + Backend Engineer
- **Scope:**
  - Create a test Stripe account and configure webhook endpoints.
  - Implement a minimal invoice → payment-link → webhook → invoice-marked-paid flow.
  - Test duplicate webhook delivery and idempotency handling.
  - Document PCI scope, platform fees, and payout timing.
- **Go criteria:**
  - Payment can be created, completed, and reflected in the invoice state within < 5 seconds of webhook receipt.
  - Duplicate webhooks do not change invoice state or create duplicate records.
  - PCI scope is limited to the provider's hosted fields (SAQ A eligible).
- **No-go criteria:**
  - Webhook delivery is unreliable in test mode, or provider fees make the business model untenable.
  - Idempotency requires more than a simple idempotency-key / state-machine pattern.
- **Decision record:** If accepted, update ADR 0001 with provider choice and create a payment-module design note.

---

### Spike 2: Tenant and Client Data Isolation

**Goal:** Confirm a simple but robust isolation model for freelancer data, client records, and invoice visibility, with a plausible path to future agency/team support.

- **Time-box:** 2 engineering days
- **Owner:** Tech Lead + Backend Engineer + Security Champion
- **Scope:**
  - Model users, freelancers, clients, and invoices with ownership chains.
  - Implement row-level ownership filters and middleware that enforces them.
  - Write integration tests that attempt cross-tenant reads/writes and assert failure.
  - Sketch how a future "agency" tenant could own multiple freelancers without a rewrite.
- **Go criteria:**
  - 100% of cross-tenant access attempts are rejected.
  - Query patterns for the "who owes me" dashboard remain simple and performant.
  - Agency/team expansion can be added by introducing a workspace/organization layer without changing invoice ownership semantics.
- **No-go criteria:**
  - Isolation logic leaks into every query in a way that is easy to forget.
  - Performance degrades significantly with ownership checks on list views.
- **Decision record:** If accepted, codify the isolation pattern in `docs/ARCHITECTURE.md` and add a risk-mitigation note to `TECHNICAL_RISK_REGISTER.md`.

---

### Spike 3: Automated Reminder Deliverability and Tone

**Goal:** Validate that system-owned payment reminders reach client inboxes, support professional tone customization, and comply with email regulations.

- **Time-box:** 2 engineering days
- **Owner:** Tech Lead + Frontend Engineer + Product Strategist
- **Scope:**
  - Evaluate SendGrid vs. Postmark vs. AWS SES for transactional email.
  - Send test reminder emails to major providers (Gmail, Outlook, iCloud) and check placement.
  - Build a small template system with default polite copy and per-freelancer tone overrides.
  - Verify unsubscribe links and sender-domain authentication (SPF/DKIM/DMARC).
- **Go criteria:**
  - Inbox placement rate ≥ 95% in test sends.
  - Default reminder copy passes a UX tone review (professional, not aggressive).
  - Template override system is usable by non-engineers (e.g., via a settings form).
- **No-go criteria:**
  - Emails consistently land in spam/promotions for major providers.
  - Deliverability requires a dedicated IP or complex warmup before MVP launch.
- **Decision record:** If accepted, document provider choice, default templates, and operational monitoring in an ADR or RFC.

---

## Spike Log

| Spike | Status | Result | Decision Record |
|---|---|---|---|
| Payment Provider Integration | Proposed | — | Pending |
| Tenant and Client Data Isolation | Proposed | — | Pending |
| Automated Reminder Deliverability and Tone | Proposed | — | Pending |
