import os  # isort:skip

# Set test config before importing application
os.environ["FASTAPI_ENV"] = "testing"
os.environ["POSTGRES_DB"] = os.environ["POSTGRES_DB"] + "_testing"
os.environ["USERS_OPEN_REGISTRATION"] = "true"

import pytest
from alembic import command as alembic_cmd
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from sqlalchemy import orm
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.db.session import engine, get_db
from app.enums.userenums import UserStatus
from app.main import app
from app.models import usermodels
from app.settings import settings

from . import factories
from .common import USER_PASSWORD, ScopedSession, override_get_db

assert settings.FASTAPI_ENV == "testing"

# Overriding dependencies
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Fixture used to setup and teardown a new database for each testing session.
    To skip running the migrations comment/uncomment the appropriate lines.
    """

    url = str(engine.url)
    assert url.endswith("_testing")

    if database_exists(url):
        drop_database(url)
    create_database(url)

    # # Create tables with SQLAlchemy
    # SQLAlchemyBase.metadata.create_all(_engine)

    # Create tables using Alembic scripts
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cmd.upgrade(config=alembic_cfg, revision="head")

    yield  # Run the tests.

    drop_database(url)


@pytest.fixture(scope="function")
def session():
    """
    Fixture returns a scoped sqlalchemy session, and after rolls back any changes.
    """

    # Using scoped session allows us to use the same session in any test case.
    _session: orm.Session = ScopedSession()
    _session.begin_nested()
    yield _session
    _session.rollback()
    ScopedSession.remove()


@pytest.fixture(scope="function")
def client(session):
    """
    Using 'client' fixture in test cases, we'll get:
        - 'startup' and 'shutdown' event handlers called
        - full database rollback between test cases

    This client does not have any authorization headers set.

    """
    with TestClient(app) as _client:
        yield _client


@pytest.fixture(scope="function")
def admin_client(client: TestClient, session: orm.Session):
    """
    Fixture provides a client with admin role headers.
    """

    # Creating new active user
    user: usermodels.User = factories.UserFactory(status=UserStatus.active)
    # Adding "admin" role to user
    user.roles = [factories.RoleFactory(name="admin")]

    session.add(user)
    # Don't know why but commit must be called twice??
    session.commit()
    session.commit()

    url = "api/v1/auth/login"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    data = {
        "username": user.email,
        "password": USER_PASSWORD,
    }

    resp = client.post(url=url, headers=headers, data=data)
    assert resp.status_code == 200

    token = resp.json()["access_token"]

    # Setting auth headers
    client.headers["Authorization"] = f"Bearer {token}"

    # Testing a protected endpoint
    url = "​/api​/v1​/auth​/login​/test-token"
    res = client.get(url=url)
    assert res.status_code == 200

    yield client


@pytest.fixture
def user():
    return factories.UserFactory()


@pytest.fixture
def users():
    return [factories.UserFactory() for _ in range(2)]


@pytest.fixture
def role():
    return factories.RoleFactory()


@pytest.fixture
def roles():
    role_names = ["admin", "user"]
    return [factories.RoleFactory(name=i) for i in role_names]
