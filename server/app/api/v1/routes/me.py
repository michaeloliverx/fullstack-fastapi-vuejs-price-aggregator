from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import rolemodels, shopmodels, usermodels
from app.service import shopservice, userservice

from ..dependencies.auth import get_current_active_user

router = APIRouter()


@router.get(
    "/me",
    response_model=usermodels.UserRead,
    dependencies=[Depends(get_current_active_user)],
)
def read_current_user(current_user: usermodels.User = Depends(get_current_active_user)):
    """Read the currently logged in user."""
    return current_user


@router.put(
    "/me", response_model=usermodels.UserRead,
)
def update_current_user(
    *,
    db_session: Session = Depends(get_db),
    current_user: usermodels.User = Depends(get_current_active_user),
    user_in: usermodels.UserUpdateMe,
):
    """Update the currently logged in user."""

    return userservice.update(db_session=db_session, user=current_user, user_in=user_in)


@router.get(
    "/me/roles", response_model=List[rolemodels.RoleRead],
)
def read_current_user_roles(
    current_user: usermodels.User = Depends(get_current_active_user),
):
    """Read the currently logged in user roles"""
    return current_user.roles


@router.get(
    "/me/shops", response_model=List[shopmodels.ShopRead],
)
def read_current_user_shops(
    current_user: usermodels.User = Depends(get_current_active_user),
):
    """
    Retrieve a list of shops assigned to the currently logged in user.
    """
    return current_user.shops


@router.put(
    "/me/shops", response_model=List[shopmodels.ShopRead],
)
def update_user_shops(
    *,
    db_session: Session = Depends(get_db),
    current_user: usermodels.User = Depends(get_current_active_user),
    shops_ids: List[int] = Body(...),
):
    """
    Update the assigned shops of the currently logged in user.
    """

    shop_objs = shopservice.get_multiple_by_ids(db_session=db_session, ids_=shops_ids)

    if len(shop_objs) != len(shops_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One of the specified shops was not found man.",
        )

    current_user.shops = shop_objs
    db_session.commit()
    return shop_objs
