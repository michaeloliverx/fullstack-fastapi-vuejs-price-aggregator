from sqlalchemy import orm

from app.db import initdb


def test_init_roles(session: orm.Session):
    initdb.init_roles(session=session)


def test_initdb(session: orm.Session):
    initdb.initdb(session=session)
