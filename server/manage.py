import contextlib
import os
import sys

import typer
from alembic import command as alembic_cmd
from alembic.config import Config as AlembicConfig
from sqlalchemy import orm
from sqlalchemy_utils import create_database, database_exists, drop_database
from tabulate import tabulate

from app.enums.logenums import LogLevel
from app.settings import settings

DB_URL = str(settings.POSTGRES_URL)
alembic_cfg = AlembicConfig("alembic.ini")

cli = typer.Typer(add_completion=False, no_args_is_help=True)


class Messages:
    success = typer.style("Success!", fg=typer.colors.GREEN, bold=True)
    failed = typer.style("Failed!", fg=typer.colors.RED, bold=True)
    confirm = typer.style(
        "Are you sure you want to continue?", fg=typer.colors.BLUE, bold=True
    )


@cli.command
def develop(
    port: int = typer.Option(8000, help="Specify port to use."),
    loglevel: LogLevel = typer.Option(
        LogLevel.debug, case_sensitive=False, help="Set specific log level."
    ),
):

    """
    Start a development server with reload.
    """
    import uvicorn

    uvicorn.run(
        "app.main:app",
        reload=True,
        log_level=loglevel,
        port=port,
        host=settings.SERVER_HOST,
    )


@cli.command()
def routes():
    """
    Display application routes and dependencies.
    """
    from app.main import app

    tbl = []
    for route in app.routes:
        path = route.path
        methods = ",".join(route.methods)

        if hasattr(route, "dependencies"):
            dependencies = [
                str(d.dependency)
                for d in route.dependencies
                if hasattr(d, "dependency")
            ]
        else:
            dependencies = []

        tbl.append([path, methods, dependencies])

    typer.echo(
        typer.style("\nApplication Endpoints\n", bold=True)
        + tabulate(tbl, headers=["Path", "Methods", "Dependencies"])
        + "\n"
    )

    # for r in routes:
    #     print(r.name)

    # table = []
    # for r in app.routes:
    #     if not hasattr(r, "dependencies"):
    #         continue
    #     deps = [d.dependency.__name__ for d in r.dependencies]
    #     if not deps:
    #         deps = ""
    #     table.append([r.path, deps, ",".join(r.methods)])


@cli.command()
def shell():
    """
    Starts an interactive shell with app object imported.
    """
    import IPython
    from app.main import app

    IPython.embed()


@cli.command(name="config")
def config():
    """
    Display application configuration.
    """
    import json

    data = json.loads(settings.json())
    settings.schema()
    table = [[k, v] for k, v in data.items()]
    typer.echo(
        typer.style("\nApplication Configuration\n", bold=True)
        + tabulate(table, headers=["Setting", "Value(s)"])
        + "\n"
    )


@cli.command(name="initdb")
def init_database():
    """
    Initialises an empty database.
    """

    from app.db.session import SessionLocal
    from app.db.initdb import initdb

    if database_exists(DB_URL):
        typer.secho("Database already exists.", fg="red")
        raise typer.Abort
    create_database(DB_URL)

    # Run all migrations
    alembic_cmd.upgrade(config=alembic_cfg, revision="head")

    with contextlib.closing(SessionLocal()) as db_session:
        initdb(db_session=db_session)

    typer.echo(Messages.success)


@cli.command(name="dropdb", help="Drop the existing database.")
def database_drop():
    """
    Drops the current database.
    """

    typer.confirm(Messages.confirm, abort=True)

    if not database_exists(DB_URL):
        typer.secho("Database does not exist.", fg="red")
        raise typer.Abort

    drop_database(DB_URL)
    typer.echo(Messages.success)


@cli.command(help="Create a user with admin role.", no_args_is_help=True)
def createadminuser(
    email: str = typer.Argument(...),
    password: str = typer.Argument(...),
    first_name: str = typer.Argument("Admin"),
    last_name: str = typer.Argument("User"),
):
    """Add user with admin role to database."""
    import pydantic
    from app.models import usermodels
    from app.service import userservice, roleservice
    from app.enums.userenums import UserStatus
    from app.db.session import SessionLocal

    db_session = SessionLocal()

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

    with contextlib.closing(SessionLocal()) as db_session:
        # TODO: Use object instead of hard coded string
        admin_role = roleservice.get_by_name(db_session=db_session, name="admin")
        if not admin_role:
            typer.secho(
                '"admin" role does not exist, is database initialised?', fg="red"
            )
            raise typer.Abort
        userservice.create_with_role(
            db_session=db_session, user_in=adminuser, role=admin_role
        )
    typer.echo(Messages.success)


if __name__ == "__main__":
    cli()
