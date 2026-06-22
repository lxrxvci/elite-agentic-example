"""Vercel serverless entry point for the FastAPI backend.

Vercel's Python runtime looks for an ``app`` callable exported from an
``api/index.py`` file at the project root. The backend source lives under
``src/``, so we add it to the module search path before importing the
application factory.
"""

from __future__ import annotations

import os
import sys

# Make ``src/`` importable for both local ``vercel dev`` and production builds.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SRC_DIR = os.path.join(_PROJECT_ROOT, "src")
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from main import app  # noqa: E402

# Re-export the ASGI application for Vercel.
__all__ = ["app"]
