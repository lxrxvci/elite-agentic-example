# Runbook: Incident Response

## Severity Levels

| Severity | Criteria | Response Time | Channel |
|---|---|---|---|
| SEV1 | Complete outage, data loss, security breach | 15 min | #war-room |
| SEV2 | Major feature degraded, significant customer impact | 1 hour | #incidents |
| SEV3 | Minor degradation, workaround available | 4 hours | #incidents |
| SEV4 | Cosmetic, no customer impact | Best effort | Backlog |

## Response Steps

1. **Detect** — Alert, support ticket, or manual observation.
2. **Triage** — Confirm impact, assign severity, start incident channel/thread.
3. **Mitigate** — Stop the bleeding. Prefer rollback over forward fix.
4. **Resolve** — Verify service is healthy; close incident.
5. **Learn** — Schedule post-mortem within 48 hours for SEV1/SEV2.

## Communication Template

```
Incident: [brief title]
Severity: [SEV1/SEV2/SEV3/SEV4]
Impact: [what is broken and who is affected]
Started: [timestamp]
Status: [investigating / mitigating / resolved]
Next update: [timestamp]
```

## Rollback

If a recent deploy is suspect, follow the rollback runbook.

## Post-Mortem

All SEV1 and SEV2 incidents require a blameless post-mortem within 48 hours. Use the post-mortem template.
