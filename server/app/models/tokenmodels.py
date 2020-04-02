from .meta.pydanticbase import PydanticBase


class TokenResponse(PydanticBase):
    access_token: str
    token_type: str


class JWTAccessToken(PydanticBase):
    exp: int
    user_id: int
