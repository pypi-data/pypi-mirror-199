import os
from typing import TypeVar

import typer
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter
from pydantic.main import BaseModel

from fastapi_cli_tool.config import TEMPLATES_DIR
from fastapi_cli_tool.context import AppContext, ProjectContext

ContextType = TypeVar("ContextType", bound=BaseModel)


def fill_template(template_name: str, context: ContextType):
    try:
        cookiecutter(
            os.path.join(TEMPLATES_DIR, template_name),
            extra_context=context.dict(),
            no_input=True,
        )
    except OutputDirExistsException:
        typer.echo(f"{template_name} '{context.folder_name}' already exists. ❌")
    else:
        typer.echo()
        typer.echo(f"FastAPI {template_name} created successfully! 🎉")
        if template_name == "project":
            typer.echo()
            typer.echo(
                typer.style(f"   cd {context.folder_name}", fg=typer.colors.GREEN)
            )
            if context.packaging == "poetry":
                typer.echo(typer.style(f"   poetry install", fg=typer.colors.GREEN))
            if context.packaging == "pip":
                typer.echo(
                    typer.style(
                        f"   pip install -r requirements.txt", fg=typer.colors.GREEN
                    )
                )
            typer.echo()


def generate_app(context: AppContext):
    fill_template("app", context)


def generate_project(context: ProjectContext):
    fill_template("project", context)
