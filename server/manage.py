import contextlib

import click_spinner
import pydantic
import typer
from tabulate import tabulate

from app.db.initdb import initdb
from app.enums import logenums, userenums
from app.main import app
from app.models import rolemodels, usermodels
from app.service import roleservice, userservice
from app.settings import settings

DB_URL = str(settings.POSTGRES_URL)


# Utilities
def create_database_if_not_exists():
    """
    Create database if it doesn't already exist.
    Runs migrations using alembic to bring it up to spec.
    """

    from sqlalchemy_utils import create_database, database_exists
    from alembic import command as alembic_cmd
    from alembic.config import Config as AlembicConfig

    alembic_cfg = AlembicConfig("alembic.ini")

    if database_exists(DB_URL):
        typer.secho("Database already exists.", fg="red")
        raise typer.Abort
    create_database(DB_URL)

    # Run all migrations
    alembic_cmd.upgrade(config=alembic_cfg, revision="head")


@contextlib.contextmanager
def existing_database():
    """
    Context manager that returns a database session that closes.
    """
    from sqlalchemy import orm
    from sqlalchemy_utils import database_exists
    from app.db.session import SessionLocal

    if not database_exists(DB_URL):
        typer.secho("Database does not exist.", fg="red")
        raise typer.Abort

    _db_session: orm.Session = SessionLocal()
    yield _db_session
    _db_session.close()


@contextlib.contextmanager
def catch_validation_err():
    """
    Catch pydantic validation errors and display pretty message.
    """
    try:
        yield
    except pydantic.ValidationError as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True)
        raise typer.Abort


class Messages:
    success = typer.style("Success!", fg=typer.colors.GREEN, bold=True)
    failed = typer.style("Failed!", fg=typer.colors.RED, bold=True)
    confirm = typer.style(
        "Are you sure you want to continue?", fg=typer.colors.BLUE, bold=True
    )


# CLI commands
cli = typer.Typer(add_completion=False, no_args_is_help=True)


@cli.command()
def develop(
    port: int = typer.Option(8000, help="Specify port to use."),
    loglevel: logenums.LogLevel = typer.Option(
        logenums.LogLevel.debug, case_sensitive=False, help="Set specific log level."
    ),
):
    """
    Start a development server with reload.
    """
    import uvicorn
    from sqlalchemy_utils import database_exists

    if not database_exists(DB_URL):
        typer.secho("No database found, has it been initialised ?", fg="red")
        raise typer.Abort

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


@cli.command()
def shell():
    """
    Starts an interactive shell with app object imported.
    """

    # Local vars defined/imported will be available in shells global scope
    import IPython
    from app.main import app

    IPython.embed()


@cli.command()
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


@cli.command()
def createdb():
    """
    Creates an empty database.
    """
    create_database_if_not_exists()
    typer.echo(Messages.success)


@cli.command()
def dropdb():
    """
    Drop the existing database.
    """
    from sqlalchemy_utils import drop_database, database_exists

    typer.confirm(Messages.confirm, abort=True)
    if not database_exists(DB_URL):
        typer.secho("Database does not exist.", fg="red")
        raise typer.Abort
    drop_database(DB_URL)
    typer.echo(Messages.success)


@cli.command(no_args_is_help=True)
def createuser(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    status: userenums.UserStatus = typer.Argument(userenums.UserStatus.active),
    role: str = typer.Argument(None),
):
    """
    Create new user in the database.

        EMAIL: Properly formatted email address.

        PASSWORD: Users password.

        FIRST_NAME: Users first name.

        LAST_NAME: Users last name.

        STATUS: Set user account status.

        Optionally assign ROLE to user.

    """

    with catch_validation_err():
        user_in = usermodels.UserCreate(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            status=status,
        )

    with existing_database() as db_session:
        if role:
            role_obj = roleservice.get_by_name(db_session=db_session, name=role)
            if not role_obj:
                typer.secho(
                    f"Role '{role}' does not exist!", fg=typer.colors.RED, bold=True
                )
                raise typer.Abort
            userservice.create_with_role(
                db_session=db_session, user_in=user_in, role=role_obj
            )
        else:
            userservice.create(db_session=db_session, user_in=user_in)
    typer.secho(Messages.success)


@cli.command(no_args_is_help=True)
def createrole(
    name: str = typer.Argument(...), description: str = typer.Argument(None),
):
    """
    Add role to database.
    """

    with catch_validation_err():
        role_in = rolemodels.RoleCreate(name=name, description=description)

    with existing_database() as db_session:
        roleservice.create(db_session=db_session, role_in=role_in)
    typer.echo(Messages.success)


@cli.command()
def seeddb():
    """
    Add fake data to database.
    """
    import random
    import faker

    fake = faker.Faker()

    # TODO: Add progress var from typer
    with existing_database() as db_session:
        with click_spinner.spinner():
            # Create roles:
            admin_role = roleservice.create(
                db_session=db_session,
                role_in=rolemodels.RoleCreate(
                    name="admin", description="Administrator privileges."
                ),
            )

            user_role = roleservice.create(
                db_session=db_session,
                role_in=rolemodels.RoleCreate(
                    name="user", description="Normal user privileges."
                ),
            )

            # Create 100 users with user role:
            for _ in range(100):
                userservice.create_with_role(
                    db_session=db_session,
                    user_in=usermodels.UserCreate(
                        email=fake.email(),
                        password="password",
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        status=random.choice(list(userenums.UserStatus)),
                    ),
                    role=user_role,
                )

            # Create users with admin role

            userservice.create_with_role(
                db_session=db_session,
                user_in=usermodels.UserCreate(
                    email="mo175@live.com",
                    password="password",
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    status=userenums.UserStatus.active,
                ),
                role=admin_role,
            )

    typer.echo(Messages.success)


if __name__ == "__main__":
    cli()
