"""Structured logging configuration."""

from __future__ import annotations

import logging
import sys
import uuid
from collections.abc import Callable
from typing import Any

import structlog
from fastapi import Request
from fastapi.responses import Response


def configure_logging(env: str = "development", log_level: str = "info") -> None:
    """Configure structlog and stdlib logging for JSON output in production."""
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.ExtraAdder(),
    ]

    if env == "development":
        # Pretty console output for local development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        # JSON output for production log aggregation
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a structured logger."""
    return structlog.get_logger(name)  # type: ignore[no-any-return]


def correlation_id_middleware(request: Request, call_next: Callable[[Request], Any]) -> Response:
    """Attach a correlation ID to every request for distributed tracing."""
    correlation_id = request.headers.get("x-correlation-id") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)
    response: Response = call_next(request)
    response.headers["x-correlation-id"] = correlation_id
    return response


def request_logging_middleware(request: Request, call_next: Callable[[Request], Any]) -> Response:
    """Log request/response details."""
    logger = get_logger("app.request")
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        query=str(request.query_params),
    )
    response: Response = call_next(request)
    logger.info(
        "request_finished",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
    )
    return response
