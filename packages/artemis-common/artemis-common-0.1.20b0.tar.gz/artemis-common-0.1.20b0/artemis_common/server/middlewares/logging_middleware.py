from __future__ import annotations

import logging
from time import perf_counter
from typing import Callable
from uuid import uuid4

from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware

from artemis_common.models.server import LogRequestModel
from artemis_common.models.server import LogResponseModel


class AsyncIteratorWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        logger: logging.Logger,
    ) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        request_id = str(uuid4())

        await self._log_request(request, request_id)

        start_time = perf_counter()
        response = await self._execute_request(request, call_next, request_id)
        end_time = perf_counter()

        process_time = round(end_time - start_time, 4)
        await self._log_response(response, request, request_id, process_time)

        return response

    async def _execute_request(
        self,
        request: Request,
        call_next: Callable,
        request_id: str,
    ) -> Response:
        try:
            response = await call_next(request)
            response.headers['X-API-Request-ID'] = request_id
            return response

        except Exception as ex:
            request_model = LogRequestModel(request=request)
            message = 'Failed to process response'
            self._logger.exception(
                message, extra=dict(
                    request_id=request_id,
                    request=request_model.dict(),
                    client_address=self._get_client_address(request),
                    exc_message=str(ex),
                ),
            )
            raise

    async def _log_request(
        self,
        request: Request,
        request_id: str,
    ):
        request_model = LogRequestModel(request=request)
        message = f'Request {request.method} {request.url}'
        self._logger.info(
            message, extra=dict(
                request_id=request_id,
                request=request_model.dict(),
                client_address=self._get_client_address(request),
            ),
        )

    async def _log_response(
        self,
        response: Response,
        request: Request,
        request_id: str,
        process_time: float,
    ):
        response_body = [section async for section in response.__dict__['body_iterator']]
        response.__setattr__(
            'body_iterator', AsyncIteratorWrapper(response_body),
        )

        response_length = 0
        for response_item in response_body:
            response_length += len(response_item)

        response_model = LogResponseModel(
            request=request,
            response=response,
            response_length=response_length,
        )
        message = f'Response {request.method} {request.url}'

        self._logger.info(
            message, extra=dict(
                request_id=request_id,
                client_address=self._get_client_address(request),
                response_time=process_time,
                response=response_model.dict(),
            ),
        )

    def _get_client_address(self, request: Request):
        client_address = request.headers.get('x-azure-clientip')
        if client_address:
            return client_address
        return request.headers.get('x-client-ip', request.client.host)
