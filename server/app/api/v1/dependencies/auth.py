import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import orm

from app.db.session import get_db
from app.enums.userenums import UserStatus
from app.models import tokenmodels, usermodels
from app.service import tokenservice, userservice

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


ADMIN_ROLE = "admin"
USER_ROLE = "user"


def get_current_user(
    db_session: orm.Session = Depends(get_db), token: str = Security(reusable_oauth2)
) -> usermodels.User:
    """Route dependency to return the current user."""
    try:
        payload = tokenservice.decode(token=token, audience=tokenservice.AUTH_AUDIENCE)
        token_data = tokenmodels.JWTAccessToken(**payload)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="JWT has expired"
        )

    except jwt.InvalidAudienceError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect JWT audience."
        )

    user = userservice.get(db_session=db_session, id_=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="EMAIL_NOT_FOUND"
        )
    return user


def get_current_active_user(current_user: usermodels.User = Security(get_current_user)):
    if current_user.status == UserStatus.inactive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Specified user is not active.",
        )
    elif current_user.status == UserStatus.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Specified user is disabled."
        )
    return current_user


class RoleChecker:
    def __init__(self, role: str):
        self.role = role

    def __call__(
        self, current_user: usermodels.User = Security(get_current_active_user)
    ):
        if self.role not in [role.name for role in current_user.roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user does not have enough privilege's to access this resource.",
            )
        return current_user


# Define roles here
user_role = RoleChecker(USER_ROLE)
admin_role = RoleChecker(ADMIN_ROLE)
