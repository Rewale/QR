# TODO: Убрать в DI контейнер conditon, state
import threading

import loguru

from webapp.models import QuoteHistory

condition = threading.Condition()


class State:
    def __init__(self):
        self.quotes: list[QuoteHistory] = []

    def update(self, new_quotes: list[QuoteHistory]):
        self.quotes = new_quotes
        loguru.logger.info(f"update {new_quotes=}")
        with condition:
            condition.notify()
            loguru.logger.info(f"notify")


state = State()
