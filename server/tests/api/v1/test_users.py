from fastapi.testclient import TestClient


def test_read_users(admin_client: TestClient):
    url = "/api/v1/users/"
    r = admin_client.get(url=url)
    assert r.status_code == 200

    data = r.json()
    assert isinstance(data, list)
