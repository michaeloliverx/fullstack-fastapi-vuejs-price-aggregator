from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import orm

from app.db.session import get_db
from app.models import rolemodels, usermodels
from app.service import roleservice, userservice


def get_role_or_404(
    db_session: orm.Session = Depends(get_db),
    role_id: int = Path(..., alias="id", ge=1),
) -> rolemodels.Role:
    """
    Route dependency that retrieves a role by id or raises 404.
    """
    role = roleservice.get(db_session=db_session, id_=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified role was not found.",
        )
    return role


def get_user_or_404(
    db_session: orm.Session = Depends(get_db),
    user_id: int = Path(..., alias="id", ge=1),
) -> usermodels.User:
    """
    Route dependency that retrieves a user by id or raises 404.
    """
    user = userservice.get(db_session=db_session, id_=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified user was not found.",
        )
    return user
