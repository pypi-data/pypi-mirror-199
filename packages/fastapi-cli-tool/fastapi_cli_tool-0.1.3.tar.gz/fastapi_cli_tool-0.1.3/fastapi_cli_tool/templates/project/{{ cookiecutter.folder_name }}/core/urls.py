from backend.settings import settings
from fastapi import APIRouter

welcome = APIRouter()


@welcome.get("/")
async def welcome_route():
    return {"detail": f"Welcome to the API from {settings.PROJECT_NAME}"}
