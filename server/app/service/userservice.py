from typing import List, Optional, Union

from sqlalchemy.orm import Session

from app.models import rolemodels
from app.models.usermodels import User, UserCreate, UserUpdate, UserUpdateMe
from app.service.passwordservice import get_password_hash, verify_password


def get(db_session: Session, id_: int) -> Optional[User]:
    return db_session.query(User).filter(User.id == id_).first()


def get_by_email(db_session: Session, email: str) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def get_multiple(
    db_session: Session, *, offset: int = 0, limit: int = 100
) -> List[User]:
    return db_session.query(User).offset(offset).limit(limit).all()


def create(db_session: Session, model: UserCreate) -> User:
    db_obj = User(
        email=model.email,
        hashed_password=get_password_hash(model.password),
        first_name=model.first_name,
        last_name=model.last_name,
        status=model.status,
    )
    db_session.add(db_obj)
    db_session.commit()
    return db_obj


def create_with_role(
    db_session: Session, model: UserCreate, role: rolemodels.Role
) -> User:
    db_obj = User(
        email=model.email,
        hashed_password=get_password_hash(model.password),
        first_name=model.first_name,
        last_name=model.last_name,
        status=model.status,
    )
    db_obj.roles = [role]
    db_session.add(db_obj)
    db_session.commit()
    return db_obj


def update(
    db_session: Session, db_obj: User, model: Union[UserUpdate, UserUpdateMe]
) -> User:

    update_data = model.dict(exclude_defaults=True, exclude_unset=True)
    if "password" in update_data:
        plainpass = update_data.pop("password")
        hashedpass = get_password_hash(plainpass)
        update_data["hashed_password"] = hashedpass

    for field in update_data:
        if hasattr(db_obj, field):
            setattr(db_obj, field, update_data[field])

    db_session.add(db_obj)
    db_session.commit()
    return db_obj


def delete(db_session: Session, id_: int):
    db_session.query(User).filter(User.id == id_).delete()
    db_session.commit()


def authenticate(db_session: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db_session=db_session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
