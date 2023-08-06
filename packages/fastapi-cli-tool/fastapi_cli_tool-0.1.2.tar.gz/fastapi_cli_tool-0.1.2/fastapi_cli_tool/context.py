import subprocess
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, root_validator

from fastapi_cli_tool.constants import (
    Database,
    DatabaseORM,
    License,
    PackageManager,
    PythonVersion,
)
from fastapi_cli_tool.helpers import get_package_version


class AppContext(BaseModel):
    name: str
    folder_name: str
    snake_name: str

    @root_validator(pre=True)
    def validate_app(cls, values: dict):
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        values["snake_name"] = values["folder_name"].replace("-", "_")
        return values


class ProjectContext(BaseModel):
    name: str
    folder_name: str
    packaging: PackageManager
    version: str

    username: Optional[str] = None
    email: Optional[EmailStr] = None

    python: PythonVersion

    license: Optional[License]
    year: int

    pre_commit: bool = False
    docker: bool = False

    database: Optional[Database] = None
    database_orm: DatabaseORM

    fastapi: str
    pytest: str
    tzdata: str
    pytz: str
    fastapi_mail: str
    passlib: str
    asgiref: str
    uvicorn: str
    python_jose: str
    fastapi_cli_tool: str
    pytest_cov: str
    httpx: str

    orm_version: str = "*"

    use_code_formatter: bool = False

    black: str
    isort: str

    @root_validator()
    def validate_orm(cls, values: dict):
        orms = {"TortoiseORM": "tortoise-orm", "SQLAlchemy": "SQLAlchemy"}
        values["orm_version"] = get_package_version(orms[values["database_orm"]])
        return values

    @root_validator(pre=True)
    def validate_project(cls, values: dict):
        try:
            values["username"] = subprocess.check_output(
                ["git", "config", "--get", "user.name"]
            )
            values["email"] = subprocess.check_output(
                ["git", "config", "--get", "user.email"]
            )
        except subprocess.CalledProcessError:
            ...
        values["folder_name"] = values["name"].lower().replace(" ", "-").strip()
        values["year"] = datetime.today().year
        return values

    class Config:
        use_enum_values = True
