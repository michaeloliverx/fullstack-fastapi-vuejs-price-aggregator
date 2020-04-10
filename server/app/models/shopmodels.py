from typing import Optional

from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String

from .meta.pydanticbase import PydanticBase
from .meta.pydanticmixins import PydanticTS
from .meta.sqlalchemybase import SQLAlchemyBase
from .meta.sqlalchemymixins import SQLAlchemyIntPK, SQLAlchemyTS


# sqlalchemy models
class Shop(SQLAlchemyTS, SQLAlchemyIntPK, SQLAlchemyBase):
    __tablename__ = "shop"
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    query_url = Column(String, nullable=False)
    render_javascript = Column(Boolean, nullable=False, default=False)
    listing_page_selector = Column(JSON, nullable=True)


class UserShops(SQLAlchemyTS, SQLAlchemyIntPK, SQLAlchemyBase):
    __tablename__ = "user_shops"
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    shop_id = Column(
        Integer, ForeignKey("shop.id", ondelete="CASCADE", onupdate="CASCADE")
    )


# pydantic models
class ShopCreate(PydanticBase):
    """Properties to receive via API on creation"""

    name: str
    url: str
    query_url: str
    render_javascript: bool
    listing_page_selector: Optional[dict]


class ShopRead(PydanticTS, ShopCreate):
    """Attributes to return via API"""

    pass


class ShopUpdate(PydanticBase):
    """Properties to receive via API on update"""

    name: Optional[str]
    url: Optional[str]
    query_url: Optional[str]
    render_javascript: Optional[bool]
    listing_page_selector: Optional[dict]
