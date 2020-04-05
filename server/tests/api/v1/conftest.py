import pytest
from fastapi.testclient import TestClient
from sqlalchemy import orm

from app.enums import userenums
from app.models import usermodels
from tests import common, factories


@pytest.fixture(scope="function")
def user_with_admin_role(db_session: orm.Session):
    admin_role = factories.RoleFactory.create(name="admin")
    user = factories.UserFactory.create(
        status=userenums.UserStatus.active, roles=[admin_role]
    )
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def user_with_user_role(db_session: orm.Session):
    user_role = factories.RoleFactory(name="user")
    user = factories.UserFactory.create(
        status=userenums.UserStatus.active, roles=[user_role]
    )
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def admin_role_client(
    client: TestClient, db_session: orm.Session, user_with_admin_role: usermodels.User
):
    """
    Fixture provides an authenticated test client with admin role.
    """

    # Get an access token from v1 api
    resp = client.post(
        url="api/v1/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={
            "username": user_with_admin_role.email,
            "password": common.USER_PASSWORD,
        },
    )

    assert resp.status_code == 200

    # Set client auth headers
    token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    # Testing a protected endpoint
    url = "/api/v1/auth/login/test-token"
    res = client.post(url=url)
    assert res.status_code == 200

    # Run tests..
    yield client


@pytest.fixture(scope="function")
def user_role_client(
    client: TestClient, db_session: orm.Session, user_with_user_role: usermodels.User
):
    """
    Fixture provides an authenticated test client with user role.
    """

    resp = client.post(
        url="api/v1/auth/login",
        headers={"content-type": "application/x-www-form-urlencoded"},
        data={"username": user_with_user_role.email, "password": common.USER_PASSWORD,},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    yield client
