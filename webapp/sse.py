import asyncio

import pydantic


class State:
    def __init__(self, condition: asyncio.Condition):
        self.condition = condition
        self.quotes: list[pydantic.BaseModel] = []

    async def update(self, new_quotes: list[pydantic.BaseModel]):
        self.quotes = new_quotes
        async with self.condition:
            self.condition.notify()
