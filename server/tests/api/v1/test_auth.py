from fastapi.testclient import TestClient


def test_use_access_token(admin_client: TestClient):
    url = "/api/v1/auth/login/test-token"
    resp = admin_client.post(url=url)
    assert resp.status_code == 200
