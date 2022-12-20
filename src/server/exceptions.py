import json
import typing as t
from pydantic import ValidationError
from docker.errors import DockerException

from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException



async def http_exception_handler(
    _,
    exc: t.Union[HTTPException, DockerException]
) -> JSONResponse:
    detail = exc.detail if isinstance(exc, HTTPException) else exc.explanation

    return JSONResponse(
        {"detail": detail},
        status_code=exc.status_code,
        headers=exc.headers if isinstance(exc, HTTPException) else {}
    )


async def pydantic_exception_handler(
    _,
    exc: ValidationError
) -> JSONResponse:
    detail: dict = json.loads(exc.json())

    return JSONResponse(
        detail,
        status_code=422
    )


__all__ = ["pydantic_exception_handler", "http_exception_handler"]
