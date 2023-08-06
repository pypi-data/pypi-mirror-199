from backend.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def include_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
