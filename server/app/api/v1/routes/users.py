from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import rolemodels, usermodels
from app.service import userservice

from ..dependencies.auth import get_current_active_user

router = APIRouter()


@router.get(
    "/", response_model=List[usermodels.UserRead],
)
def read_multiple(*, db_session: Session = Depends(get_db)):
    """Read multiple users."""
    return userservice.get_multiple(session=db_session)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=usermodels.UserRead,
)
def create_new_user(
    *, db_session: Session = Depends(get_db), user_in: usermodels.UserCreate
):
    """Create a new user."""
    if userservice.get_by_email(session=db_session, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already exists",
        )
    return userservice.create(session=db_session, model=user_in)


@router.get(
    "/me",
    response_model=usermodels.UserRead,
)
def read_current_user(
    current_user: usermodels.User = Depends(get_current_active_user)
):
    """Read the currently logged in user."""
    return current_user


@router.get(
    "/{id}",
    response_model=usermodels.UserRead,
    # dependencies=[Depends(get_current_active_superuser)],
)
def read_single_user(
    db_session: Session = Depends(get_db), user_id: int = Path(..., alias="id")
):
    """Read a single user."""
    user = userservice.get(session=db_session, id_=user_id)
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EMAIL_NOT_FOUND",
        )
    return user


@router.put(
    "/{id}",
    response_model=usermodels.UserRead,
    # dependencies=[Depends(get_current_active_superuser)],
)
def update_user(
    *,
    db_session: Session = Depends(get_db),
    user_in: usermodels.UserUpdate,
    user_id: int = Path(..., alias="id"),
):
    """Update an individual user."""

    user = userservice.get(session=db_session, id_=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND",
        )

    return userservice.update(session=db_session, db_obj=user, model=user_in)


@router.delete(
    "/{id}",
    response_model=usermodels.UserRead,
    # dependencies=[Depends(get_current_active_superuser)],
)
def delete_user(
    *, db_session: Session = Depends(get_db), user_id: int = Path(..., alias="id")
):
    """Delete an individual user."""

    user = userservice.get(session=db_session, id_=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="USER_NOT_FOUND",
        )

    return userservice.delete(session=db_session, id_=user_id)


@router.get(
    "/me/roles", response_model=List[rolemodels.RoleRead],
)
def read_current_user_roles(
    current_user: usermodels.User = Depends(get_current_active_user)
):
    return current_user.roles


@router.get(
    "/{id}/roles", response_model=List[rolemodels.RoleRead],
)
def read_user_roles(
    *, db_session: Session = Depends(get_db), user_id: int = Path(..., alias="id")
):
    user = userservice.get(session=db_session, id_=user_id)
    return user.roles
