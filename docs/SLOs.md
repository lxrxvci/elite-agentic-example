# Service Level Objectives

## Overview

| Attribute | Value |
|---|---|
| Product | {{product_name}} |
| Version | {{version}} |
| Author | {{author}} |
| Date | {{date}} |
| Review cadence | Monthly |

## SLIs & SLOs

### API Availability

| Field | Value |
|---|---|
| SLI | Ratio of successful HTTP responses (2xx/3xx) to total requests |
| SLO | 99.9% over 30 days |
| Error budget | 0.1% of requests may fail |
| Measurement | Prometheus/OTel metrics from `/health` and access logs |
| Alert threshold | 99.5% over 5 minutes |

### API Latency

| Field | Value |
|---|---|
| SLI | p95 response time for API requests |
| SLO | p95 < 300ms over 30 days |
| Measurement | Prometheus/OTel histograms |
| Alert threshold | p95 > 500ms for 5 minutes |

### Frontend Performance

| Field | Value |
|---|---|
| SLI | LCP for authenticated dashboard |
| SLO | LCP < 2.5s for 75th percentile of users |
| Measurement | Vercel Analytics / Chrome UX Report |
| Alert threshold | LCP > 4s |

### Error Rate

| Field | Value |
|---|---|
| SLI | Ratio of 5xx responses to total responses |
| SLO | < 0.1% over 30 days |
| Measurement | Access logs / APM |
| Alert threshold | > 0.5% for 5 minutes |

## Error Budget Policy

1. **Budget period:** 30 days, reset monthly.
2. **Exhaustion triggers:**
   - 50% exhausted → page on-call; prioritize reliability work.
   - 100% exhausted → feature freeze until budget resets or SLO is restored.
3. **Exceptions:** security incidents and force-majeure events do not consume error budget.

## On-Call & Escalation

| Severity | Criteria | Response time | Escalation |
|---|---|---|---|
| SEV1 | Complete outage or data loss | 15 minutes | Page engineering + product |
| SEV2 | Major feature degraded | 1 hour | Page engineering |
| SEV3 | Minor degradation | 4 hours | Next business day |
| SEV4 | Cosmetic / low impact | Best effort | Backlog |

## Review Log

| Date | SLO attainment | Error budget remaining | Notes |
|---|---|---|---|
| {{date}} | {{%}} | {{%}} | Initial SLOs defined |
