"""

https://flask-user.readthedocs.io/en/latest/data_models.html

https://factoryboy.readthedocs.io/en/latest/orms.html#factory.alchemy.SQLAlchemyOptions.sqlalchemy_session

"""

from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String

from .meta.pydanticbase import PydanticBase
from .meta.pydanticmixins import PydanticTS
from .meta.sqlalchemybase import SQLAlchemyBase
from .meta.sqlalchemymixins import SQLAlchemyIntPK, SQLAlchemyTS


# sqlalchemy models
class Role(SQLAlchemyTS, SQLAlchemyIntPK, SQLAlchemyBase):
    __tablename__ = "role"
    name = Column(String, unique=True, nullable=False)
    description = Column(String)


class UserRoles(SQLAlchemyTS, SQLAlchemyIntPK, SQLAlchemyBase):
    """Association table to hold user roles."""

    __tablename__ = "user_roles"
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    role_id = Column(
        Integer, ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE")
    )


# pydantic models
class RoleCreate(PydanticBase):
    """Properties to receive via API on creation"""

    name: str
    description: Optional[str]


class RoleRead(PydanticTS, PydanticBase):
    """Attributes to return via API"""

    id: int
    name: str
    description: str


class RoleUpdate(PydanticBase):
    """Properties to receive via API on update"""

    name: Optional[str]
    description: Optional[str]
