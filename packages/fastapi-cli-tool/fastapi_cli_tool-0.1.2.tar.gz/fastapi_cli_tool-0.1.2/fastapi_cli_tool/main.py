import os
import subprocess
import sys
import pkg_resources
import typer
from questionary.form import form

from fastapi_cli_tool.constants import (
    Database,
    DatabaseORM,
    License,
    PackageManager,
    PythonVersion,
)
from fastapi_cli_tool.context import AppContext, ProjectContext
from fastapi_cli_tool.generator import generate_app, generate_project
from fastapi_cli_tool.helpers import (
    binary_question,
    get_package_version,
    question,
    question_input,
)

app = typer.Typer(
    add_completion=False,
    help="Create FastApi Projects and Apps!",
    name="fastapi-cli-tool",
)


@app.command(help="Creates a FastAPI project.")
def startproject(name: str):
    if os.path.exists(
        os.path.join(os.getcwd(), name.lower().replace(" ", "-").strip())
    ):
        typer.echo(f"Project '{name}' already exists. ❌")
        SystemExit(1)
        sys.exit(1)
    try:
        results = form(
            packaging=question("Select a Package Manger:", PackageManager),
            python=question("Select a Python Version:", PythonVersion),
            version=question_input("Version of the Project:", default="0.0.1"),
            license=question("Select a License:", License),
            database=question("Select a Database:", Database),
            database_orm=question("Select a Database ORM:", DatabaseORM),
            use_code_formatter=binary_question("use code formatter:"),
        ).ask()

        packeage_version = {
            "fastapi": get_package_version("fastapi"),
            "pytest": get_package_version("pytest"),
            "tzdata": get_package_version("tzdata"),
            "pytz": get_package_version("pytz"),
            "fastapi_mail": get_package_version("fastapi-mail"),
            "passlib": get_package_version("passlib"),
            "asgiref": get_package_version("asgiref"),
            "uvicorn": get_package_version("uvicorn"),
            "python_jose": get_package_version("python-jose"),
            "fastapi_cli_tool": get_package_version("fastapi-cli-tool"),
            "pytest_cov": get_package_version("pytest-cov"),
            "black": get_package_version("black"),
            "isort": get_package_version("isort"),
            "httpx": get_package_version("httpx"),
        }

        results = {**results, **packeage_version}
        context = ProjectContext(name=name, **results)
        generate_project(context)
    except Exception as e:
        SystemExit(1)


@app.command(help="Creates a FastAPI component.")
def startapp(name: str):
    if os.path.exists(os.path.join(os.getcwd(), "manage.py")):
        context = AppContext(name=name)
        generate_app(context)
    else:
        typer.echo(f"No FastApi Project Found! ❌")


@app.command(help="Run a FastAPI application.")
def runserver(
    reload: bool = typer.Option(False, "--reload"),
    port: int = typer.Option(8000, "--port", case_sensitive=False),
):
    args = []
    if reload:
        args.append("--reload")
    args.append(f"--port")
    args.append(str(port))
    app_file = os.getenv("FASTAPI_APP", "core.app")
    subprocess.call(["uvicorn", f"{app_file}:app", *args])


def version_callback(value: bool):
    if value:
        version = pkg_resources.get_distribution("fastapi-cli-tool").version
        typer.echo(f"Version {version}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the FastAPI CLI Tool Version.",
    )
):
    ...


if __name__ == "__main__":
    app()
