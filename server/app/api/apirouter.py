from fastapi import APIRouter

from .v1 import v1router

router = APIRouter()
router.include_router(router=v1router.router, prefix="/v1")


@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
