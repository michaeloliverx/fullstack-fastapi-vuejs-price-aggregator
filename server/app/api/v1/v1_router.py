from fastapi import APIRouter, Depends

from .dependencies.auth import admin_role
from .routes import auth, me, roles, users

router = APIRouter()
router.include_router(router=auth.router, prefix="/auth", tags=["auth"])
router.include_router(router=me.router, tags=["self"])
router.include_router(
    router=users.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(admin_role)],
)
router.include_router(
    router=roles.router,
    prefix="/roles",
    tags=["roles"],
    dependencies=[Depends(admin_role)],
)
