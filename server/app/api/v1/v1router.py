from fastapi import APIRouter

from .routes import auth, roles, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(roles.router, prefix="/roles", tags=["roles"])
