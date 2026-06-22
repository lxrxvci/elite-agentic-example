# Technical Risk Register

*Living document owned by the Tech Lead. Reviewed weekly during shaping and updated after every architecture spike or production incident.*

---

## Risk Summary

| ID | Risk | Area | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|---|---|
| R1 | Payment-provider webhook failures or duplicate events cause invoices to be marked unpaid/paid incorrectly | Payments | High (revenue & trust) | Medium | Idempotent webhook handlers, Stripe signature verification, outbox/event-sourcing pattern for payment state, reconciliation job | Tech Lead |
| R2 | Automated reminder emails land in spam or are blocked, degrading the core "get paid faster" promise | Notifications | High (North Star) | Medium | Dedicated transactional email provider (Postmark/SendGrid), SPF/DKIM/DMARC, domain warmup, unsubscribe compliance, delivery monitoring | Tech Lead |
| R3 | Freelancer A sees freelancer B's clients, invoices, or payment data | Multi-tenancy / Security | Critical | Low | Row-level ownership checks on every query, integration tests for cross-tenant access, least-privilege DB roles, audit logging | Tech Lead |
| R4 | Weak authentication or session handling exposes freelancer or client financial data | Auth | Critical | Medium | OAuth 2.0 / OIDC via proven provider, short-lived tokens, HTTPS-only cookies, rate limiting, dependency scanning | Tech Lead |
| R5 | Tax / invoicing compliance gaps (e.g., VAT, US sales tax, 1099 reporting) create legal exposure | Compliance | High | Medium | Start with jurisdiction-agnostic invoice totals; defer tax calculation to a spike; clearly scope MVP to US-only freelancers; legal review before international launch | Tech Lead |
| R6 | Calendar / project-management integrations break silently, causing missed billable hours | Integrations | Medium | Medium | Abstract integration adapters behind ports, health checks, retry with exponential backoff, degraded-mode UX, user-visible sync status | Tech Lead |
| R7 | Cash-flow dashboard shows stale or inconsistent "who owes what" totals | Data / Analytics | Medium | Low | Single source of truth in PostgreSQL, materialized view or idempotent aggregate job, write-time validation of invoice/payment states | Tech Lead |

---

## Detailed Notes

### R1 — Payment-provider webhook reliability
*Why it matters:* The North Star (Monthly Paid Invoice Value) depends on accurate, timely payment state. A missed or duplicated webhook can make a freelancer think they haven't been paid, or mark an unpaid invoice as paid.
*Trigger for escalation:* More than one payment-state mismatch per 1,000 invoices or any double-payout incident.

### R2 — Email deliverability for payment reminders
*Why it matters:* Opportunity 6 (de-personalized reminders) is a top-shaped bet. If reminders hit spam, the product fails its core promise regardless of UX quality.
*Trigger for escalation:* Delivery rate below 95% or spam-complaint rate above 0.1%.

### R3 — Cross-tenant data leakage
*Why it matters:* Invoices contain sensitive financial and client data. A single leakage incident destroys trust and may violate contractual or regulatory obligations.
*Trigger for escalation:* Any successful cross-tenant read in staging or production.

### R4 — Authentication and authorization vulnerabilities
*Why it matters:* Client portals (invoice recipients) and freelancer dashboards have different privilege models. Blurred boundaries here are a common attack vector.
*Trigger for escalation:* Any auth bypass in pen-test or bug bounty.

### R5 — Tax and invoicing compliance
*Why it matters:* Invoicing software sits adjacent to tax collection and reporting. Getting it wrong exposes both the business and freelancers to penalties.
*Trigger for escalation:* Entering a new jurisdiction or adding automated tax calculation.

### R6 — Third-party integration fragility
*Why it matters:* Strategic Bet 4 ("Capture time where it actually happens") depends on integrations. Silent failures undermine the accuracy that freelancers trust us with.
*Trigger for escalation:* Sync success rate below 99% over 7 days or user-reported missing entries.

### R7 — Cash-flow analytics consistency
*Why it matters:* Opportunity 4 targets cash-flow anxiety. A dashboard that contradicts the invoice list increases rather than reduces uncertainty.
*Trigger for escalation:* Discrepancy between invoice list and aggregate totals exceeding rounding tolerance.
