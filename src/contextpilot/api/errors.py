import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def _error_payload(message: str, error_type: str, code: str | None = None) -> dict:
    return {"error": {"message": message, "type": error_type, "code": code}}


def _http_exception_type(status_code: int) -> str:
    if status_code == 401:
        return "unauthorized_error"
    if 400 <= status_code < 500:
        return "invalid_request_error"
    return "api_error"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(
                str(exc.detail),
                _http_exception_type(exc.status_code),
                str(exc.status_code),
            ),
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_payload(str(exc), "invalid_request_error", "validation_error"),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception in API request: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_error_payload(
                "Internal server error", "internal_server_error", "internal_error"
            ),
        )
