#!/usr/bin/env python3
"""Synthetic canary analysis: hit an endpoint and check latency/error SLOs."""
from __future__ import annotations

import argparse
import statistics
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.error import HTTPError


def request_once(url: str, timeout: float) -> tuple[float, int | None]:
    start = time.perf_counter()
    status: int | None = None
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            status = response.getcode()
    except HTTPError as exc:
        status = exc.code
    except Exception:
        status = None
    duration = time.perf_counter() - start
    return duration, status


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic canary analysis")
    parser.add_argument("--url", default="https://elite-backend.fly.dev/health")
    parser.add_argument("--requests", type=int, default=50)
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--max-error-rate", type=float, default=0.02)
    parser.add_argument("--max-latency-p99", type=float, default=0.5)
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    print(f"Running {args.requests} requests against {args.url}...")
    durations: list[float] = []
    errors = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(request_once, args.url, args.timeout) for _ in range(args.requests)]
        for future in as_completed(futures):
            duration, status = future.result()
            durations.append(duration)
            if status is None or status >= 500:
                errors += 1

    total = len(durations)
    error_rate = errors / total if total else 1.0
    durations.sort()
    p99 = durations[int(len(durations) * 0.99)] if durations else 0.0
    median = statistics.median(durations) if durations else 0.0

    print(f"Requests: {total}, Errors: {errors}, Error rate: {error_rate:.2%}")
    print(f"Median latency: {median:.3f}s, P99 latency: {p99:.3f}s")

    ok = error_rate <= args.max_error_rate and p99 <= args.max_latency_p99
    if not ok:
        print("Canary FAILED: SLO breach detected.")
        return 1
    print("Canary PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
