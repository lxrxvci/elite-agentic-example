"""Database session management tuned for long-running containers and serverless."""

from __future__ import annotations

import os
from collections.abc import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool


def _normalize_database_url(url: str) -> str:
    """Return a SQLAlchemy-compatible URL for the psycopg v3 driver.

    Vercel Postgres / Neon expose ``postgres://`` or ``postgresql://`` URLs.
    SQLAlchemy requires the explicit ``postgresql+psycopg://`` dialect prefix.
    """
    if url.startswith("postgres://"):
        url = "postgresql+psycopg" + url[len("postgres") :]
    elif url.startswith("postgresql://"):
        url = "postgresql+psycopg" + url[len("postgresql") :]
    return url


DATABASE_URL = _normalize_database_url(
    os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/elite_db",
    )
)

# Serverless environments (Vercel, Neon pooled connections) should not keep
# persistent connections. Use NullPool when an external pooler is in front of
# the database or when requested explicitly.
POOL_DISABLED = os.getenv("DATABASE_POOL_DISABLED", "").lower() in {"1", "true", "yes"}

connect_args: dict[str, object] = {
    "sslmode": os.getenv("DATABASE_SSLMODE", "prefer"),
    "connect_timeout": 10,
}

if POOL_DISABLED:
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        connect_args=connect_args,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=int(os.getenv("DATABASE_POOL_SIZE", "2")),
        max_overflow=int(os.getenv("DATABASE_POOL_MAX_OVERFLOW", "4")),
        pool_recycle=int(os.getenv("DATABASE_POOL_RECYCLE", "300")),
        connect_args=connect_args,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_database() -> bool:
    """Return True if the database is reachable, False otherwise."""
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
            return True
    except Exception:
        return False
