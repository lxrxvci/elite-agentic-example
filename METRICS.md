# Metrics

## North Star

| Metric | Definition | Target | Owner |
|---|---|---|---|
| {{North Star}} | {{Definition}} | {{Target}} | Product Strategist |

## DORA Metrics

| Metric | Definition | Current | Target | Data Source |
|---|---|---|---|---|
| Deployment Frequency | Number of production deployments per week | {{value}} | On demand (multiple/day) | GitHub Actions deploy events |
| Lead Time for Changes | Median time from PR merge to production | {{value}} | < 1 day | GitHub API + deploy events |
| Change Failure Rate | Percentage of deploys causing incidents | {{value}} | < 5% | Incident / deploy ratio |
| Failed Deployment Recovery Time | Median time to recover from failed deploy | {{value}} | < 1 hour | Incident data |

## Flow Metrics

| Metric | Definition | Current | Target | Data Source |
|---|---|---|---|---|
| WIP | Work in progress items | {{value}} | Team size + 1 per stage | Board / backlog |
| Cycle Time | Time from start to done | {{value}} | < 5 days | Board timestamps |
| Throughput | Items completed per week | {{value}} | TBD | Board velocity |
| Flow Efficiency | Process time / lead time | {{value}} | > 10% | VSM analysis |

## Quality Metrics

| Metric | Definition | Current | Target | Data Source |
|---|---|---|---|---|
| Test Coverage | Line coverage (backend + frontend) | {{value}} | ≥ 80% | pytest / vitest |
| Unit Test Pass Rate | % passing on main | {{value}} | 100% | CI |
| E2E Pass Rate | % passing on main | {{value}} | 100% | CI |
| Security Scan Findings | Open CRITICAL/HIGH | {{value}} | 0 | Trivy / Bandit / Semgrep |
| Bug Escape Rate | Bugs found in production / total bugs | {{value}} | < 10% | Issue tracker |

## UX Metrics

| Metric | Definition | Current | Target | Data Source |
|---|---|---|---|---|
| Core Web Vitals LCP | Largest Contentful Paint | {{value}} | < 2.5s | Chrome UX Report / Vercel |
| Core Web Vitals INP | Interaction to Next Paint | {{value}} | < 200ms | Chrome UX Report |
| Core Web Vitals CLS | Cumulative Layout Shift | {{value}} | < 0.1 | Chrome UX Report |
| Task Success Rate | % users completing key task | {{value}} | TBD | Analytics / user tests |

## Review Cadence

- Weekly: DORA and flow metrics during squad review.
- Monthly: North Star and UX metrics review with leadership.
- Quarterly: Full metrics audit and target recalibration.
