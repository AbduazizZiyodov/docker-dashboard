import json

from typing import Any
from pydantic import BaseModel
from pydantic import ValidationError
from docker.errors import DockerException

import starlette.status as error
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

from server.types import HttpDockerException


async def http_exception_handler(_, exc: HttpDockerException) -> JSONResponse:
    """Starlette HTTP exception handler"""
    detail = exc.detail if isinstance(exc, HTTPException) else exc.explanation

    return JSONResponse(
        {"detail": detail},
        status_code=exc.status_code,
        headers=exc.headers if isinstance(exc, HTTPException) else {},
    )


async def pydantic_exception_handler(_, exc: ValidationError) -> JSONResponse:
    """Handling pydantic validation exceptions"""
    detail: dict = json.loads(exc.json())
    return JSONResponse(detail, status_code=error.HTTP_422_UNPROCESSABLE_ENTITY)


def websocket_request_handler(data: Any, Model: BaseModel) -> Any:
    try:
        return Model(**data), None
    except ValidationError as exc:
        return None, json.loads(exc.json())


exception_handlers = {
    HTTPException: http_exception_handler,
    DockerException: http_exception_handler,
    ValidationError: pydantic_exception_handler,
}
