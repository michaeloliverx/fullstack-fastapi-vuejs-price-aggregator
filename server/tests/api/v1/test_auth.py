from fastapi.testclient import TestClient


def test_use_access_token(admin_role_client):
    url = "/api/v1/auth/login/test-token"
    resp = admin_role_client.post(url=url)
    assert resp.status_code == 200


def test_access_protected_endpoint_without_token(client: TestClient):
    url = "/api/v1/auth/login/test-token"
    resp = client.post(url=url)
    assert resp.status_code == 401
