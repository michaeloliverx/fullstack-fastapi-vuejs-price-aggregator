import sys

import click_spinner
import typer
from alembic import command as alembic_cmd
from alembic.config import Config as AlembicConfig
from sqlalchemy_utils import create_database, database_exists, drop_database
from tabulate import tabulate

from app.enums.logenums import LogLevel
from app.settings import settings

DB_URL = str(settings.POSTGRES_URL)
alembic_cfg = AlembicConfig("alembic.ini")

SUCCESS = typer.style("Success!", fg="green", bold=True)


cli = typer.Typer(add_completion=False, no_args_is_help=True)

app = typer.Typer(add_completion=False, help="Application specific commands.")
db = typer.Typer(add_completion=False, help="Database specific commands.")


@cli.command(help="Start a development server with reload.")
def develop(
    port: int = typer.Option(8000, help="Specify port to use."),
    loglevel: LogLevel = typer.Option(
        LogLevel.debug, case_sensitive=False, help="Set specific log level."
    ),
):

    """Start a development server with reload."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        reload=True,
        log_level=loglevel,
        port=port,
        host=settings.SERVER_HOST,
    )


@cli.command(name="routes")
def routes():
    """Display application routes and dependencies."""
    from app.main import app

    table = []
    for r in app.routes:
        if not hasattr(r, "dependencies"):
            continue
        deps = [d.dependency.__name__ for d in r.dependencies]
        if not deps:
            deps = ""
        table.append([r.path, deps, ",".join(r.methods)])
    typer.echo(
        typer.style("\nApplication Endpoints\n", bold=True)
        + tabulate(table, headers=["Path", "Dependencies", "Methods"])
        + "\n"
    )


@cli.command(name="shell")
def shell():
    """Starts an interactive shell with app object imported."""
    import IPython
    from app.main import app

    IPython.embed()


@cli.command(name="config")
def config():
    """Display application configuration."""
    import json

    data = json.loads(settings.json())
    settings.schema()
    table = [[k, v] for k, v in data.items()]
    typer.echo(
        typer.style("\nApplication Configuration\n", bold=True)
        + tabulate(table, headers=["Setting", "Value(s)"])
        + "\n"
    )


@cli.command(name="initdb", help="Initialises an empty database.")
def database_init():
    from app.db.session import SessionLocal
    from app.db.initdb import initdb

    if database_exists(DB_URL):
        typer.secho("Database already exists.", fg="red")
        raise typer.Abort
    create_database(DB_URL)
    alembic_cmd.upgrade(config=alembic_cfg, revision="head")
    session = SessionLocal()
    initdb(session=session)
    typer.secho("Success!", fg="green", bold=True)


@cli.command(name="dropdb", help="Drop the existing database.")
def database_drop():
    """Drops the current database"""
    typer.confirm("Are you sure you want to delete it?", abort=True)

    if not database_exists(DB_URL):
        typer.secho("Database does not exist.", fg="red")
        raise typer.Abort
    drop_database(DB_URL)
    typer.secho("Success!", fg="green", bold=True)


@cli.command(help="Create a user with admin role.", no_args_is_help=True)
def createadminuser(
    email: str = typer.Argument(...),
    password: str = typer.Argument(...),
    first_name: str = typer.Argument("Admin"),
    last_name: str = typer.Argument("User"),
):
    """Add superuser to database."""
    import pydantic
    from app.models import usermodels
    from app.service import userservice, roleservice
    from app.enums.userenums import UserStatus
    from app.db.session import SessionLocal

    session = SessionLocal()

    try:
        adminuser = usermodels.UserCreate(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            status=UserStatus.active,
        )
    except pydantic.ValidationError as e:
        typer.secho(f"Validation error for user: \n {str(e)}", fg="red")
        raise typer.Abort

    adminrole = roleservice.get_by_name(session=session, name="admin")
    if not adminrole:
        typer.secho('"admin" role does not exist, is database initialised?', fg="red")
        raise typer.Abort

    userservice.create_with_role(session=session, model=adminuser, role=adminrole)
    typer.echo(SUCCESS)


if __name__ == "__main__":
    cli()
