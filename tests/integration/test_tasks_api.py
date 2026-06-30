from __future__ import annotations

from fastapi.testclient import TestClient

from task_manager.infrastructure.database import get_db
from task_manager.main import app


def _override_get_db(session):
    def _get_db():
        yield session

    return _get_db


def _make_client(db_session) -> TestClient:
    app.dependency_overrides[get_db] = _override_get_db(db_session)
    return TestClient(app)


def _auth_headers(client: TestClient, email="jane@example.com", password="s3cretpw"):
    client.post(
        "/auth/register",
        json={"email": email, "password": password, "name": "Jane"},
    )
    response = client.post("/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(db_session):
    client = _make_client(db_session)

    register_response = client.post(
        "/auth/register",
        json={"email": "jane@example.com", "password": "s3cretpw", "name": "Jane"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["email"] == "jane@example.com"

    login_response = client.post(
        "/auth/login", json={"email": "jane@example.com", "password": "s3cretpw"}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    app.dependency_overrides.clear()


def test_login_with_wrong_password_is_rejected(db_session):
    client = _make_client(db_session)
    client.post(
        "/auth/register",
        json={"email": "jane@example.com", "password": "s3cretpw", "name": "Jane"},
    )

    response = client.post(
        "/auth/login", json={"email": "jane@example.com", "password": "wrong"}
    )

    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_tasks_endpoints_require_auth(db_session):
    client = _make_client(db_session)

    response = client.post("/tasks", json={"title": "Buy milk"})

    assert response.status_code == 401

    app.dependency_overrides.clear()


def test_full_task_crud_flow(db_session):
    client = _make_client(db_session)
    headers = _auth_headers(client)

    create_response = client.post("/tasks", json={"title": "Buy milk"}, headers=headers)
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    list_response = client.get("/tasks", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Buy oat milk"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Buy oat milk"

    status_response = client.patch(
        f"/tasks/{task_id}/status", json={"status": "done"}, headers=headers
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "done"

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404

    app.dependency_overrides.clear()


def test_cannot_access_another_users_task(db_session):
    client = _make_client(db_session)
    owner_headers = _auth_headers(client, email="owner@example.com")
    create_response = client.post(
        "/tasks", json={"title": "Owner only"}, headers=owner_headers
    )
    task_id = create_response.json()["id"]

    intruder_headers = _auth_headers(client, email="intruder@example.com")
    response = client.get(f"/tasks/{task_id}", headers=intruder_headers)

    assert response.status_code == 404

    app.dependency_overrides.clear()
