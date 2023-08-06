from __future__ import annotations

from fastapi import Request
from fastapi import Response
from pydantic import BaseModel


class LogRequestModel(BaseModel):
    method: str
    path: str
    query: str
    headers: dict

    def __init__(self, request: Request):
        super().__init__(
            method=request.method,
            path=request.url.path,
            query=request.url.query,
            headers=dict(request.headers),
        )


class LogResponseModel(BaseModel):
    length: int
    status_code: int

    def __init__(self, request: Request, response: Response, response_length: int):
        super().__init__(
            status_code=response.status_code,
            length=response_length,
        )


__all__ = [
    LogRequestModel.__name__,
    LogResponseModel.__name__,
]
