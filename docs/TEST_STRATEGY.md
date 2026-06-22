# Test Strategy

## Philosophy

Quality is owned by the stream-aligned squad. Tests are written close to the code they validate, run in CI on every commit, and provide fast feedback. We avoid separate QA gatekeeping; instead, QA Enablement provides standards, templates, and tooling.

## Testing Pyramid

```
        ┌─────────┐
        │   E2E   │  ← Playwright: critical user journeys
        │  ~5%    │
       ├───────────┤
       │ Integration│ ← API tests, repository tests
       │   ~15%    │
      ├─────────────┤
      │    Unit      │ ← pytest / Vitest: domain logic, components
      │    ~80%     │
      └─────────────┘
```

## Test Types

### Unit Tests

| Layer | Tool | Scope | Gate |
|---|---|---|---|
| Backend | pytest | Domain services, use cases, utility functions | ≥ 80% coverage |
| Frontend | Vitest | Pure functions, hooks, presentational components | ≥ 70% coverage |

### Integration Tests

| Layer | Tool | Scope | Gate |
|---|---|---|---|
| Backend API | pytest + TestClient | Router endpoints with test DB | Run on every PR |
| Database | pytest + Alembic | Migrations up/down | Run on every PR |
| Contracts | Pact | Consumer/provider API contracts | Run on every PR |

### End-to-End Tests

| Tool | Scope | Frequency |
|---|---|---|
| Playwright | Critical user journeys: login, time entry, invoice, payment | Every PR + nightly |
| axe-core | WCAG 2.1 AA automated checks | Every PR |

### Performance & Load Tests

| Tool | Scope | Frequency |
|---|---|---|
| k6 | Login + time-entry journey against staging | Before releases |
| Lighthouse CI | Core Web Vitals | Every PR |

## CI Gates

1. **Lint & type check** must pass.
2. **Unit + integration tests** must pass with coverage ≥ 80% backend.
3. **E2E smoke tests** must pass.
4. **Security scans** (SAST, SCA, secrets) must pass.
5. **Accessibility checks** must pass.
6. **Contract tests** must pass.

## Environments

| Environment | Purpose | Data |
|---|---|---|
| Local | Developer iteration | Synthetic / seeded |
| CI | Automated checks | Ephemeral SQLite/Postgres |
| Staging | Pre-release validation | Anonymized production-like |
| Production | Live users | Real |

## Responsibilities

| Role | Responsibility |
|---|---|
| SDET | Owns test architecture, E2E framework, CI integration. |
| Backend Engineer | Owns unit and integration tests for backend code. |
| Frontend Engineer | Owns unit tests for components and hooks; supports E2E. |
| QA Enablement | Sets standards, templates, and tooling; does not gatekeep. |

## Tooling

- Backend: pytest, pytest-asyncio, pytest-cov, factory-boy, httpx
- Frontend: Vitest, Testing Library, Playwright, @axe-core/playwright
- Contracts: Pact
- Load: k6
- Coverage reporting: pytest-cov, Vitest coverage

## Review & Improvement

- Weekly: review flaky tests, coverage trends, and test runtimes.
- Monthly: assess pyramid balance and add tests for recent incidents.
