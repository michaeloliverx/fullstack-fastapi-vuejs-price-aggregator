from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import rolemodels
from app.service import roleservice

router = APIRouter()


@router.get(
    "/", response_model=List[rolemodels.RoleRead],
)
def read_multiple(*, db_session: Session = Depends(get_db)):
    """Read multiple roles."""
    return roleservice.get_multiple(session=db_session)
