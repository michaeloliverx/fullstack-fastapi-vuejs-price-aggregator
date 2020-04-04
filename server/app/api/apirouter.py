from fastapi import APIRouter

from .v1 import v1_router

router = APIRouter()
router.include_router(router=v1_router.router, prefix="/v1")


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
