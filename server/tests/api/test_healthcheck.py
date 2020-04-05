from fastapi.testclient import TestClient


def test_read_me(client: TestClient):
    url = "/api/healthcheck"
    resp = client.get(url=url)
    assert resp.status_code == 200
