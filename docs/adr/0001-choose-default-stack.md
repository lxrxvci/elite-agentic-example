# ADR 0001: Choose Default Application Stack

## Status

- Accepted

## Context

The product is a freelancer SaaS dashboard that turns logged time into paid invoices faster. The initial shaped bets depend on three capabilities working reliably together: time capture, invoice generation, and payment follow-up. We need a default stack before the first engineering cycle so that the squad can build a modular monolith with strong type safety, a shared API contract, and a deployment pipeline that supports DORA-aligned practices.

The research report on elite SDLC methodologies emphasizes four themes that should govern this decision:

1. **Choose Boring Technology** — spend innovation tokens deliberately on differentiators, not on infrastructure that has mature, well-understood solutions.
2. **Modular monolith by default** — start simple and evolve based on evidence; microservices are a scaling option, not a starting point.
3. **Cognitive load reduction** — the stack should let a small stream-aligned team own the full lifecycle without mastering too many runtime models, deployment patterns, or languages.
4. **DORA-aligned practices** — trunk-based development, automated testing, fast feedback loops, and small, safe deploys should be easy to adopt from day one.

## Decision

Adopt the following default stack for the MVP and the foreseeable future:

| Layer | Choice |
|---|---|
| Frontend | TypeScript + Next.js 15 (App Router) |
| Backend API | Python + FastAPI |
| Database | PostgreSQL |
| ORM / Migrations | SQLAlchemy 2.0 + Alembic |
| API Contracts | OpenAPI generated from FastAPI Pydantic models |
| Styling | Tailwind CSS + design-system tokens |
| Testing | Vitest (frontend), pytest + pytest-asyncio (backend) |
| Deployment target | Containerized workload (Docker) on a managed platform |

We will build a **modular monolith**: a single deployable backend with clearly bounded internal modules (users, clients, time-entries, invoices, payments, reminders, reports). Each module owns its domain logic and exposes an internal interface; cross-module calls go through typed ports rather than direct database access.

## Consequences

### Positive

- **Cognitive load stays low.** The squad uses two mainstream, statically typed languages (TypeScript for the frontend, Python for the backend) with large talent pools and mature ecosystems. No engineer needs to reason about distributed tracing, service meshes, or inter-service contracts in the MVP.
- **"Boring" choices reduce risk.** PostgreSQL is the most widely used and admired relational database; Next.js is the dominant React framework with first-class deployment tooling; FastAPI is a proven, high-performance Python API framework. These are all well-understood, well-supported choices.
- **OpenAPI-first is natural.** FastAPI emits an OpenAPI schema from Pydantic models, which the frontend can consume for type generation and contract tests. This decouples frontend and backend deploys and supports parallel work.
- **DORA practices are easy to adopt.** A single repository, single deployable artifact, and comprehensive automated tests enable trunk-based development, small PRs, and multiple deploys per day with low change-failure risk.
- **The modular monolith preserves optionality.** If a domain (e.g., payments or reminders) later needs independent scaling or a different runtime, we can extract it into a service because boundaries are explicit from the start.

### Negative

- **Two languages instead of one** increases context switching slightly. We mitigate this by keeping each language in a clear layer (UI vs. API/domain) and using TypeScript-style strict typing on both sides.
- **Next.js App Router and React Server Components** are newer patterns that carry some learning curve. The trade-off is accepted because they reduce client-side complexity and improve performance for a dashboard-heavy product.
- **PostgreSQL will be the single source of truth for analytics.** For very large freelance practices this may eventually require read replicas or an analytical store, but that is a future concern.

## Alternatives considered

### Single-language stack (Next.js full-stack with tRPC or Next.js API routes)
- *Rejected:* A single language would lower cognitive load further, but Python's ecosystem for long-running background jobs, invoice/PDF generation, payment webhooks, and financial calculations is stronger. Keeping the backend in Python also makes future extraction of domains into services easier.

### Microservices from the start
- *Rejected:* The research report and our own rules state "modular monolith by default; microservices only with evidence." We have no evidence of scaling constraints, and the team size is small. Microservices would add network, deployment, and debugging complexity without clear benefit.

### Serverless-first (e.g., AWS Lambda + DynamoDB)
- *Rejected:* Serverless can reduce operational load, but it introduces cold-start latency, complex local development, and a NoSQL data model that is harder to evolve for relational invoicing data. The Prime Video case study in the research report (90% cost reduction by moving from serverless microservices to a monolith) is a cautionary signal.

### A different database (e.g., MySQL or a document store)
- *Rejected:* PostgreSQL is explicitly called out in the research report as the consensus default database. Its JSONB support also gives us flexibility for less-structured data without abandoning relational integrity.

## Related

- `docs/SPIKE_LOG.md` — payment-provider and tenant-isolation spikes will validate parts of this stack.
- `docs/TECHNICAL_RISK_REGISTER.md` — risks R1, R3, R4, and R7 are mitigated by this stack choice.
- `ROADMAP.md` — "Now" milestones assume this stack.
