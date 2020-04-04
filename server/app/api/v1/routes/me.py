from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import rolemodels, usermodels
from app.service import userservice

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
