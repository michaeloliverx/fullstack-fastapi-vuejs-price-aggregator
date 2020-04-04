from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import orm

from app.db.session import get_db
from app.enums import userenums
from app.models import tokenmodels, usermodels
from app.service import tokenservice, userservice
from app.settings import settings

from ..dependencies.auth import get_current_user, verify_admin_role

router = APIRouter()


@router.post("/login", response_model=tokenmodels.TokenResponse)
def login(
    *,
    db_session: orm.Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = userservice.authenticate(
        db_session=db_session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="REPLACE ME",
        )

    elif not user.status == userenums.UserStatus.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="USER_INACTIVE"
        )

    # TODO: maybe ? add custom encoder like ujson/orjson to encode method
    token = tokenservice.encode(
        payload={"user_id": str(user.id), "aud": tokenservice.AUTH_AUDIENCE},
        lifetime_seconds=settings.JWT_AUTH_LIFETIME_SECONDS,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout():
    return {"logout-status": "successful"}


@router.post("/login/test-token", response_model=usermodels.UserRead)
def test_token(current_user: usermodels.User = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.post("/login/test-admin-role", response_model=usermodels.UserRead)
def test_role(current_user: usermodels.User = Depends(verify_admin_role)):
    return current_user
