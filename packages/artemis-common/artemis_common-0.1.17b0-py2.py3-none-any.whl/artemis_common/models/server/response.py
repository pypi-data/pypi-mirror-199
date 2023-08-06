from __future__ import annotations

from typing import Optional
from typing import Type

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


class ExceptionChain(BaseModel):
    type: str
    message: str


def get_exception_chain(
    exc: Type[Exception],
    exc_chain: list[ExceptionChain],
) -> list[ExceptionChain]:
    if exc.__cause__:
        cause = exc.__cause__
        exception_chain_item = ExceptionChain(
            type=type(cause).__name__,
            message=str(cause),
        )
        exc_chain.append(exception_chain_item)
        return get_exception_chain(cause, exc_chain)
    return exc_chain


class BaseServerResponseModel(BaseModel):
    status_code: int
    success: bool


class ServerSuccessResponseModel(BaseServerResponseModel):
    success: bool = Field(default=True)
    data: Optional[dict] = Field(default=None)


class ServerExceptionResponseModel(BaseServerResponseModel):
    class Config:
        arbitrary_types_allowed = True

    message: str
    error: str
    url: str
    path: str
    params: dict
    exc: Exception = Field(exclude=True)
    exc_chain: list[ExceptionChain] = Field(default=None)
    success: bool = Field(default=False)
    extra: Optional[dict] = Field(default=None)

    @root_validator(pre=True)
    def pre(cls, values: dict) -> dict:
        exc = values['exc']
        exc_chain = get_exception_chain(exc, [])
        values['exc_chain'] = exc_chain
        return values


__all__ = [
    BaseServerResponseModel.__name__,
    ServerSuccessResponseModel.__name__,
    ServerExceptionResponseModel.__name__,
]
