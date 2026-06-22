# Threat Model

## Overview

| Attribute | Value |
|---|---|
| Product | {{product_name}} |
| Version | {{version}} |
| Author | {{author}} |
| Date | {{date}} |
| Status | Draft / Review / Accepted |

## Scope

This threat model covers:
- {{scope_boundary_1}}
- {{scope_boundary_2}}

Out of scope:
- {{out_of_scope_1}}

## Data Flow Diagram

```
[User Browser] ──HTTPS──▶ [CDN / Vercel] ──HTTPS──▶ [FastAPI Backend] ──TLS──▶ [PostgreSQL]
                              │                           │
                              ▼                           ▼
                        [Static Assets]              [GitHub Actions / CI]
```

## Threats

### 1. {{Threat title}}

| Field | Description |
|---|---|
| Threat ID | T001 |
| STRIDE category | Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege |
| Description | {{What could go wrong?}} |
| Likelihood | Low / Medium / High |
| Impact | Low / Medium / High |
| Risk rating | Low / Medium / High / Critical |
| Mitigation | {{How do we prevent or reduce this?}} |
| Owner | {{role}} |
| Status | Open / Mitigated / Accepted |

### 2. {{Threat title}}

| Field | Description |
|---|---|
| Threat ID | T002 |
| STRIDE category | ... |
| Description | ... |
| Likelihood | ... |
| Impact | ... |
| Risk rating | ... |
| Mitigation | ... |
| Owner | ... |
| Status | ... |

## Security Controls

| Control | Implementation | Verification |
|---|---|---|
| Authentication | {{OIDC / JWT / etc.}} | {{Tests or checks}} |
| Authorization | {{RBAC / tenant isolation}} | {{Tests}} |
| Input validation | {{Pydantic schemas}} | {{Unit tests}} |
| Output encoding | {{React escaping / CSP}} | {{E2E + headers}} |
| Rate limiting | {{slowapi}} | {{Integration tests}} |
| Logging & monitoring | {{structured logs, alerts}} | {{Dashboard review}} |

## Action Items

| ID | Action | Owner | Due | Status |
|---|---|---|---|---|
| A001 | {{Action}} | {{Owner}} | {{Due}} | Open |

## Review History

| Date | Reviewer | Notes |
|---|---|---|
| {{date}} | {{reviewer}} | Initial threat model |
