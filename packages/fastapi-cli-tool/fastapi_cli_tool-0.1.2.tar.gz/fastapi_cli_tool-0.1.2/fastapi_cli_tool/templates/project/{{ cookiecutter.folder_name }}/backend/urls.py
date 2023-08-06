from core.urls import welcome
from fastapi import FastAPI


def include_router(app: FastAPI):
    app.include_router(welcome)
