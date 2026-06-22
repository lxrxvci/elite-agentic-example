"""Tests for Alembic migration safety."""

from __future__ import annotations

from pathlib import Path


def test_all_migrations_have_downgrade() -> None:
    """Every migration must define a downgrade so rollbacks are possible."""
    versions_dir = Path(__file__).parent.parent / "alembic" / "versions"
    assert versions_dir.exists(), "Alembic versions directory not found"

    migration_files = list(versions_dir.glob("*.py"))
    assert migration_files, "No migration files found"

    for migration_file in migration_files:
        content = migration_file.read_text()
        assert "def downgrade()" in content, f"{migration_file.name} is missing downgrade()"
