import os  # isort:skip

# Set test config before importing application
os.environ["FASTAPI_ENV"] = "testing"
os.environ["POSTGRES_DB"] = os.environ["POSTGRES_DB"] + "_testing"
os.environ["USERS_OPEN_REGISTRATION"] = "true"

import contextlib

import pytest
from alembic import command as alembic_cmd
from alembic.config import Config as AlembicConfig
from fastapi.testclient import TestClient
from sqlalchemy import orm
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.db.session import engine
from app.main import app
from app.models.meta.sqlalchemybase import SQLAlchemyBase
from app.settings import settings

from . import common

assert settings.FASTAPI_ENV == "testing"


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
def db_session():
    """
    Fixture returns a scoped sqlalchemy session, and after rolls back any changes.

    See:
        https://factoryboy.readthedocs.io/en/latest/orms.html#managing-sessions

    """

    session: orm.Session = common.ScopedSession()
    try:
        yield session  # Run tests here
    finally:
        # Drop all data after each test
        # https://stackoverflow.com/a/5003705
        with contextlib.closing(engine.connect()) as con:
            trans = con.begin()
            for table in reversed(SQLAlchemyBase.metadata.sorted_tables):
                con.execute(table.delete())
            trans.commit()

        # put back the connection to the connection pool
        common.ScopedSession.remove()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Fixture returns an api client based on `requests`.
    As we are using a context manager 'startup' and 'shutdown'
    event handlers are called.
    Using the `db_session` fixture gives us a clean database
    for each test case.

    This client does not have any authorization headers set.

    """

    with TestClient(app) as _client:
        yield _client
