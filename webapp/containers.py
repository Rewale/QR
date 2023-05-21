"""Containers module."""
import threading
from unittest.mock import Mock

from dependency_injector import containers, providers

from .database import Database
from .quotes_source import BinanceQuoteReceive
from .repositories import QuotesRepository
from .services import QuoteService
from .sse import State


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])

    Real_db = providers.Singleton(Database, db_url=config.db.url)
    Test_db = providers.Singleton(Mock())
    condition = providers.Singleton(threading.Condition)
    state = providers.Singleton(State, condition=condition)

    db = providers.Selector(
        config.is_test,
        true=Test_db,
        false=Real_db
    )

    quote_repository = providers.Factory(
        QuotesRepository,
        session_factory=db.provided.session,
    )
    quote_service = providers.Factory(
        QuoteService,
        user_repository=quote_repository,
    )

    binance_quote_receiver = providers.Singleton(
        BinanceQuoteReceive,
        symbol_name='BTCUSDT',
        state=state,
        service=quote_service
    )
