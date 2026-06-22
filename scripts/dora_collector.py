"""Collect DORA metrics from GitHub and emit Prometheus exposition format.

Usage:
    python scripts/dora_collector.py --owner myorg --repo myrepo --days 30

Requires GITHUB_TOKEN with repo scope.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


def github_api(path: str, token: str) -> list[dict]:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect DORA metrics")
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--output", type=Path, default=Path("dora-metrics.prom"))
    args = parser.parse_args()

    token = os.environ["GITHUB_TOKEN"]
    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    # Fetch deployments
    deployments = github_api(
        f"/repos/{args.owner}/{args.repo}/deployments?per_page=100",
        token,
    )
    recent_deployments = [
        d for d in deployments if parse_iso(d["created_at"]) >= since
    ]
    deployment_frequency = len(recent_deployments)

    # Fetch workflow runs for lead time approximation
    runs = github_api(
        f"/repos/{args.owner}/{args.repo}/actions/runs?per_page=100",
        token,
    )
    lead_times = []
    for run in runs.get("workflow_runs", []):
        created = run.get("created_at")
        updated = run.get("updated_at")
        if created and updated:
            lead = (parse_iso(updated) - parse_iso(created)).total_seconds()
            lead_times.append(lead)
    median_lead_time = sorted(lead_times)[len(lead_times) // 2] if lead_times else 0

    # Fetch issues labeled incident for change failure / recovery
    incidents = github_api(
        f"/repos/{args.owner}/{args.repo}/issues?labels=incident&state=all&per_page=100",
        token,
    )
    recent_incidents = [i for i in incidents if parse_iso(i["created_at"]) >= since]
    failed_deployments = len(recent_incidents)
    cfr = failed_deployments / deployment_frequency if deployment_frequency else 0

    recovery_times = []
    for incident in recent_incidents:
        created = parse_iso(incident["created_at"])
        closed = incident.get("closed_at")
        if closed:
            recovery_times.append((parse_iso(closed) - created).total_seconds())
    mttr = sorted(recovery_times)[len(recovery_times) // 2] if recovery_times else 0

    lines = [
        "# HELP elite_deployments_total Number of deployments in the window",
        "# TYPE elite_deployments_total counter",
        f'elite_deployments_total{{window="{args.days}d"}} {deployment_frequency}',
        "# HELP elite_lead_time_seconds Median lead time for changes",
        "# TYPE elite_lead_time_seconds gauge",
        f'elite_lead_time_seconds{{window="{args.days}d"}} {median_lead_time}',
        "# HELP elite_change_failure_rate Ratio of failed deployments",
        "# TYPE elite_change_failure_rate gauge",
        f'elite_change_failure_rate{{window="{args.days}d"}} {cfr}',
        "# HELP elite_recovery_time_seconds Median time to recovery",
        "# TYPE elite_recovery_time_seconds gauge",
        f'elite_recovery_time_seconds{{window="{args.days}d"}} {mttr}',
    ]

    args.output.write_text("\n".join(lines) + "\n")
    print(f"Wrote DORA metrics to {args.output}")


if __name__ == "__main__":
    main()
