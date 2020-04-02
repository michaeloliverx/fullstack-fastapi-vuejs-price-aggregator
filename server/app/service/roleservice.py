from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.rolemodels import Role, RoleCreate, RoleUpdate


def get(session: Session, id_: int) -> Optional[Role]:
    return session.query(Role).filter(Role.id == id_).first()


def get_by_name(*, session: Session, name: str) -> Optional[Role]:
    return session.query(Role).filter(Role.name == name).first()


def get_multiple(session: Session, *, offset: int = 0, limit: int = 100) -> List[Role]:
    return session.query(Role).offset(offset).limit(limit).all()


def create(session: Session, role_in: RoleCreate) -> Role:
    db_obj = Role(name=role_in.name, description=role_in.description)
    session.add(db_obj)
    session.commit()
    return db_obj


def create_multiple(session: Session, roles_in: List[RoleCreate]) -> List[Role]:
    db_objs = [Role(name=role.name, description=role.description) for role in roles_in]
    session.add_all(db_objs)
    session.commit()
    return db_objs


def update(*, session: Session, role: Role, role_in: RoleUpdate) -> Role:
    update_data = role_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(role, field, update_data[field])

    session.add(role)
    session.commit()
    return role


def delete(session: Session, *, id_: int):
    obj = session.query(Role).get(id_)
    session.delete(obj)
    session.commit()
