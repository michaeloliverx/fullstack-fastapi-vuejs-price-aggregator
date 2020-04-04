from sqlalchemy import TIMESTAMP, Column, Integer
from sqlalchemy.sql import func

from .sqlalchemytypes import GUID


class SQLAlchemyIntPK:
    """
    Provides an integer PK column named `id`.
    """

    id = Column(Integer, primary_key=True)


class SQLAlchemyGUIDPK:
    """
    Provides a GUID PK column named `id`.
    """

    id = Column(GUID, primary_key=True)


class SQLAlchemyTS:
    """
    SQLAlchemy timestamp mixin.
    """

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_onupdate=func.now())
