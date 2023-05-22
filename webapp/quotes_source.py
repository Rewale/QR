import asyncio
import datetime
import json
import logging
import threading
from unittest.mock import Mock

import loguru
import pydantic
import websocket

from webapp.models import QuoteHistory
from webapp.services import QuoteService
from webapp.sse import State


class QuoteHistoryEvent(pydantic.BaseModel):
    quote_time: datetime.datetime
    bid: float
    ask: float
    symbol_name: str
    source_name: str


class BinanceQuoteReceive(threading.Thread):
    wss_pattern = 'wss://stream.binance.com:9443/ws/%s@ticker'

    def __init__(self, symbol_name: str, state: State, service: QuoteService):
        loguru.logger.info("start quote")
        super().__init__()
        symbol_name = symbol_name.lower()
        loguru.logger.info("start quote")
        self.source_name = 'Binance'
        self.symbol_name = symbol_name
        wss = self.wss_pattern % symbol_name
        self.state = state
        self.wsa = websocket.WebSocketApp(wss, on_message=self.on_message)
        self.service = service
        self.service.add_symbol(self.source_name,
                                self.symbol_name,
                                self.wss_pattern)

        self.start()

    def on_message(self, _wsa, data: str):
        data = json.loads(data)

        try:
            quote_time = datetime.datetime.fromtimestamp(int(data['E'] / 1000))
            bid = data['b']
            ask = data['a']
            symbol_name = self.symbol_name
            source_name = self.source_name
            self.service.add_history(
                source_name=self.source_name,
                symbol_name=self.symbol_name,
                time_quote=quote_time,
                bid=bid,
                ask=ask)
            quote_history = QuoteHistoryEvent(bid=bid, ask=ask, symbol_name=symbol_name, source_name=source_name,
                                              quote_time=quote_time)
            asyncio.run(self.state.update([quote_history]))
        except Exception as e:
            loguru.logger.exception(e)
            raise e

    def run(self) -> None:
        loguru.logger.info('RUN')
        self.wsa.run_forever()


if __name__ == '__main__':
    BinanceQuoteReceive(symbol_name='BTCUSDT', state=Mock(), service=Mock())
