from typing import List

import pytest
from sqlalchemy.orm import Session

from app.enums.userenums import UserStatus
from app.models import rolemodels, usermodels
from app.service import userservice
from app.service.passwordservice import verify_password
from tests import common, factories


def test_create(db_session: Session):
    email = "user@example.com"
    password = "safe_pass"
    first_name = "Michael"
    last_name = "Oliver"
    status = UserStatus.active

    user_in = usermodels.UserCreate(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        status=status,
    )

    created = userservice.create(db_session=db_session, model=user_in)
    assert created
    assert isinstance(created, usermodels.User)
    assert user_in.email == created.email
    assert not hasattr(created, "password")
    for attr in [
        "id",
        "email",
        "hashed_password",
        "first_name",
        "last_name",
        "status",
        "created_at",
        "updated_at",
    ]:
        assert hasattr(created, attr)


def test_create_with_role(db_session: Session):

    role = factories.RoleFactory(name="admin")

    email = "user@example.com"
    password = "safe_pass"
    first_name = "Michael"
    last_name = "Oliver"
    status = UserStatus.active

    user_in = usermodels.UserCreate(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        status=status,
    )

    created_with_role = userservice.create_with_role(
        db_session=db_session, model=user_in, role=role
    )
    assert created_with_role.roles[0].id == role.id


def test_get(db_session: Session):
    user: usermodels.User = factories.UserFactory()
    read = userservice.get(db_session=db_session, id_=user.id)
    assert user.id == read.id


def test_get_by_email(db_session: Session):
    user: usermodels.User = factories.UserFactory()
    read = userservice.get_by_email(db_session=db_session, email=user.email)
    assert user.id == read.id


def test_get_multiple(db_session: Session):
    users = [factories.UserFactory() for _ in range(2)]
    read = userservice.get_multiple(db_session=db_session)
    assert len(read) > 1


@pytest.mark.parametrize(
    "update_model",
    [
        usermodels.UserUpdate(first_name="newname"),
        usermodels.UserUpdate(last_name="newname"),
        usermodels.UserUpdate(password="newp@ssw0rd"),
    ],
)
def test_update(db_session: Session, update_model: usermodels.UserUpdate):
    user: usermodels.User = factories.UserFactory()
    updated = userservice.update(db_session=db_session, db_obj=user, model=update_model)
    for field in update_model.__fields_set__:
        if field == "password":
            assert verify_password(update_model.password, updated.hashed_password)
        else:
            assert getattr(updated, field) == getattr(update_model, field)


def test_delete(db_session: Session):
    user: usermodels.User = factories.UserFactory()
    userservice.delete(db_session=db_session, id_=user.id)
    assert not userservice.get(db_session=db_session, id_=user.id)


def test_authenticate(db_session: Session):
    user: usermodels.User = factories.UserFactory()
    assert userservice.authenticate(
        db_session=db_session, email=user.email, password=common.USER_PASSWORD
    )


def test_authenticate_wrong_password(db_session: Session):
    user: usermodels.User = factories.UserFactory()
    assert (
        userservice.authenticate(
            db_session=db_session, email=user.email, password="wrong"
        )
        is None
    )
