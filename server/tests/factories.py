from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyText
from pytz import UTC

from app.enums import roleenums, userenums
from app.models import rolemodels, usermodels
from app.service.passwordservice import get_password_hash

from .common import USER_PASSWORD, ScopedSession


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = ScopedSession
        sqlalchemy_session_persistence = "flush"


class TimeStampBaseFactory(BaseFactory):
    """Timestamp Base Factory."""

    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=UTC))


class UserFactory(TimeStampBaseFactory, BaseFactory):
    """User Factory."""

    email = Faker("email")
    hashed_password = get_password_hash(USER_PASSWORD)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    status = FuzzyChoice(userenums.UserStatus)

    class Meta:
        model = usermodels.User


class RoleFactory(TimeStampBaseFactory, BaseFactory):
    """Role factory."""

    name = FuzzyChoice(roleenums.RoleName)
    description = FuzzyText()

    class Meta:
        model = rolemodels.Role
