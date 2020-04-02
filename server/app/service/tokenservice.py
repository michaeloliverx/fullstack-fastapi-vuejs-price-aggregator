from datetime import datetime, timedelta
from typing import Union

import jwt

from app.settings import settings

ALGORITHM: str = "HS256"

AUTH_AUDIENCE = "auth-login"


def decode(token: str, **jwtkwargs) -> dict:
    return jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY.get_secret_value(),
        algorithms=[ALGORITHM],
        **jwtkwargs,
    )


def encode(payload: dict, lifetime_seconds: Union[int, float]) -> str:
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM,
    ).decode("utf-8")
    return encoded_jwt
