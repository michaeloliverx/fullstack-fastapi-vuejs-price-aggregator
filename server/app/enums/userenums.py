from enum import Enum


class UserStatus(str, Enum):
    """
    UserStatus enum.

    active: User account is active.
    inactive: User account is inactive, perhaps email has not been validated.
    disabled: User has been disabled, perhaps banned by an administrator.
    """

    active = "active"
    inactive = "inactive"
    disabled = "disabled"
