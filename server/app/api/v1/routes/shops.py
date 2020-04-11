from typing import List, Set

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import orm

from app.db.session import get_db
from app.models import shopmodels
from app.service import scraperservice, shopservice

from ..dependencies.auth import RoleChecker, admin_role, user_role
from ..dependencies.or_404 import get_shop_or_404

router = APIRouter()


# Populate the scrapers into memory
@router.on_event("startup")
def populate_scrapers():
    from tests.common import SessionLocal

    scraperservice.populate_scrapers(db_session=SessionLocal())


@router.get(
    "/",
    response_model=List[shopmodels.ShopRead],
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
def get_shops(*, db_session: orm.Session = Depends(get_db)):
    """
    Retrieve a list of shops.
    """
    return shopservice.get_multiple(db_session=db_session)


@router.get("/{id}", response_model=shopmodels.ShopRead)
def get_single_shop(shop: shopmodels.ShopRead = Depends(get_shop_or_404),):
    """
    Retrieve details about a specific shop.
    """
    return shop


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=shopmodels.ShopRead,
    dependencies=[Depends(admin_role)],
)
def create_shop(
    *, db_session: orm.Session = Depends(get_db), shop_in: shopmodels.ShopCreate
):
    """
    Create a new shop.
    """

    if shopservice.get_by_name(db_session=db_session, name=shop_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shop with that name already exists",
        )
    return shopservice.create(db_session=db_session, shop_in=shop_in)


@router.put(
    "/{id}", response_model=shopmodels.ShopRead, dependencies=[Depends(admin_role)]
)
def update_shop(
    *,
    db_session: orm.Session = Depends(get_db),
    shop_in: shopmodels.ShopUpdate,
    shop: shopmodels.Shop = Depends(get_shop_or_404),
):
    """
    Update an individual shop.
    """

    return shopservice.update(db_session=db_session, shop=shop, shop_in=shop_in)


@router.delete(
    "/{id}", response_model=shopmodels.ShopRead, dependencies=[Depends(admin_role)]
)
def delete_shop(
    *,
    db_session: orm.Session = Depends(get_db),
    shop: shopmodels.Shop = Depends(get_shop_or_404),
):
    """
    Delete an individual shop.
    """

    return shopservice.delete(db_session=db_session, id_=shop.id)


@router.get("/listings/", dependencies=[Depends(admin_role)])
async def read_multiple_shops_listings(
    query: str = Query(..., description="The search term to query by."),
    limit: int = Query(10, description="The number of results to return.", ge=1, le=40),
    include: Set[int] = Query(..., description="Shop IDs to query for listings."),
):
    """
    Scrape multiple shops for listings in real time.
    """

    return await scraperservice.query_scrapers(
        query=query, limit=limit, include=include
    )
