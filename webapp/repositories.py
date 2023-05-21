"""Repositories module."""
import datetime
from contextlib import AbstractContextManager
from typing import Callable

import sqlalchemy
from sqlalchemy.orm import Session

from .models import Source, Symbol, QuoteHistory


class QuotesRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_symbol_history(self, symbol_name: str) -> list[QuoteHistory]:
        with self.session_factory() as session:
            quote_history = session.query(QuoteHistory).filter(QuoteHistory.symbol_name == symbol_name).all()
            if not quote_history:
                raise SymbolNotFound(symbol_name)
            return quote_history

    def add_symbol(self, name: str, source_name: str, source_url: str) -> Symbol:
        with self.session_factory() as session:
            source = session.query(Source).filter(Source.name == source_name).first()
            if not source:
                source = Source(name=source_name, url=source_url)
                session.add(source)

            user = Symbol(name=name, source=source)
            session.add(user)

            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError as ex:
                return user

            session.refresh(user)
            return user

    def add_symbol_history(self, name: str, source_name: str,
                           bid: float, ask: float, time_quote: datetime.datetime = None) -> QuoteHistory:
        time_quote = datetime.datetime.now() if not time_quote else time_quote
        with self.session_factory() as session:
            symbol = session.query(Symbol).filter(Symbol.name == name and Symbol.Source.name == source_name).first()
            if not symbol:
                raise SymbolNotFound(name)
            history = QuoteHistory(bid=bid, ask=ask, quote_time=time_quote)
            symbol.history_symbol.append(history)
            session.add(symbol)
            session.commit()
            return history

    def delete_by_name(self, symbol_name: str) -> None:
        with self.session_factory() as session:
            entity: Symbol = session.query(Symbol).filter(Symbol.name == symbol_name).first()
            if not entity:
                raise SymbolNotFound(symbol_name)
            session.delete(entity)
            session.commit()


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class SymbolNotFound(NotFoundError):
    entity_name: str = "Symbol"
