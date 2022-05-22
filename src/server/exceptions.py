import typing as t

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException

from docker.errors import DockerException


async def http_exception_handler(
    request: Request,
    exc: t.Union[HTTPException, DockerException]
) -> JSONResponse:
    detail = exc.detail if isinstance(exc, HTTPException) else exc.explanation

    return JSONResponse(
        {"detail": detail},
        status_code=exc.status_code,
        headers=exc.headers if isinstance(exc, HTTPException) else {}
    )
