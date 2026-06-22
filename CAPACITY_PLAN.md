# 2-Week Capacity Plan

*5-engineer squad, 2-week cycle. Capacity allocation follows the 55–70% features / 15–20% debt / 10–15% bugs / 10–15% buffer rule.*

## Assumptions

- Squad size: **5 engineers**
- Cycle length: **2 weeks** (10 working days)
- Total engineering capacity: **50 engineer-days** (5 × 10)
- Overhead (stand-ups, planning, 1:1s) is absorbed by the buffer bucket and the feature appetite time-boxes.

## Capacity envelope

| Bucket | Allocation | Engineer-Days | Purpose |
|---|---:|---:|---|
| **Features** | 60% | 30 | Deliver validated backlog items that move the North Star (MPIV). |
| **Tech Debt** | 16% | 8 | Keep the codebase deployable, observable, and safe to change. |
| **Bugs** | 12% | 6 | Fix production defects that hurt activation or trust. |
| **Buffer** | 12% | 6 | Unplanned work, incidents, stakeholder requests, and cycle carry-over. |
| **Total** | 100% | **50** |  |

## Feature allocation

| Backlog Item | Appetite | Eng-Days | % of Feature Bucket |
|---|---|---:|---:|
| B1 — Quick invoice creation from unbilled hours | S | 8 | 27% |
| B2 — One-click time capture for micro-tasks | S | 6 | 20% |
| B3 — "Who owes me" dashboard | S | 6 | 20% |
| B4 — Invoice payment-status timeline | S | 4 | 13% |
| B5 — System-owned automated payment reminders | M | 4 | 13% |
| B6 — Late-fee and net-terms configuration (stretch) | S | 2 | 7% |
| **Feature subtotal** |  | **30** | **100%** |

## Debt, bugs, and buffer

### Tech debt (8 days)
- Increase test coverage for the authentication and invoice PDF paths to ≥ 80%.
- Document the public invoice/time-entry API contract.
- Refactor the invoice status state machine so `draft` → `sent` → `viewed` → `paid`/`overdue` is explicit and tested.
- Add database indexing strategy for the "who owes me" aggregate query.

### Bugs (6 days)
- Invoice PDF wraps line items incorrectly on long descriptions.
- Live timer continues counting after browser tab is backgrounded for > 30 minutes.
- Login redirect loses the intended invoice context for unauthenticated users.

### Buffer (6 days)
- Unplanned production incidents.
- Urgent stakeholder clarifications on invoice template branding.
- Scope negotiation if reminder spike reveals deliverability risks.

## WIP limits

Keep flow visible and protect throughput:

- **Discovery/Ready:** max 3 items
- **In Development:** max 2 items
- **In Review/QA:** max 2 items
- **Waiting for deploy:** max 1 item

## Cycle commitments

1. Ship B1, B2, and B3 to production or behind feature flags by end of Week 1.
2. Complete B4 and start B5 in Week 2; B5 may require a deliverability spike that rolls into the next cycle.
3. B6 is a stretch goal and is only started if B1–B4 are merged and stable.
4. Protect 6 days of buffer; do not pre-fill it with lower-priority feature work.
