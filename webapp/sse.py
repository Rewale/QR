# TODO: Убрать в DI контейнер conditon, state
import threading

from webapp.models import QuoteHistory

condition = threading.Condition()


class State:
    def __init__(self):
        self.quotes: list[QuoteHistory] = []

    def update(self, new_quotes: list[QuoteHistory]):
        self.quotes = new_quotes
        with condition:
            condition.notify()


state = State()

