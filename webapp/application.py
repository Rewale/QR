"""Application module."""

from fastapi import FastAPI

from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()
    container.config.is_test.from_env('IS_TEST')
    db = container.db()
    db.create_database()

    application = FastAPI()
    application.container = container
    application.include_router(endpoints.router)
    return application


app = create_app()
