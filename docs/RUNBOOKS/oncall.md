# Runbook: On-Call

## Purpose

This runbook describes the responsibilities and daily workflow for the on-call engineer.

## Prerequisites

- Access to PagerDuty / Opsgenie / alerting system.
- Access to logs (Grafana/Loki / CloudWatch).
- Access to dashboards (Grafana / Vercel / Fly).
- Access to deployment pipeline (GitHub Actions).

## Shift Start

1. Acknowledge any active pages.
2. Review dashboard for anomalies (error rate, latency, saturation).
3. Check #incidents channel for ongoing issues.
4. Note any deploys in the last 24 hours.

## During the Shift

1. Respond to alerts per the incident-response runbook.
2. Triage low-severity issues; file tickets for non-urgent work.
3. Do not perform risky changes alone; escalate if unsure.

## Shift End

1. Document any incidents in `docs/post-mortems/`.
2. Hand off open issues to next on-call with context.
3. Update the on-call log.

## Useful Commands

```bash
# Check backend health
curl https://<backend>/health

# Check frontend
curl -I https://<frontend>

# View recent deploys
gh run list --workflow=deploy.yml
```
