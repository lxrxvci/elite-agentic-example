# Shaped Bets

*Rough-but-bounded solutions for the top validated opportunities from the [Opportunity Solution Tree](../DISCOVERY/OST.md). Shaped using the [Shaping & Betting workflow](../../pipeline/workflows/shaping.md).*

---

## Bet 1 — Capture more billable hours that are currently lost

**OST opportunity:** [Opportunity 3 — Capture more billable hours that are currently lost](../DISCOVERY/OST.md#3-capture-more-billable-hours-that-are-currently-lost)  
**Decision:** **Bet** — build in the next cycle.  
**Feasibility note:** Core manual capture is low risk; integrations are explicitly out of this bet.

### Problem

Freelancers lose small billable increments — micro-tasks, out-of-scope requests, and revision rounds — because they rely on memory and batch reconstruction. I2 forgets "the 20-minute fixes I did on Tuesday"; Diego loses revision hours in Slack; Maya forgets micro-tasks by the time she invoices. The result is lower invoice value, under-billing anxiety, and more evening admin.

### Appetite

**2 weeks** for the MVP of manual quick-entry + a basic live timer. We are not trying to build an all-in-one time-tracking platform; we are removing the friction of capturing a billable moment before it is forgotten.

### Solution sketch

1. **Global quick-entry widget**
   - Accessible from any page via a keyboard shortcut (e.g., `Cmd/Ctrl + Shift + T`) and a persistent nav button.
   - Fields: client, project, description, duration OR start/stop timer.
   - Default to the most recently used client/project to reduce typing.

2. **Live timer**
   - One-click start/stop with a visible floating indicator.
   - On stop, pre-fills the quick-entry form so the user can add a description and save.
   - Round to the nearest 15 minutes by default; allow per-project rounding override later.

3. **Unbilled signal**
   - Each unbilled entry gets an "Unbilled" badge.
   - Dashboard shows a weekly unbilled-hours summary.
   - Invoice creation screen pre-groups unbilled entries by client/project.

4. **Weekly nudge (optional if time allows)**
   - Friday afternoon email/sidebar reminder listing unbilled entries from the week.

### Rabbit holes

- **Billing-rate management** — per-project or per-client rates are useful but can expand into pricing configuration. Keep a single default rate for now.
- **Idle detection / screenshots** — invasive tracking would destroy trust. Avoid entirely.
- **Multi-device sync** — out of scope; timer lives in the active browser session.
- **Timer precision disputes** — round to 15 minutes; do not expose raw seconds.
- **Calendar/project integrations** — these are promising but a separate spike once the core loop is proven.

### No-gos

- No calendar scraping or project-management integrations in this bet.
- No automated activity detection or desktop agent.
- No mobile native app or offline support.
- No retainer/contract time budgets.

### Success criteria

- [ ] A user can log a manual time entry in under 10 seconds.
- [ ] At least 60% of active users log at least one time entry within 7 days of signup.
- [ ] Unbilled hours are visible and can be converted into invoice line items without retyping.
- [ ] Invoice creation time does not increase because of extra time-entry data.

### Hand-off

If approved at the betting table, hand off to the RFC/ADR workflow to define the data model (time entries, projects, clients), API contract, and frontend state for the timer.

---

## Bet 2 — Reduce days between invoice sent and payment received

**OST opportunity:** [Opportunity 2 — Reduce days between invoice sent and payment received](../DISCOVERY/OST.md#2-reduce-days-between-invoice-sent-and-payment-received)  
**Decision:** **Spike first, then build** — run a focused 1-week spike on email deliverability and payment-status tracking before committing the full build.  
**Feasibility note:** The outcome depends on payment-provider webhooks and reminder deliverability. The spike de-risks the bounded build described below.

### Problem

Freelancers wait weeks or months to be paid because chasing feels personal and emotionally costly. I1 let an $8,000 invoice go 60 days overdue out of embarrassment; I2 distrusts read-receipt ambiguity; I3 wants system-owned reminders so she can "blame the system." Existing tools either provide no follow-up help or make the freelancer own the awkwardness.

### Appetite

**2 weeks** for the bounded build after the spike: automated system-owned reminders + a payment-status timeline. Embedded checkout is intentionally excluded.

### Solution sketch

1. **Payment-status timeline on every invoice**
   - States: `draft` → `sent` → `viewed` → `paid` / `overdue`.
   - `viewed` captured by a lightweight tracking pixel with a tooltip explaining it is an estimate.
   - Manual "record payment" action for offline methods (bank transfer, Venmo, Zelle).

2. **System-owned reminder schedule**
   - Up to three reminders: 3 days before due date, on the due date, and 7 days after.
   - Sender is a product-owned address (e.g., `reminders@product.com`) with the freelancer's branding in the body.
   - Tone is polite, professional, and concise; no guilt language.

3. **Freelancer controls**
   - Enable/disable reminders per invoice.
   - Preview the first reminder before it is sent.
   - One-click "send now" override.

4. **Delivery health**
   - Track bounces, spam complaints, and unsubscribes.
   - Surface delivery failures in the dashboard so the freelancer can follow up directly.

### Rabbit holes

- **Email deliverability** — a new domain can land in spam. The spike must validate inbox placement with major providers.
- **Reliable "viewed" detection** — open pixels are imperfect. We should expose uncertainty rather than over-promise.
- **Template customization** — freelancers will want to tweak tone. A full template editor is a separate feature; start with one well-written default.
- **Compliance** — CAN-SPAM, GDPR, and unsubscribe requirements for automated emails.
- **Time zones and due-date arithmetic** — due dates must be unambiguous.

### No-gos

- No embedded payment processing in this bet (Stripe checkout is a later initiative).
- No custom reminder schedules per client (fixed schedule only).
- No SMS, postal, or phone reminders.
- No multi-currency late-fee calculations.
- No automated collections agency or legal escalation language.

### Success criteria

- [ ] Reminders are sent automatically for 100% of invoices with due dates and reminders enabled.
- [ ] Median time-to-payment for invoices with reminders is reduced by at least 15% within 4 weeks of release.
- [ ] Freelancers can see the payment-status timeline for every sent invoice.
- [ ] Reminder bounce/complaint rate stays below 5%.

### Hand-off

If the spike confirms deliverability and webhook viability, hand off to the RFC/ADR workflow to design the email pipeline, event store for invoice status transitions, and integration with the existing invoice model.

---

## Betting-table summary

| Bet | Opportunity | Decision | Cycle appetite | North-Star lever |
|---|---|---|---|---|
| 1 | Capture more billable hours | Build | 2 weeks | Increases invoice value (AIV) |
| 2 | Reduce days to payment | Spike, then build | 1-week spike + 2-week build | Shortens time-to-payment (MTP) |
