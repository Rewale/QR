"""Application module."""

from fastapi import FastAPI

from .containers import Container
from . import endpoints
from .quotes_source import BinanceQuoteReceive
from .sse import state


def create_app() -> FastAPI:
    container = Container()
    container.config.is_test.from_env('IS_TEST')
    db = container.db()
    db.create_database()

    binance_quote_receive = BinanceQuoteReceive(
        symbol_name='BTCUSDT',
        state=state,
        service=container.quote_service()
    )

    application = FastAPI()
    application.container = container
    application.include_router(endpoints.router)
    return application


app = create_app()
