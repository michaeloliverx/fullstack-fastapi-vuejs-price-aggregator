import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "url, method",
    (
        ("/api/v1/users/", "GET",),
        ("/api/v1/users/", "POST",),
        ("/api/v1/users/1", "GET",),
        ("/api/v1/users/1", "PUT",),
        ("/api/v1/users/1", "DELETE",),
        ("/api/v1/users/1/roles", "GET",),
    ),
)
def test_endpoints_without_admin_role(
    user_role_client: TestClient, url: str, method: str
):
    """
    Test all /user endpoints with an authenticated client but without an admin role assigned.
    """
    resp = user_role_client.request(method, url, json={})
    assert 400 <= resp.status_code < 500


def test_read_many(admin_role_client: TestClient):
    url = "/api/v1/users/"
    resp = admin_role_client.get(url=url)
    assert resp.status_code == 200, resp.json()
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read(admin_role_client: TestClient):
    """
    Test getting a user.
    """

    # Create a user to read first
    url = "/api/v1/users/"
    data = {
        "email": "user@domain.com",
        "password": "safe_pass",
        "first_name": "Michael",
        "last_name": "Oliver",
    }

    resp = admin_role_client.post(url, json=data)
    assert resp.status_code == 201

    data = resp.json()
    user_id = data["id"]

    url = f"/api/v1/users/{user_id}"
    resp = admin_role_client.get(url)
    assert resp.status_code == 200


@pytest.mark.parametrize("user_id", [999, 0, -1, "g"])
def test_read_invalid_id(admin_role_client: TestClient, user_id):
    """
    Test getting a user with an invalid id.
    """

    # Create a user to read first
    url = f"/api/v1/users/{user_id}"
    resp = admin_role_client.get(url)
    assert resp.status_code in [404, 422]  # User not found / Invalid ID


def test_create(admin_role_client: TestClient):
    """
    Test creating a user.
    """
    url = "/api/v1/users/"
    data = {
        "email": "user@domain.com",
        "password": "safe_pass",
        "first_name": "Michael",
        "last_name": "Oliver",
    }

    resp = admin_role_client.post(url, json=data)
    assert resp.status_code == 201

    # Default value of status should be inactive
    data = resp.json()
    assert data["status"] == "inactive"


@pytest.mark.parametrize("status", ("active", "disabled", "inactive"))
def test_create_with_status(admin_role_client: TestClient, status: str):
    """
    Test creating a user with a certain status.
    """
    data = {
        "email": "user@domain.com",
        "password": "safe_pass",
        "first_name": "Michael",
        "last_name": "Oliver",
        "status": status,
    }

    resp = admin_role_client.post("/api/v1/users/", json=data)
    assert resp.status_code == 201

    data = resp.json()
    assert data["status"] == status


def test_create_existing_email(admin_role_client: TestClient):
    """
    Test creating a user with an existing email.
    """
    url = "/api/v1/users/"
    data = {
        "email": "user@domain.com",
        "password": "safe_pass",
        "first_name": "Michael",
        "last_name": "Oliver",
    }

    resp = admin_role_client.post(url, json=data)
    assert resp.status_code == 201

    resp2 = admin_role_client.post(url, json=data)
    assert 400 <= resp2.status_code < 500


def test_delete(admin_role_client: TestClient):
    """
    Test deleting a user.
    """

    # Create a user
    url = "/api/v1/users/"
    data = {
        "email": "user@domain.com",
        "password": "safe_pass",
        "first_name": "Michael",
        "last_name": "Oliver",
    }
    resp = admin_role_client.post(url, json=data)
    assert resp.status_code == 201

    data = resp.json()
    user_id = data["id"]

    # Delete the user
    url = f"/api/v1/users/{user_id}"
    resp = admin_role_client.delete(url)
    assert resp.status_code == 200

    # Ensure user has been deleted from the database
    resp = admin_role_client.get(url)
    assert resp.status_code == 404
