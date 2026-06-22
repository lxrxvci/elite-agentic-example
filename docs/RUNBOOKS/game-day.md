# Runbook: Game Day

## Purpose

Quarterly failure-injection exercise to validate incident response, observability, and recovery procedures in a controlled setting.

## Schedule

- Frequency: Once per quarter
- Duration: 2–3 hours
- Participants: On-call engineer, Tech Lead, Product Owner, optional observers

## Scenarios

### Scenario 1: Database latency spike

1. Use a tool like `pumba` or manual query to introduce latency to the database.
2. Observe p95 latency and error rate dashboards.
3. Verify alerts fire.
4. Practice scaling or failover procedures.
5. Document learnings.

### Scenario 2: Backend crash loop

1. Deploy a faulty image to staging.
2. Observe health checks fail.
3. Practice rollback to previous image.
4. Measure time to recovery.

### Scenario 3: Feature flag misconfiguration

1. Flip a critical feature flag to an unexpected state.
2. Observe business metrics and user impact.
3. Practice kill-switch procedure.

## Facilitator checklist

- [ ] Schedule session and invite participants.
- [ ] Prepare scenario scripts and expected outcomes.
- [ ] Ensure staging environment is available.
- [ ] Assign a note-taker.
- [ ] Run post-mortem within 48 hours.

## Success criteria

- Recovery time is within SLO.
- Alerts are actionable and reach the right people.
- Runbooks are updated based on gaps found.
