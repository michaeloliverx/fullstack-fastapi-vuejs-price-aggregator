import enum

from fastapi import HTTPException, status

AUTHENTICATION_FAILED = "Could not validate credentials."
FORBIDDEN = "You are not authorized to access this resource."
REGISTRATION_CLOSED = "Open user registration is forbidden on this server"

USER_EXISTS = "Email address is already in use."
USER_INACTIVE = "User is inactive."

_NOT_FOUND = "{item} not found."
USER_NOT_FOUND = _NOT_FOUND.format(item="User")

EMAIL_NOT_FOUND = _NOT_FOUND.format(item="Email address")
