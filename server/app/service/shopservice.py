from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.shopmodels import Shop, ShopCreate, ShopUpdate


def get(db_session: Session, id_: int) -> Optional[Shop]:
    return db_session.query(Shop).filter(Shop.id == id_).first()


def get_by_name(db_session: Session, name: str) -> Optional[Shop]:
    return db_session.query(Shop).filter(Shop.name == name).first()


def get_multiple(
    db_session: Session, *, offset: int = 0, limit: int = 100
) -> List[Shop]:
    return db_session.query(Shop).offset(offset).limit(limit).all()


def get_multiple_by_ids(db_session: Session, *, ids_: List[int]) -> List[Shop]:
    return db_session.query(Shop).filter(Shop.id.in_(ids_)).all()


def create(db_session: Session, shop_in: ShopCreate) -> Shop:

    db_obj = Shop(
        name=shop_in.name,
        url=shop_in.url,
        query_url=shop_in.query_url,
        render_javascript=shop_in.render_javascript,
        listing_page_selector=shop_in.listing_page_selector,
    )

    db_session.add(db_obj)
    db_session.commit()
    return db_obj


def update(db_session: Session, shop: Shop, shop_in: ShopUpdate) -> Shop:
    update_data = shop_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(shop, field, update_data[field])
    db_session.add(shop)
    db_session.commit()
    return shop


def delete(db_session: Session, id_: int) -> None:
    obj = db_session.query(Shop).get(id_)
    db_session.delete(obj)
    db_session.commit()
