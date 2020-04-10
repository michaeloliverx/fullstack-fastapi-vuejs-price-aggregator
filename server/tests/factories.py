import random
from datetime import datetime

import factory
import pytz
from factory.alchemy import SQLAlchemyModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyDateTime, FuzzyText

from app.enums import userenums
from app.models import rolemodels, shopmodels, usermodels
from app.service.passwordservice import get_password_hash

from . import common


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = common.ScopedSession
        sqlalchemy_session_persistence = "commit"


class TimeStampFactory(BaseFactory):
    """Timestamp Base Factory."""

    created_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=pytz.UTC))
    updated_at = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=pytz.UTC))


class UserFactory(TimeStampFactory, BaseFactory):
    """User Factory.
    Has a default password and active status.
    """

    class Meta:
        model = usermodels.User

    email = Faker("email")
    hashed_password = get_password_hash(common.USER_PASSWORD)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    status = userenums.UserStatus.active

    # Relationships
    @factory.post_generation
    def roles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of roles were passed in, use them
            for role in extracted:
                self.roles.append(role)


class RoleFactory(TimeStampFactory, BaseFactory):
    """Role factory."""

    class Meta:
        model = rolemodels.Role

    name = FuzzyText()
    description = FuzzyText()


class ShopFactory(TimeStampFactory, BaseFactory):
    """Shop factory."""

    class Meta:
        model = shopmodels.Shop

    name = FuzzyText()
    url = FuzzyText()
    query_url = FuzzyText()
    render_javascript = Faker("boolean")
    listing_page_selector = {"data": "here"}
