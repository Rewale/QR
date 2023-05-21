"""Services module."""
import logging

from .models import *
from .repositories import QuotesRepository

logger = logging.getLogger(__name__)


class QuoteService:
    def __init__(self, user_repository: QuotesRepository) -> None:
        logger.info(f"{user_repository=}")
        self._repository: QuotesRepository = user_repository

    def get_history(self, symbol_name: str) -> list[QuoteHistory]:
        return self._repository.get_symbol_history(symbol_name)

    def add_history(self, source_name: str, symbol_name: str,
                    bid: float, ask: float, time_quote: datetime.datetime = None) -> QuoteHistory:
        return self._repository.add_symbol_history(source_name=source_name,
                                                   bid=bid, ask=ask,
                                                   name=symbol_name,
                                                   time_quote=time_quote)

    def add_symbol(self, source_name: str, symbol_name: str, url: str) -> Symbol:
        return self._repository.add_symbol(name=symbol_name, source_name=source_name, source_url=url)
