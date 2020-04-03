from typing import List

from sqlalchemy.orm import Session

from app.models import rolemodels
from app.service import roleservice


def test_create(session: Session):

    name = "admin"
    description = "admin desc"

    role_in = rolemodels.RoleCreate(name=name, description=description)

    created = roleservice.create(session=session, role_in=role_in)
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


def test_create_multiple(session: Session):
    roles_data = [
        {"name": "admin", "description": "Administrator"},
        {"name": "user", "description": "User"},
    ]
    roles_in = [
        rolemodels.RoleCreate(name=role["name"], description=role["description"])
        for role in roles_data
    ]
    created_roles = roleservice.create_multiple(session=session, roles_in=roles_in)
    assert len(created_roles) == len(roles_in)


def test_get(session: Session, role: rolemodels.Role):
    read = roleservice.get(session=session, id_=role.id)
    assert read.id == role.id


def test_get_by_name(session: Session, role: rolemodels.Role):
    read = roleservice.get_by_name(session=session, name=role.name)
    assert read.id == role.id


def test_get_multiple(session: Session, roles: List[rolemodels.Role]):
    read = roleservice.get_multiple(session=session)
    assert len(read) > 1


def test_delete(session: Session, role: rolemodels.Role):
    roleservice.delete(session=session, id_=role.id)
    assert not roleservice.get(session=session, id_=role.id)
