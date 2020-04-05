import pytest
from fastapi.testclient import TestClient


def test_read_me(user_role_client: TestClient):
    url = "/api/v1/me"
    resp = user_role_client.get(url=url)
    assert resp.status_code == 200, resp.json()


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "mynewemail@gmail.com"},
        {"password": "NewSecretPass01"},
        {"first_name": "New"},
        {"last_name": "Name"},
    ],
)
def test_update_user_me(user_role_client: TestClient, payload: dict):
    url = "/api/v1/me"

    resp = user_role_client.put(url=url, json=payload)
    assert resp.status_code == 200

    data = resp.json()

    for field in payload:
        if field == "password":
            pass
        else:
            assert payload[field].lower() == data[field].lower()


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "imvalid-email-"},
        {"email": "user@@domain.com"},
        {"email": "www.notAnEmail.com"},
    ],
)
def test_update_user_me_invalid_data(user_role_client: TestClient, payload: dict):
    url = "/api/v1/me"
    resp = user_role_client.put(url=url, json=payload)
    assert 400 <= resp.status_code < 500


def test_read_me_roles(user_role_client: TestClient):
    url = "/api/v1/me/roles"
    resp = user_role_client.get(url=url)
    assert resp.status_code == 200

    roles = resp.json()
    assert roles[0]["name"] == "user"
