"""Project API tests."""

from fastapi.testclient import TestClient


def test_create_and_get_project(client: TestClient, seeded_user: dict, seeded_client) -> None:
    headers = seeded_user["headers"]
    response = client.post(
        "/api/v1/projects",
        json={
            "client_id": str(seeded_client.id),
            "name": "Website Redesign",
            "rounding_minutes": 15,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Website Redesign"
    assert data["client_id"] == str(seeded_client.id)

    get_response = client.get(f"/api/v1/projects/{data['id']}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Website Redesign"


def test_list_projects_filtered_by_client(
    client: TestClient, seeded_user: dict, seeded_project
) -> None:
    headers = seeded_user["headers"]
    response = client.get(f"/api/v1/projects?client_id={seeded_project.client_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
