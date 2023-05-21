import threading

import pydantic


class State:
    def __init__(self, condition: threading.Condition):
        self.condition = condition
        self.quotes: list[pydantic.BaseModel] = []

    def update(self, new_quotes: list[pydantic.BaseModel]):
        self.quotes = new_quotes
        with self.condition:
            self.condition.notify()
