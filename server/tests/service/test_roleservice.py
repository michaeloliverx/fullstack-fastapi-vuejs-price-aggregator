from typing import List

import pytest
from sqlalchemy.orm import Session

from app.models import rolemodels
from app.service import roleservice
from tests import factories


def test_create(db_session: Session):

    name = "admin"
    description = "admin desc"

    role_in = rolemodels.RoleCreate(name=name, description=description)

    created = roleservice.create(db_session=db_session, role_in=role_in)
    assert created
    assert isinstance(created, rolemodels.Role)
    for attr in [
        "id",
        "created_at",
        "updated_at",
        "name",
        "description",
    ]:
        assert hasattr(created, attr)


def test_create_multiple(db_session: Session):
    roles_data = [
        {"name": "admin", "description": "Administrator"},
        {"name": "user", "description": "User"},
    ]
    roles_in = [
        rolemodels.RoleCreate(name=role["name"], description=role["description"])
        for role in roles_data
    ]
    created_roles = roleservice.create_multiple(
        db_session=db_session, roles_in=roles_in
    )
    assert len(created_roles) == len(roles_in)


def test_get(db_session: Session):
    role = factories.RoleFactory(name="admin")
    read = roleservice.get(db_session=db_session, id_=role.id)
    assert read.id == role.id


def test_get_by_name(db_session: Session):
    role = factories.RoleFactory(name="user")
    read = roleservice.get_by_name(db_session=db_session, name=role.name)
    assert read.id == role.id


def test_get_multiple(db_session: Session):
    roles = [factories.RoleFactory(name="admin"), factories.RoleFactory(name="user")]
    read = roleservice.get_multiple(db_session=db_session)
    assert len(read) > 1


def test_update(db_session: Session):
    role = factories.RoleFactory(name="user")
    role_in = rolemodels.RoleUpdate(description="More descriptive description.")
    updated = roleservice.update(db_session=db_session, role=role, role_in=role_in)
    for field in role_in.__fields_set__:
        assert getattr(updated, field) == getattr(role_in, field)


def test_delete(db_session: Session):
    role = factories.RoleFactory(name="admin")
    roleservice.delete(db_session=db_session, id_=role.id)
    assert not roleservice.get(db_session=db_session, id_=role.id)
