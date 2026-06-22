"""Client API tests."""

from fastapi.testclient import TestClient


def test_create_and_get_client(client: TestClient, seeded_user: dict) -> None:
    headers = seeded_user["headers"]
    response = client.post(
        "/api/v1/clients",
        json={
            "name": "Acme Corp",
            "email": "billing@acme.example",
            "currency": "USD",
            "default_hourly_rate": "150.00",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme Corp"
    assert data["tenant_id"] == str(seeded_user["tenant"].id)

    get_response = client.get(f"/api/v1/clients/{data['id']}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Acme Corp"


def test_list_clients(client: TestClient, seeded_user: dict, seeded_client) -> None:
    headers = seeded_user["headers"]
    response = client.get("/api/v1/clients", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
