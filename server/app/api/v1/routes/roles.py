from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import rolemodels
from app.service import roleservice

from ..dependencies.or_404 import get_role_by_id_or_404

router = APIRouter()


@router.get(
    "/", response_model=List[rolemodels.RoleRead],
)
def get_roles(*, db_session: Session = Depends(get_db)):
    """
    Retrieve a list of roles.
    """
    return roleservice.get_multiple(db_session=db_session)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=rolemodels.RoleRead,
)
def create_role(
    *, db_session: Session = Depends(get_db), role_in: rolemodels.RoleCreate
):
    """
    Create a new role.
    """
    if roleservice.get_by_name(db_session=db_session, name=role_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists.",
        )

    return roleservice.create(db_session=db_session, role_in=role_in)


@router.get("/{id}", response_model=rolemodels.RoleRead)
def read_role(role: rolemodels.Role = Depends(get_role_by_id_or_404),):
    """
    Retrieve details about a specific role.
    """
    return role


@router.put(
    "/{id}", response_model=rolemodels.RoleRead,
)
def update_role(
    *,
    db_session: Session = Depends(get_db),
    role: rolemodels.Role = Depends(get_role_by_id_or_404),
    role_in: rolemodels.RoleUpdate,
):
    """
    Update an individual role.
    """

    return roleservice.update(db_session=db_session, role=role, role_in=role_in)


@router.delete(
    "/{id}", response_model=rolemodels.RoleRead,
)
def delete_role(
    *,
    db_session: Session = Depends(get_db),
    role: rolemodels.Role = Depends(get_role_by_id_or_404),
):
    """
    Delete an individual role.
    """
    return roleservice.delete(db_session=db_session, id_=role.id)
