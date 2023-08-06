from backend.settings import settings
from fastapi import APIRouter
from {{cookiecutter.snake_name}}.api import (routes_delete, routes_get,
                                         routes_patch, routes_post, routes_put)

{{ cookiecutter.snake_name }}_router = APIRouter()

{{ cookiecutter.snake_name }}_router.include_router(
    routes_get.router,
    prefix=f"{settings.API_V1_STR}/{{ cookiecutter.snake_name }}",
    tags=["{{ cookiecutter.snake_name }}", "Gets"],
)
{{ cookiecutter.snake_name }}_router.include_router(
    routes_post.router,
    prefix=f"{settings.API_V1_STR}/{{ cookiecutter.snake_name }}",
    tags=["{{ cookiecutter.snake_name }}", "Posts"],
)
{{ cookiecutter.snake_name }}_router.include_router(
    routes_patch.router,
    prefix=f"{settings.API_V1_STR}/{{ cookiecutter.snake_name }}",
    tags=["kanban", "Patches"],
)
{{ cookiecutter.snake_name }}_router.include_router(
    routes_put.router,
    prefix=f"{settings.API_V1_STR}/{{ cookiecutter.snake_name }}",
    tags=["{{ cookiecutter.snake_name }}", "Puts"],
)
{{ cookiecutter.snake_name }}_router.include_router(
    routes_delete.router,
    prefix=f"{settings.API_V1_STR}/{{ cookiecutter.snake_name }}",
    tags=["{{ cookiecutter.snake_name }}", "Deletes"],
)




