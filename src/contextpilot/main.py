from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contextpilot.api.auth import require_api_key
from contextpilot.api.health import router as h
from contextpilot.api.models import router as m
from contextpilot.api.openai import router as o
from contextpilot.api.anthropic import router as a
from contextpilot.storage.migrations import init_db

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(h)
app.include_router(m, dependencies=[Depends(require_api_key)])
app.include_router(o, dependencies=[Depends(require_api_key)])
app.include_router(a, dependencies=[Depends(require_api_key)])


def _error_payload(message: str, error_type: str, code: int) -> dict:
    return {"error": {"message": message, "type": error_type, "code": code}}


@app.exception_handler(RequestValidationError)
async def handle_validation_error(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=_error_payload(str(exc), "invalid_request_error", 422),
    )


@app.exception_handler(HTTPException)
async def handle_http_error(_, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "Request failed"
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(detail, "http_error", exc.status_code),
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(_, __: Exception):
    return JSONResponse(
        status_code=500,
        content=_error_payload("Internal server error", "internal_error", 500),
    )
