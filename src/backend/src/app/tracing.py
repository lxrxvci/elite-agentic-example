"""OpenTelemetry tracing configuration."""

from __future__ import annotations

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import settings


def configure_tracing(service_name: str = "elite-backend") -> None:
    """Configure OpenTelemetry tracing when OTEL_EXPORTER_OTLP_ENDPOINT is set."""
    endpoint = settings.otel_exporter_otlp_endpoint
    if not endpoint:
        return

    resource = Resource({SERVICE_NAME: service_name})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def get_tracer(name: str) -> trace.Tracer:
    """Return a tracer for the given module name."""
    return trace.get_tracer(name)


def shutdown_tracing() -> None:
    """Flush and shutdown the global tracer provider, if configured."""
    provider = trace.get_tracer_provider()
    if provider is None:
        return

    # SDK TracerProvider exposes force_flush/shutdown; the no-op provider does not.
    try:
        provider.force_flush(timeout_millis=5000)  # type: ignore[attr-defined]
        provider.shutdown()  # type: ignore[attr-defined]
    except Exception:
        pass
