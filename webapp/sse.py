# TODO: Убрать в DI контейнер conditon, state
import threading

import loguru

from webapp.models import QuoteHistory


class State:
    def __init__(self, condition: threading.Condition):
        self.condition = condition
        self.quotes: list[QuoteHistory] = []

    def update(self, new_quotes: list[QuoteHistory]):
        self.quotes = new_quotes
        loguru.logger.info(f"update {new_quotes=}")
        with self.condition:
            self.condition.notify()
            loguru.logger.info(f"notify")
