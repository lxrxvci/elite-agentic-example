"""Time entry API tests."""

from fastapi.testclient import TestClient


def test_create_time_entry_with_duration(
    client: TestClient, seeded_user: dict, seeded_project
) -> None:
    headers = seeded_user["headers"]
    response = client.post(
        "/api/v1/time-entries",
        json={
            "client_id": str(seeded_project.client_id),
            "project_id": str(seeded_project.id),
            "description": "Revised homepage hero copy",
            "duration_minutes": 20,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Revised homepage hero copy"
    assert data["duration_minutes"] == 20
    assert data["rounded_minutes"] == 15
    assert data["status"] == "unbilled"


def test_list_time_entries(client: TestClient, seeded_user: dict, seeded_project) -> None:
    headers = seeded_user["headers"]
    client.post(
        "/api/v1/time-entries",
        json={
            "client_id": str(seeded_project.client_id),
            "project_id": str(seeded_project.id),
            "description": "Another entry",
            "duration_minutes": 30,
        },
        headers=headers,
    )
    response = client.get("/api/v1/time-entries?status=unbilled", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
