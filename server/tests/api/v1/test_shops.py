import pytest
from fastapi.testclient import TestClient

from tests.factories import ShopFactory


def test_read_many(user_role_client: TestClient):
    """
    Test reading many shops.
    """

    # Create some shops in the db first
    ShopFactory()
    ShopFactory()
    ShopFactory()

    url = "/api/v1/shops/"
    resp = user_role_client.get(url=url)
    assert resp.status_code == 200, resp.json()
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read(admin_role_client: TestClient):
    """
    Test getting a shop.
    """

    # Create a shop to read first
    db_shop = ShopFactory()

    shop_id = db_shop.id
    url = f"/api/v1/shops/{shop_id}"
    resp = admin_role_client.get(url)
    assert resp.status_code == 200, resp.text


@pytest.mark.parametrize("user_id", [999, 0, -1, "g"])
def test_read_invalid_id(admin_role_client: TestClient, user_id):
    """
    Test getting a shop with an invalid id.
    """

    # Create a user to read first
    url = f"/api/v1/users/{user_id}"
    resp = admin_role_client.get(url)
    assert resp.status_code in [404, 422]


def test_create(admin_role_client: TestClient):
    """
    Test creating a shop.
    """
    url = "/api/v1/shops/"
    data = {
        "name": "tesco",
        "url": "www.tesco.com",
        "query_url": "/groceries/en-GB/search?query={query}",
        "render_javascript": False,
        "listing_page_selector": {},
    }

    resp = admin_role_client.post(url, json=data)
    assert resp.status_code == 201, resp.text


def test_create_existing_name(admin_role_client: TestClient):
    """
    Test creating a shop with an already existing name.
    """
    db_shop = ShopFactory()
    name = db_shop.name
    url = "/api/v1/shops/"
    data = {
        "name": name,
        "url": "www.tesco.com",
        "query_url": "/groceries/en-GB/search?query={query}",
        "render_javascript": False,
        "listing_page_selector": {},
    }

    resp = admin_role_client.post(url, json=data)
    assert resp.status_code == 400, resp.text


def test_delete(admin_role_client: TestClient):
    """
    Test deleting a user.
    """

    # Create one to delete first
    db_shop = ShopFactory()

    id_ = db_shop.id

    # Delete the shop
    url = f"/api/v1/shops/{id_}"
    resp = admin_role_client.delete(url)
    assert resp.status_code == 200

    # Ensure user has been deleted from the database
    resp = admin_role_client.get(url)
    assert resp.status_code == 404
