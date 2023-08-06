from backend.middleware import include_middleware
from backend.register_db import init_db
from backend.settings import settings
from backend.urls import include_router
from fastapi import FastAPI


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
    )
    init_db(app=app)
    include_router(app=app)
    include_middleware(app=app)

    return app


app = start_application()
