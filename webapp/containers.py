"""Containers module."""
from unittest.mock import Mock

from dependency_injector import containers, providers

from .database import Database
from .repositories import UserRepository
from .services import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    Real_db = providers.Singleton(Database, db_url=config.db.url)
    Test_db = providers.Singleton(Mock())

    db = providers.Selector(
        config.is_test,
        true=Test_db,
        false=Real_db
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=db.provided.session,
    )

    quote_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
