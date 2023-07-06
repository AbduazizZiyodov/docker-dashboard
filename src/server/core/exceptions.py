import json

import typing as t
from pydantic import ValidationError
from docker.errors import DockerException

import starlette.status as error
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

from server.core.types import HttpDockerException, SupportsRead


def http_exception_handler(_, exc: HttpDockerException) -> JSONResponse:
    """Starlette HTTP exception handler"""
    detail = exc.detail if isinstance(exc, HTTPException) else exc.explanation

    return JSONResponse(
        {"detail": detail},
        status_code=exc.status_code,
        headers=exc.headers if isinstance(exc, HTTPException) else {},
    )


def pydantic_exception_handler(_, exc: ValidationError) -> JSONResponse:
    """Handling pydantic validation exceptions"""
    return JSONResponse(
        content=exc.errors(), status_code=error.HTTP_422_UNPROCESSABLE_ENTITY
    )


def json_exception_handler(_, exc: json.decoder.JSONDecodeError) -> JSONResponse:
    return JSONResponse(
        status_code=error.HTTP_400_BAD_REQUEST, content={"error": "JSON decode error"}
    )


def websocket_request_handler(data: dict, Model: t.Any) -> t.Any:
    try:
        return Model.parse_obj(data), None
    except ValidationError as exc:
        return None, json.loads(exc.json())


exception_handlers: dict[t.Any, t.Callable[..., t.Any]] = {
    HTTPException: http_exception_handler,
    DockerException: http_exception_handler,
    ValidationError: pydantic_exception_handler,
    json.decoder.JSONDecodeError: json_exception_handler,
}
