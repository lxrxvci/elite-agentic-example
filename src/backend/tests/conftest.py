"""Test fixtures."""

from __future__ import annotations

import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENV", "development")

import uuid  # noqa: E402
from decimal import Decimal  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import Session, sessionmaker  # noqa: E402

from app.dependencies import create_access_token  # noqa: E402
from infrastructure.database import Base, get_db  # noqa: E402
from infrastructure.models import Client, Project, Tenant, User  # noqa: E402
from main import app  # noqa: E402

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///./test.db",
)

_connect_args = {"check_same_thread": False} if TEST_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(TEST_DATABASE_URL, connect_args=_connect_args)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db: Session):
    def _override():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def seeded_user(db: Session):
    tenant = Tenant(
        name="Test Tenant", default_currency="USD", default_hourly_rate=Decimal("150.00")
    )
    db.add(tenant)
    db.flush()

    user = User(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email="test@example.com",
        name="Test User",
    )
    db.add(user)
    db.commit()

    token = create_access_token(
        user_id=user.id,
        email=user.email,
        name=user.name,
        tenant_id=user.tenant_id,
    )
    return {
        "user": user,
        "tenant": tenant,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"},
    }


@pytest.fixture()
def seeded_client(db: Session, seeded_user):
    client = Client(
        tenant_id=seeded_user["tenant"].id,
        name="Acme Corp",
        email="billing@acme.example",
        currency="USD",
        default_hourly_rate=Decimal("150.00"),
    )
    db.add(client)
    db.commit()
    return client


@pytest.fixture()
def seeded_project(db: Session, seeded_user, seeded_client):
    project = Project(
        tenant_id=seeded_user["tenant"].id,
        client_id=seeded_client.id,
        name="Website Redesign",
        rounding_minutes=15,
    )
    db.add(project)
    db.commit()
    return project
