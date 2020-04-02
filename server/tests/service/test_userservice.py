from typing import List

import pytest
from sqlalchemy.orm import Session

from app.enums.userenums import UserStatus
from app.models import rolemodels, usermodels
from app.service import userservice
from app.service.passwordservice import verify_password

from ..common import USER_PASSWORD


def test_create(session: Session):
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

    created = userservice.create(session=session, model=user_in)
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


def test_create_with_role(session: Session, role: rolemodels.Role):

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
        session=session, model=user_in, role=role
    )
    assert created_with_role.roles[0].id == role.id


def test_get(session: Session, user: usermodels.User):
    read = userservice.get(session=session, id_=user.id)
    assert user.id == read.id


def test_get_by_email(session: Session, user: usermodels.User):
    read = userservice.get_by_email(session=session, email=user.email)
    assert user.id == read.id


def test_get_multiple(session: Session, users: List[usermodels.User]):
    read = userservice.get_multiple(session=session)
    assert len(read) > 1


@pytest.mark.parametrize(
    "update_model",
    [
        usermodels.UserUpdate(first_name="newname"),
        usermodels.UserUpdate(last_name="newname"),
        usermodels.UserUpdate(password="newp@ssw0rd"),
    ],
)
def test_update(
    session: Session, user: usermodels.User, update_model: usermodels.UserUpdate
):

    updated = userservice.update(session=session, db_obj=user, model=update_model)
    for field in update_model.__fields_set__:
        if field == "password":
            assert verify_password(update_model.password, updated.hashed_password)
        else:
            assert getattr(updated, field) == getattr(update_model, field)


def test_delete(session: Session, user: usermodels.User):
    userservice.delete(session=session, id_=user.id)
    assert not userservice.get(session=session, id_=user.id)


def test_authenticate(session: Session, user: usermodels.User):
    assert userservice.authenticate(
        session=session, email=user.email, password=USER_PASSWORD
    )


def test_authenticate_wrong_password(session: Session, user: usermodels.User):
    assert (
        userservice.authenticate(session=session, email=user.email, password="wrong")
        is None
    )
