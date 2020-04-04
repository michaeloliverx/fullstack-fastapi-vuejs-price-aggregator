from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import rolemodels, usermodels
from app.service import userservice

from ..dependencies.or_404 import get_user_or_404

router = APIRouter()


@router.get(
    "/", response_model=List[usermodels.UserRead],
)
def get_users(*, db_session: Session = Depends(get_db)):
    """
    Retrieve a list of users.
    """
    return userservice.get_multiple(db_session=db_session)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=usermodels.UserRead,
)
def create_user(
    *, db_session: Session = Depends(get_db), user_in: usermodels.UserCreate
):
    """
    Create a new user.
    """
    if userservice.get_by_email(db_session=db_session, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address already exists",
        )
    return userservice.create(db_session=db_session, user_in=user_in)


@router.get(
    "/{id}", response_model=usermodels.UserRead,
)
def get_user(user: usermodels.User = Depends(get_user_or_404),):
    """
    Retrieve details about a specific user.
    """
    return user


@router.put(
    "/{id}", response_model=usermodels.UserRead,
)
def update_user(
    *,
    db_session: Session = Depends(get_db),
    user_in: usermodels.UserUpdate,
    user: usermodels.User = Depends(get_user_or_404),
):
    """
    Update an individual user.
    """

    return userservice.update(db_session=db_session, user=user, user_in=user_in)


@router.delete(
    "/{id}", response_model=usermodels.UserRead,
)
def delete_user(
    *,
    db_session: Session = Depends(get_db),
    user: usermodels.User = Depends(get_user_or_404),
):
    """
    Delete an individual user.
    """

    return userservice.delete(db_session=db_session, id_=user.id)


@router.get(
    "/{id}/roles", response_model=List[rolemodels.RoleRead],
)
def read_user_roles(user: usermodels.User = Depends(get_user_or_404),):
    """
    Retrieve a list of roles assigned to an individual user.
    """
    return user.roles
