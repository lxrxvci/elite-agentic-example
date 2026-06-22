"""Pact provider verification for the auth API."""

from __future__ import annotations

from pathlib import Path

import pytest
from pact import Verifier

PACTS_DIR = Path(__file__).parent.parent.parent.parent.parent / "src" / "frontend" / "pacts"


@pytest.mark.skipif(not list(PACTS_DIR.glob("*.json")), reason="No pact contracts found")
def test_auth_provider() -> None:
    """Verify the backend satisfies consumer contracts."""
    verifier = Verifier(
        provider="elite-backend",
        provider_base_url="http://localhost:8000",
    )
    contracts = [str(p) for p in PACTS_DIR.glob("*.json")]
    result = verifier.verify_pacts(contracts)
    assert result == 0, "Pact provider verification failed"
