# RFC 0001: Manual Time Capture & Quick-Entry Widget

**Shaped bet:** [Bet 1 — Capture more billable hours that are currently lost](../SHAPED_BETS.md#bet-1--capture-more-billable-hours-that-are-currently-lost)  
**Status:** Proposed  
**Author:** Tech Lead  
**Review window:** 3 business days

## Summary

This RFC proposes the technical design for Bet 1: a low-friction, global quick-entry widget and live timer that let freelancers capture billable moments before they are forgotten, plus an invoice-creation flow that converts unbilled time entries into invoice line items without retyping. The implementation will be a 2-week MVP built inside the existing modular monolith (Next.js + FastAPI + PostgreSQL) and gated behind feature flags.

## Problem

Freelancers lose small billable increments — micro-tasks, out-of-scope requests, and revision rounds — because they rely on memory and batch reconstruction. The shaped bet identifies three concrete failure modes:

- **Forgotten micro-tasks:** 20-minute fixes and ad-hoc requests are gone by invoicing day.
- **Lost revision hours:** Back-and-forth in Slack/email is rarely logged.
- **Evening admin debt:** Reconstructing a week of work increases anxiety and under-billing.

The result is lower invoice value, cash-flow uncertainty, and churn risk for a product whose North Star is Monthly Paid Invoice Value.

## Proposed solution

### User-facing behavior

1. **Global quick-entry widget**
   - Triggered by `Cmd/Ctrl + Shift + T` and a persistent nav button.
   - Fields: client, project, description, duration OR start/end time.
   - Defaults to the most recently used client/project (stored per tenant).
   - Target: log a manual entry in under 10 seconds.

2. **Live timer**
   - One-click start/stop with a floating, always-visible indicator.
   - On stop, pre-fills the quick-entry form with the elapsed duration rounded to the nearest 15 minutes.
   - Timer state is local to the browser session; on stop it becomes a normal time entry.

3. **Unbilled signal**
   - Each unbilled entry gets an `Unbilled` badge.
   - Dashboard shows weekly unbilled-hours summary.
   - Invoice creation screen pre-groups unbilled entries by client/project.

4. **Invoice-from-time flow**
   - User selects unbilled entries; system generates a draft invoice grouped by client/project.
   - Selected entries are atomically marked as `billed` and linked to the invoice.
   - Single default hourly rate per tenant for this bet; per-project rates are out of scope.

### Backend architecture

We extend the modular monolith defined in [ADR 0002](../adr/0002-domain-boundaries.md) with two new bounded contexts for this bet:

- **Time Tracking** owns `TimeEntry` and rounding rules.
- **Invoicing** owns `Invoice`, `InvoiceLineItem`, and status transitions.
- **Client & Project Directory** provides master data used by both contexts.
- **Identity & Tenant** resolves the authenticated freelancer and tenant boundary.

Cross-context rules:

- Time Tracking never reads invoice tables.
- Invoicing reads unbilled time entries through a typed internal port and marks them billed in the same transaction that creates the invoice.
- All queries are scoped by `tenant_id`.

### Data model (MVP)

```text
TimeEntry
  id UUID PK
  tenant_id UUID FK -> Tenant
  client_id UUID FK -> Client
  project_id UUID FK -> Project
  description TEXT
  duration_minutes INT           -- raw logged duration
  rounded_minutes INT            -- rounded per tenant default (15 min)
  started_at TIMESTAMPTZ NULL
  ended_at TIMESTAMPTZ NULL
  status ENUM('unbilled','billed','written_off')
  invoice_id UUID FK -> Invoice NULL
  created_at / updated_at

Invoice
  id UUID PK
  tenant_id UUID FK -> Tenant
  client_id UUID FK -> Client
  status ENUM('draft','sent','paid','overdue','cancelled')
  issue_date DATE
  due_date DATE
  subtotal DECIMAL
  total DECIMAL
  notes TEXT
  created_at / updated_at

InvoiceLineItem
  id UUID PK
  invoice_id FK -> Invoice
  description TEXT
  quantity DECIMAL (hours)
  rate DECIMAL
  amount DECIMAL
  time_entry_ids UUID[]          -- immutable audit link
```

### API contract

The public REST API is defined in [`openapi.yaml`](../../openapi.yaml). Key surfaces:

- `GET /me` — current user/tenant context.
- `GET /clients`, `GET /projects` — master data for the quick-entry widget.
- `POST /time-entries`, `GET /time-entries`, `PATCH /time-entries/{id}` — capture and manage time.
- `POST /invoices` — create a draft invoice from a list of unbilled time entries.
- `GET /invoices`, `GET /invoices/{id}`, `POST /invoices/{id}/mark-paid` — invoice lifecycle.

All error responses follow RFC 9457 Problem Details.

### Frontend notes

- Use the existing design-system tokens for the modal and timer indicator.
- Timer state persists in `sessionStorage`/`IndexedDB` to survive accidental refreshes; the canonical time entry is only created when the user confirms stop.
- Quick-entry modal is a React Server Component wrapper with a client-side form for instant interactivity.

## Alternatives considered

| Alternative | Trade-off | Decision |
|---|---|---|
| Keep timer state server-side with a heartbeat | More resilient to browser crashes, but adds real-time sync complexity and is overkill while multi-device is a no-go. | Rejected for MVP; revisit if timer reliability becomes an issue. |
| Auto-create invoice line items at time-entry save | Would force users into a rigid billing model and prevent batching/review. | Rejected; keep entries unbilled until the freelancer explicitly invoices. |
| Separate time-tracking microservice | Would let that context scale independently, but adds network, deployment, and transactional complexity with no evidence of need. | Rejected per "modular monolith by default." |
| Build generic activity/screen tracking | Could capture more hours, but violates the shaped-bet no-gos and would destroy freelancer trust. | Rejected. |
| Per-project hourly rates now | Useful later, but expands the bet into pricing configuration. | Rejected; single default rate for MVP. |

## Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Cross-tenant data leakage | Critical | Every repository query filters by `tenant_id`. Add integration tests that assert tenant isolation for time entries and invoices. |
| Timer state lost on refresh/tab close | Medium | Persist timer start timestamp in `sessionStorage`/`IndexedDB`; on recovery, show elapsed time and let the user resume or discard. |
| Scope creep into rates, retainers, or integrations | High (timeline) | Enforce the shaped-bet no-gos; use a feature flag for anything beyond the 2-week appetite. |
| Duplicate invoices created from the same time entries | High (revenue accuracy) | Invoice creation is transactional and marks entries `billed`; use an idempotency key on `POST /invoices` for retry safety. |
| Low adoption due to hidden widget | Medium | Onboarding tooltip, keyboard shortcut hint in nav, and default-to-MRU client/project reduce friction. |
| Invoice creation time increases because of extra data | Medium | Pre-group unbilled entries by client/project and auto-fill defaults; measure end-to-end time in acceptance tests. |

## Rollback plan

- **Feature flags:** Quick-entry widget and live timer are each behind a launch flag (`time-capture.quick-entry`, `time-capture.live-timer`). Disabling a flag immediately removes the UI without a deploy.
- **Database migrations are additive only.** New tables (`time_entries`, `invoices`, `invoice_line_items`) and the `status` column on future iterations do not mutate existing `users` data. If the bet fails, we can hide the features and archive rows; no destructive rollback is required.
- **API versioning:** New endpoints are added under `/api/v1`. If we need to redesign, we can introduce `/api/v2` while keeping v1 stable for any active clients.

## Dependencies

| Dependency | Owner | Notes |
|---|---|---|
| ADR 0002 — Domain boundaries | Tech Lead | Defines the modular monolith packages this RFC will populate. |
| Identity / tenant resolution | Backend / Security | `GET /me` and all repository methods need a stable `tenant_id` from auth. |
| Clients & projects master data | Backend + UX | Quick-entry needs read endpoints and seed data for onboarding. |
| Design-system modal + button tokens | UX / Frontend | Reuse existing tokens; no new components required. |
| Acceptance-test environment | DevOps/SRE | Needed for the 10-second capture success criterion and tenant-isolation tests. |

## Timeline

**Appetite: 2 weeks.**

- **Day 1–2:** RFC/ADR review, finalize `openapi.yaml`, create migrations.
- **Day 3–5:** Implement `TimeEntry` domain + API + quick-entry UI.
- **Day 6–8:** Implement live timer (client-side), unbilled dashboard badges, and MRU defaults.
- **Day 9–10:** Implement invoice creation from unbilled entries, mark-paid flow, and PDF/email stub (send action updates status).
- **Day 11+:** Integration/tenant-isolation tests, staging sign-off, feature-flag enablement.
