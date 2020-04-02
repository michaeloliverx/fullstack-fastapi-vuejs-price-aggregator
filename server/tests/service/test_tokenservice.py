import time

import jwt
import pytest

from app.service import tokenservice

# jwt.ExpiredSignatureError
# jwt.InvalidAudienceError


def test_token():
    """Tests the encode and decode of a json web token."""
    audience = "login-token"
    data = {"user_id": 1, "aud": audience}

    token = tokenservice.encode(payload=data, lifetime_seconds=10)
    assert isinstance(token, str)

    decoded = tokenservice.decode(token=token, audience=audience)
    assert decoded["user_id"] == data["user_id"]


def test_token_expired():
    """Tests expired tokens raise an exception."""
    data = {"foo": "bar"}
    token = tokenservice.encode(payload=data, lifetime_seconds=0.1)
    time.sleep(1)
    with pytest.raises(jwt.ExpiredSignatureError):
        tokenservice.decode(token=token)


def test_token_invalid_audience():
    """Tests wrong audience raises an exception"""
    audience = "foo"
    data = {"user_id": 1, "aud": audience}
    token = tokenservice.encode(payload=data, lifetime_seconds=10)

    # Wrong audience claim
    with pytest.raises(jwt.InvalidAudienceError):
        tokenservice.decode(token=token, audience="bar")

    # No audience claim
    with pytest.raises(jwt.InvalidAudienceError):
        tokenservice.decode(token=token)
