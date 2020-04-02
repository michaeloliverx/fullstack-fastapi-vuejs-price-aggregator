import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import apirouter
from .settings import settings

log = logging.getLogger(__name__)

app = FastAPI(debug=settings.DEBUG, title=settings.PROJECT_NAME)

# TODO: Add correct local CORS origins to .env file, atm everything is allowed
if settings.CORS_WHITELIST:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(router=apirouter.router, prefix="/api")
