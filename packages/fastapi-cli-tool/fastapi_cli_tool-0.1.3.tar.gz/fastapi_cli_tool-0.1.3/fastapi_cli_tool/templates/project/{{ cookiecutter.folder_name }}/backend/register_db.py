{% if cookiecutter.database_orm == "TortoiseORM" %}from backend.settings import settings
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": settings.APP_MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )


Tortoise.init_models(settings.APP_MODELS, "models") {% endif %}
{% if cookiecutter.database_orm == "SQLAlchemy" %}from typing import Generator, Any
from backend.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


def init_db(app):
    Base.metadata.create_all(bind=engine) {% endif %}
