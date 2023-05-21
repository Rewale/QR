"""Models module."""
import datetime

from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Source(Base):
    __tablename__ = "source"

    name = Column(String, primary_key=True)
    url = Column(String)
    connect_type = Column(String(12), default="ws")


class Symbol(Base):
    __tablename__ = "symbol"

    name = Column(String, max)
    source = relationship('Source', backref='symbol_source', lazy='subquery')


class QuoteHistory(Base):
    __tablename__ = "history"

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    quote_time = Column(DateTime, default=datetime.datetime.now)
    symbol = relationship('Symbol', backref='history_symbol', lazy='subquery')
    ask = Column(Float(20))
    bid = Column(Float(20))
