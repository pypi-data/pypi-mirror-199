from __future__ import annotations

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from artemis_common import exceptions as artemis_exceptions
from artemis_common.models.server import ServerExceptionResponseModel


def add_base_exception_handlers(app: FastAPI):
    @app.exception_handler(artemis_exceptions.ArtemisOperationFailedError)
    async def handle_artemis_operation_failed_error(
        request: Request,
        exc: artemis_exceptions.ArtemisOperationFailedError,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServerExceptionResponseModel(
                message='Artemis server operation failed!',
                error=str(exc),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                url=str(request.url),
                path=request.url.path,
                params=request.query_params,
                exc=exc,
            ).dict(),
        )

    @app.exception_handler(artemis_exceptions.ArtemisOperationUnexpectedlyFailedError)
    async def handle_artemis_operation_unexpectedly_failed_error(
        request: Request,
        exc: artemis_exceptions.ArtemisOperationUnexpectedlyFailedError,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServerExceptionResponseModel(
                message='[Unexpected] Artemis server operation failed unexpectedly!',
                error=str(exc),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                url=str(request.url),
                path=request.url.path,
                params=request.query_params,
                exc=exc,
            ).dict(),
        )

    @app.exception_handler(artemis_exceptions.ArtemisUnexpectedFlowError)
    async def handle_artemis_unexpected_flow_reached_error(
        request: Request,
        exc: artemis_exceptions.ArtemisUnexpectedFlowError,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServerExceptionResponseModel(
                message='[Unexpected] This exception should never be raised!',
                error=str(exc),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                url=str(request.url),
                path=request.url.path,
                params=request.query_params,
                exc=exc,
            ).dict(),
        )

    @app.exception_handler(artemis_exceptions.ArtemisException)
    async def handle_unclassified_artemis_exception(
        request: Request,
        exc: artemis_exceptions.ArtemisException,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServerExceptionResponseModel(
                message='[Unexpected] Artemis Unclassified Error',
                error=str(exc),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                url=str(request.url),
                path=request.url.path,
                params=request.query_params,
                exc=exc,
            ).dict(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ServerExceptionResponseModel(
                message='Validation Error',
                error=str(exc),
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                url=str(request.url),
                path=request.url.path,
                params=request.query_params,
                exc=exc,
            ).dict(),
        )

    @app.exception_handler(Exception)
    async def handle_unknown_exception(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServerExceptionResponseModel(
                message='[Unexpected] Server Error',
                error=str(exc),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                url=str(request.url),
                path=request.url.path,
                params=request.query_params,
                exc=exc,
            ).dict(),
        )
