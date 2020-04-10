from typing import List

import pytest
from sqlalchemy.orm import Session

from app.models import shopmodels
from app.service import shopservice
from tests import factories


def test_create(db_session: Session):

    name = "tesco"
    url = "www.tesco.com"
    query_url = "/groceries/en-GB/search?query={query}"
    render_javascript = False
    listing_page_selector = {}

    shop_in = shopmodels.ShopCreate(
        name=name,
        url=url,
        query_url=query_url,
        render_javascript=render_javascript,
        listing_page_selector=listing_page_selector,
    )

    created = shopservice.create(db_session=db_session, shop_in=shop_in)

    assert created
    assert isinstance(created, shopmodels.Shop)
    for attr in [
        "id",
        "created_at",
        "updated_at",
        "name",
        "url",
        "name",
        "query_url",
        "render_javascript",
        "listing_page_selector",
    ]:
        assert hasattr(created, attr)


def test_get(db_session: Session):
    shop = factories.ShopFactory()
    read = shopservice.get(db_session=db_session, id_=shop.id)
    assert read.id == shop.id


def test_get_by_name(db_session: Session):
    name = "tesco"
    shop = factories.ShopFactory(name=name)
    read = shopservice.get_by_name(db_session=db_session, name=name)
    assert read.id == shop.id


def test_get_multiple(db_session: Session):
    shops = [factories.ShopFactory() for _ in range(3)]
    read = shopservice.get_multiple(db_session=db_session)
    assert len(read) > 1


def test_update(db_session: Session):
    shop = factories.ShopFactory()
    shop_in = shopmodels.ShopUpdate(listing_page_selector={"updated": "selector"})
    updated = shopservice.update(db_session=db_session, shop=shop, shop_in=shop_in)
    for field in shop_in.__fields_set__:
        assert getattr(updated, field) == getattr(shop_in, field)


def test_delete(db_session: Session):
    shop = factories.ShopFactory()
    shopservice.delete(db_session=db_session, id_=shop.id)
    assert not shopservice.get(db_session=db_session, id_=shop.id)
