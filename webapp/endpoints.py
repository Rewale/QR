"""Endpoints module."""
import json

import pydantic
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from starlette.responses import Response, StreamingResponse

from .containers import Container
from .models import QuoteHistory
from .repositories import NotFoundError
from .services import QuoteService
from .sse import condition, state

router = APIRouter()


class Source(pydantic.BaseModel):
    name: str
    url: str


class SymbolCreate(pydantic.BaseModel):
    name: str
    source: Source


@router.get("/quotes/{symbol_name}")
@inject
def get_quotes_history(symbol_name: str,
                       quote_service: QuoteService = Depends(Provide[Container.quote_service])) -> list[
                                                                                                       QuoteHistory] | Response:
    try:
        return quote_service.get_history(symbol_name)
    except NotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/source", status_code=status.HTTP_201_CREATED)
@inject
def add(
        symbol: SymbolCreate,
        quote_service: QuoteService = Depends(Provide[Container.quote_service]),
):
    return quote_service.add_symbol(source_name=symbol.source.name,
                                    symbol_name=symbol.name,
                                    url=symbol.source.url)


@router.delete("/quotes/{symbol_name}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
        symbol_name: str,
        user_service: QuoteService = Depends(Provide[Container.quote_service]),
):
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/status")
def get_status():
    return {"status": "OK"}


@router.get('/stream')
def stream():
    def event_stream():
        while True:
            with condition:
                condition.wait()

            for message in state.quotes:
                yield json.dumps(message)

    return StreamingResponse(event_stream(), media_type="text/event-stream")
