"""Tenant isolation tests."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.dependencies import create_access_token
from infrastructure.models import Client, Tenant, User


def test_user_cannot_read_other_tenant_client(
    client: TestClient, db: Session, seeded_user: dict, seeded_client
) -> None:
    # Create a second tenant/user with access to a different client
    other_tenant = Tenant(name="Other Tenant", default_currency="USD")
    db.add(other_tenant)
    db.flush()

    other_client = Client(
        tenant_id=other_tenant.id,
        name="Other Client",
        currency="USD",
    )
    db.add(other_client)

    other_user = User(
        id=uuid.uuid4(),
        tenant_id=other_tenant.id,
        email="other@example.com",
        name="Other User",
    )
    db.add(other_user)
    db.flush()

    other_token = create_access_token(
        user_id=other_user.id,
        email=other_user.email,
        name=other_user.name,
        tenant_id=other_tenant.id,
    )

    response = client.get(
        f"/api/v1/clients/{seeded_client.id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 404
