from fastapi.testclient import TestClient


def test_read_users(admin_role_client: TestClient):
    url = "/api/v1/users/"
    resp = admin_role_client.get(url=url)
    assert resp.status_code == 200, resp.json()
