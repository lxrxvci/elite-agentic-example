# Runbook: Rollback

## When to Rollback

- Recent deploy caused increased errors or latency.
- Feature flag flip caused unexpected behavior.
- Data corruption or security issue introduced.

## Steps

### 1. Identify the bad release

```bash
gh run list --workflow=deploy.yml
# or
fly releases list --app <app-name>
```

### 2. Stop traffic (if needed)

- Flip feature flag to off.
- Scale problematic service to 0 temporarily.
- Enable maintenance page if required.

### 3. Roll back backend

```bash
# Fly.io example
fly deploy --image ghcr.io/<owner>/elite-backend:<previous-sha>
```

### 4. Roll back frontend

```bash
# Vercel example
vercel --prod # redeploy previous production build via dashboard or CLI
```

### 5. Roll back database (if safe)

- Run downgrades only after backups.
- Document any data fixes needed.

### 6. Verify

- Check `/health` and `/ready`.
- Review error rate and latency dashboards.
- Confirm key user journeys via smoke tests.

### 7. Communicate

Update incident channel with rollback status and next steps.
