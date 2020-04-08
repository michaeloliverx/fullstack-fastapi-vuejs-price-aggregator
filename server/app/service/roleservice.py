from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.rolemodels import Role, RoleCreate, RoleUpdate


def get(db_session: Session, id_: int) -> Optional[Role]:
    return db_session.query(Role).filter(Role.id == id_).first()


def get_by_name(db_session: Session, name: str) -> Optional[Role]:
    return db_session.query(Role).filter(Role.name == name).first()


def get_multiple(
    db_session: Session, *, offset: int = 0, limit: int = 100
) -> List[Role]:
    return db_session.query(Role).offset(offset).limit(limit).all()


def get_multiple_by_ids(db_session: Session, *, ids_: List[int]) -> List[Role]:
    return db_session.query(Role).filter(Role.id.in_(ids_)).all()


def create(db_session: Session, role_in: RoleCreate) -> Role:
    db_obj = Role(name=role_in.name, description=role_in.description)
    db_session.add(db_obj)
    db_session.commit()
    return db_obj


def create_multiple(db_session: Session, roles_in: List[RoleCreate]) -> List[Role]:
    db_objs = [Role(name=role.name, description=role.description) for role in roles_in]
    db_session.add_all(db_objs)
    db_session.commit()
    return db_objs


def update(db_session: Session, role: Role, role_in: RoleUpdate) -> Role:
    update_data = role_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(role, field, update_data[field])

    db_session.add(role)
    db_session.commit()
    return role


def delete(db_session: Session, *, id_: int):
    obj = db_session.query(Role).get(id_)
    db_session.delete(obj)
    db_session.commit()
