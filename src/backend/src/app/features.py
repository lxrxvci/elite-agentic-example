"""Feature flag integration with Unleash and env-based fallback."""

from __future__ import annotations

import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

_unleash_client: Any | None = None


def _get_unleash_client() -> Any | None:
    """Return a lazily-initialized Unleash client, or None if not configured."""
    global _unleash_client  # noqa: PLW0603
    if _unleash_client is not None:
        return _unleash_client

    if not settings.unleash_url:
        return None

    try:
        from UnleashClient import UnleashClient

        _unleash_client = UnleashClient(
            url=settings.unleash_url,
            app_name=settings.unleash_app_name,
            custom_headers={"Authorization": settings.unleash_api_token},
            refresh_interval=settings.unleash_refresh_interval,
        )
        _unleash_client.initialize_client()
        logger.info("Unleash feature flag client initialized")
        return _unleash_client
    except Exception:
        logger.exception("Failed to initialize Unleash client; falling back to env flags")
        _unleash_client = None
        return None


def is_feature_enabled(flag_key: str, context: dict[str, Any] | None = None) -> bool:
    """Return True if the feature flag is enabled.

    Uses Unleash when configured; otherwise falls back to the comma-separated
    ENABLED_FEATURES environment variable.
    """
    client = _get_unleash_client()
    if client is not None:
        try:
            return bool(client.is_enabled(flag_key, context))
        except Exception:
            logger.exception("Unleash check failed for %s; falling back to env flags", flag_key)

    enabled = {key.strip() for key in settings.enabled_features.split(",") if key.strip()}
    return flag_key in enabled


def shutdown_feature_client() -> None:
    """Gracefully destroy the Unleash client, if initialized."""
    global _unleash_client  # noqa: PLW0603
    if _unleash_client is not None:
        try:
            _unleash_client.destroy()
        except Exception:
            logger.exception("Error shutting down Unleash client")
        finally:
            _unleash_client = None
