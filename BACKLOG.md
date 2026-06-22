# Product Backlog

*Prioritized backlog for the freelancer time-to-payment dashboard. Derived from the [Product Strategy](./PRODUCT_STRATEGY.md), [Roadmap](./ROADMAP.md), and [Opportunity Solution Tree](./DISCOVERY/OST.md).*

## How we prioritize

- **Scoring:** RICE = Reach × Impact × Confidence / Effort  
  - Reach = 5 (all active freelancers), 4 (most), 3 (some)
  - Impact = 3 (high North-Star leverage), 2 (medium), 1 (low)
  - Confidence = 1.0 (High), 0.8 (Medium-High), 0.5 (Medium)
  - Effort = 1 (S / ≤1 week), 2 (M / 1–2 weeks), 3 (L / >2 weeks)
- **Priority label:** Must / Should / Could — mapped from RICE rank and strategic dependency.
- **Definition of Done (shared):**
  - [ ] Code implemented behind a feature flag where appropriate
  - [ ] Unit/integration tests with diff coverage ≥ 80%
  - [ ] Code reviewed and CI passing
  - [ ] Acceptance criteria verified in a staging environment
  - [ ] Product/UX sign-off and docs updated

---

## Summary

| Rank | Initiative | OST Opportunity | Priority | Size | RICE |
|---|---|---|---|---|---|
| 1 | [Quick invoice creation from unbilled hours](#1-quick-invoice-creation-from-unbilled-hours) | Opp 1 | Must | S | 15 |
| 2 | [One-click time capture for micro-tasks](#2-one-click-time-capture-for-micro-tasks-and-out-of-scope-work) | Opp 3 | Must | S | 10 |
| 3 | ["Who owes me" dashboard](#3-who-owes-me-dashboard) | Opp 4 | Must | S | 10 |
| 4 | [Invoice payment-status timeline](#4-invoice-payment-status-timeline) | Opp 2 | Should | S | 8 |
| 5 | [System-owned payment reminders](#5-system-owned-automated-payment-reminders) | Opp 2 / Opp 6 | Should | M | 6 |
| 6 | [Late-fee and net-terms configuration](#6-late-fee-and-net-terms-configuration) | Opp 2 | Could | S | 4 |
| 7 | [Stripe embedded checkout](#7-stripe-embedded-checkout) | Opp 5 | Could | L | 2 |

---

## 1. Quick invoice creation from unbilled hours

**Outcome:** A freelancer can generate and send an accurate invoice in under 60 seconds.

- **Priority:** Must
- **Size / appetite:** S — time-box to 1 cycle week
- **RICE score:** 15 (Reach 5 × Impact 3 × Conf 1.0 / Effort 1)
- **Link to OST:** [Opportunity 1 — Reduce the time and effort to create an invoice](./DISCOVERY/OST.md#1-reduce-the-time-and-effort-to-create-an-invoice)

### Acceptance criteria
- [ ] User can select unbilled time entries grouped by client and project and generate a draft invoice in ≤3 clicks.
- [ ] Default invoice template renders line items, subtotal, tax (if set), total, due date, and payment instructions as a PDF.
- [ ] Invoice can be sent to the client email from the dashboard and its status updates to `sent`.

---

## 2. One-click time capture for micro-tasks and out-of-scope work

**Outcome:** Freelancers capture billable minutes as they happen instead of reconstructing them later.

- **Priority:** Must
- **Size / appetite:** S — time-box to 1 cycle week
- **RICE score:** 10 (Reach 5 × Impact 2 × Conf 1.0 / Effort 1)
- **Link to OST:** [Opportunity 3 — Capture more billable hours that are currently lost](./DISCOVERY/OST.md#3-capture-more-billable-hours-that-are-currently-lost)

### Acceptance criteria
- [ ] User can start a live timer or log a manual entry (client, project, duration, note) in under 10 seconds.
- [ ] Unbilled entries surface a visible badge and aggregate by client/project for invoice creation.
- [ ] Quick-entry widget is reachable from any page via a keyboard shortcut and from the main nav.

---

## 3. "Who owes me" dashboard

**Outcome:** Freelancers log in and immediately see what money is outstanding and for how long.

- **Priority:** Must
- **Size / appetite:** S — time-box to 1 cycle week
- **RICE score:** 10 (Reach 5 × Impact 2 × Conf 1.0 / Effort 1)
- **Link to OST:** [Opportunity 4 — Increase confidence in who owes what and when](./DISCOVERY/OST.md#4-increase-confidence-in-who-owes-what-and-when)

### Acceptance criteria
- [ ] Dashboard lists all outstanding invoices sorted by urgency (due date / days overdue), showing client, amount, and status.
- [ ] Aggregates total outstanding and per-client totals update within one minute of payment or invoice changes.
- [ ] Provides a one-click action to view the invoice, send a reminder, or record an offline payment.

---

## 4. Invoice payment-status timeline

**Outcome:** Freelancers stop guessing whether a client has seen or is about to pay an invoice.

- **Priority:** Should
- **Size / appetite:** S — time-box to 3–4 days
- **RICE score:** 8 (Reach 5 × Impact 2 × Conf 0.8 / Effort 1)
- **Link to OST:** [Opportunity 2 — Reduce days between invoice sent and payment received](./DISCOVERY/OST.md#2-reduce-days-between-invoice-sent-and-payment-received)

### Acceptance criteria
- [ ] Every sent invoice shows a chronological status: `sent`, `viewed`, `paid`, `overdue` with timestamps.
- [ ] `viewed` status is captured by a lightweight email tracking pixel with acknowledged limitations.
- [ ] `paid` status can be updated automatically via webhook or manually by the freelancer.

---

## 5. System-owned automated payment reminders

**Outcome:** Overdue invoices are followed up automatically, giving freelancers emotional cover and shortening time-to-payment.

- **Priority:** Should
- **Size / appetite:** M — time-box to 2 cycle weeks
- **RICE score:** 6 (Reach 5 × Impact 3 × Conf 0.8 / Effort 2)
- **Link to OST:** [Opportunity 2 — Reduce days between invoice sent and payment received](./DISCOVERY/OST.md#2-reduce-days-between-invoice-sent-and-payment-received) and [Opportunity 6 — De-personalize payment reminders](./DISCOVERY/OST.md#6-de-personalize-payment-reminders-while-preserving-the-client-relationship-emerged-from-synthesis)

### Acceptance criteria
- [ ] System sends up to three polite, product-branded reminders per invoice (3 days before due, on due date, 7 days after).
- [ ] Freelancer can enable/disable reminders per invoice and preview the message before the first send.
- [ ] Reminder sender address is product-owned; replies/bounces are tracked and surfaced to the freelancer.

---

## 6. Late-fee and net-terms configuration

**Outcome:** Payment terms are explicit on every invoice, creating urgency without awkward freelancer negotiation.

- **Priority:** Could
- **Size / appetite:** S — time-box to 2–3 days
- **RICE score:** 4 (Reach 4 × Impact 2 × Conf 0.5 / Effort 1)
- **Link to OST:** [Opportunity 2 — Reduce days between invoice sent and payment received](./DISCOVERY/OST.md#2-reduce-days-between-invoice-sent-and-payment-received)

### Acceptance criteria
- [ ] User can set a default net-terms value and optional late-fee percentage at the client or invoice level.
- [ ] Terms and late-fee line item appear clearly on the invoice PDF and client email.
- [ ] Late fees are calculated automatically when a reissued/overdue invoice is generated.

---

## 7. Stripe embedded checkout

**Outcome:** Clients can pay an invoice instantly without leaving the invoice experience.

- **Priority:** Could
- **Size / appetite:** L — spike first; full build likely 1+ cycles
- **RICE score:** 2 (Reach 4 × Impact 3 × Conf 0.5 / Effort 3)
- **Link to OST:** [Opportunity 5 — Reduce the friction of accepting payments inside the product](./DISCOVERY/OST.md#5-reduce-the-friction-of-accepting-payments-inside-the-product)

### Acceptance criteria
- [ ] Client receives a secure payment link in the invoice email and can pay by card via Stripe Checkout or Elements.
- [ ] Webhook updates the invoice status to `paid`, records the Stripe fee, and exposes payout reference to the freelancer.
- [ ] No card data is stored in our systems; PCI scope is minimized by using Stripe-hosted components.

---

## Deferred / pruned

- Calendar/project-management integrations for ambient time capture (Opp 3) — valuable but depends on core timer behavior; revisit after Opp 2/3 are validated.
- Expense/reimbursement tracking — Later roadmap item, not validated by current discovery.
- Proposals/contracts/e-signatures — Later roadmap item, not in scope for current cycle.
