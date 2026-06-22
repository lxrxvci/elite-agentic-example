# ADR 0002: Domain Boundaries and Modular Monolith Structure

## Status

- Proposed

## Context

The freelancer SaaS dashboard has three core jobs: capture billable time, turn that time into invoices, and get those invoices paid. Without explicit boundaries, these concerns quickly collapse into a single CRUD layer, making it hard to test, reason about, or later extract into independently deployable services.

Bet 1 adds the first cross-domain flow: a time entry created in Time Tracking must become a line item in Invoicing, and its status must flip from `unbilled` to `billed` atomically. We need to decide where each concept lives, how modules communicate, and how we keep the system a single deployable artifact while preserving optionality.

## Decision

We will build a **modular monolith** with the following bounded contexts. Each context is a top-level Python package in the FastAPI backend with its own domain models, service layer, repository interface, and public internal ports. No module may query another module's tables directly.

### Bounded contexts

| Context | Responsibilities | Owns |
|---|---|---|
| **Identity & Access Management (IAM)** | Authentication, session/tokens, tenant resolution, user profiles. | `User`, `Tenant`, `Session` |
| **Client & Project Directory** | Master data about the freelancer's clients, projects, contacts, and default billing settings. | `Client`, `Project`, `Contact` |
| **Time Tracking** | Capturing, rounding, and querying billable time; timer session metadata. | `TimeEntry`, `RoundingRule` |
| **Invoicing** | Drafting, sending, and versioning invoices; grouping entries into line items; status transitions. | `Invoice`, `InvoiceLineItem`, `InvoiceStatus` |
| **Payments** | Recording payments, reconciling provider webhooks, and updating invoice paid status. | `Payment`, `PaymentMethod`, `ReconciliationEvent` |
| **Notifications** | Sending transactional emails (invoice sent, reminders, payment confirmations) and tracking delivery. | `Notification`, `EmailDeliveryEvent` |
| **Reporting** | Read-only aggregates for dashboards: unbilled hours, outstanding invoices, cash-flow summaries. | Materialized views / query handlers |

### Module interaction rules

1. **No direct database access across contexts.** If Invoicing needs unbilled entries, it calls the Time Tracking port, not the `time_entries` table.
2. **Cross-context writes are transactional where consistency matters.** Creating an invoice from time entries uses a local transaction in the Invoicing module that invokes Time Tracking's "mark billed" port; if either side fails, the transaction rolls back.
3. **Less critical updates are event-driven.** Payments publishes `PaymentReceived`; Notifications and Reporting subscribe without blocking the payment transaction.
4. **Shared kernel is minimal.** Only generic primitives cross contexts: `tenant_id`, `UTC` timestamps, and a `Money` value object (amount + currency). Everything else is context-owned.
5. **Frontend consumes a single public REST API.** Internal module boundaries are not exposed as separate services.

### Physical structure

```text
src/backend/app/
├── main.py                    # FastAPI app composition, middleware, routers
├── shared/                    # shared kernel (tenant_id, money, exceptions)
├── iam/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interfaces/
├── directory/                 # clients & projects
├── time_tracking/
├── invoicing/
├── payments/
├── notifications/
└── reporting/
```

Each module follows Clean/Hexagonal layering:

- `domain/` — entities, value objects, domain events, invariants.
- `application/` — use-case services and ports (abstract interfaces).
- `infrastructure/` — SQLAlchemy repositories, HTTP clients, external adapters.
- `interfaces/` — FastAPI routers / internal module facades.

## Consequences

### Positive

- **Clear ownership.** Each bet can add or change one module without spilling into unrelated code.
- **Testability.** Domain logic has no framework or database dependencies; ports are mocked in unit tests.
- **Optionality preserved.** If Payments or Notifications later need independent scaling, they can be extracted because their public ports are already explicit.
- **Tenant isolation is centralized.** IAM resolves `tenant_id`; every repository enforces it, reducing the surface area for cross-tenant bugs.

### Negative

- **Initial package overhead.** A small team must maintain directory structure and import discipline.
- **Refactoring cost if boundaries are wrong.** We accept this risk and will revisit boundaries at the end of each cycle.
- **Shared kernel evolution needs coordination.** Changes to `Money` or timestamp handling affect all modules and require a brief RFC.

## Alternatives considered

### Microservices from the start
- *Rejected:* We have no scaling, team-size, or deployment-velocity evidence that justifies the operational complexity of inter-service networking, distributed transactions, and observability. The shaped bet explicitly targets a 2-week MVP.

### Anemic layered architecture (controllers → services → repositories without bounded contexts)
- *Rejected:* Would ship faster on day one, but would create a "big ball of mud" as soon as Invoicing needs to touch Time Tracking data. Bounded contexts keep the cost of change low.

### Vertical slice architecture by feature instead of domain
- *Rejected:* Vertical slices work well for small CRUD features, but they blur long-lived domain concepts. `Invoice` and `Payment` appear in multiple bets; a domain-oriented cut is more stable.

## Related

- [ADR 0001: Choose Default Application Stack](0001-choose-default-stack.md)
- [RFC 0001: Manual Time Capture & Quick-Entry Widget](../rfc/0001-first-bet.md)
- [`openapi.yaml`](../../openapi.yaml)
- [`docs/DEPENDENCY_MAP.md`](../DEPENDENCY_MAP.md)
