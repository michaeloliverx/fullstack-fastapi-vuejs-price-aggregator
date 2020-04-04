from typing import Dict, List

import yaml
from sqlalchemy import engine, orm

from app.models import rolemodels, usermodels
from app.service import roleservice, userservice
from app.settings import settings

INITDB_PATH = settings.APP_DIR / "db" / "initdb.yaml"
with open(INITDB_PATH) as file:
    config = yaml.safe_load(file)


def initdb(db_session: orm.Session):
    init_roles(db_session=db_session)


def init_roles(db_session: orm.Session):
    roles_in = [
        rolemodels.RoleCreate(name=role["name"], description=role["description"])
        for role in config["roles"]
    ]
    roleservice.create_multiple(db_session=db_session, roles_in=roles_in)


def setup_guids_postgresql(engine: engine.Engine) -> None:  # pragma: no cover
    """
    Set up UUID generation using the pgcrypto extension for postgres
    This query only needs to be executed once when the database is created
    """
    engine.execute('create EXTENSION if not EXISTS "pgcrypto"')
