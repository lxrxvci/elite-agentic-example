"""Prometheus metrics and business counters."""

from __future__ import annotations

from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

# Business counters
LOGIN_COUNTER = Counter(
    "elite_logins_total",
    "Total number of successful logins",
    ["tenant_id"],
)

TIME_ENTRY_COUNTER = Counter(
    "elite_time_entries_created_total",
    "Total number of time entries created",
    ["tenant_id"],
)

INVOICE_COUNTER = Counter(
    "elite_invoices_created_total",
    "Total number of invoices created",
    ["tenant_id"],
)

# HTTP request latency
REQUEST_LATENCY = Histogram(
    "elite_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path", "status_code"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)


def metrics_response() -> tuple[bytes, str]:
    """Return Prometheus metrics payload."""
    return generate_latest(), CONTENT_TYPE_LATEST
