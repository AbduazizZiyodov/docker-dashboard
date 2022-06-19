import typer
import pytest
import uvicorn
import typing as t

from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from pydantic import ValidationError
from docker.errors import DockerException

from pydantic import ValidationError
from images.views import image_routes
from containers.views import container_routes

from exceptions import (
    http_exception_handler,
    pydantic_exception_handler
)
from tests.client import CustomAsyncTestClient

cli, client = typer.Typer(), CustomAsyncTestClient()


def create_app() -> Starlette:
    routes = container_routes + image_routes + [
        Route("/", lambda _:JSONResponse("ok"), methods=["GET"])
    ]

    return Starlette(
        routes=routes,
        exception_handlers={
            HTTPException: http_exception_handler,
            DockerException: http_exception_handler,
            ValidationError: pydantic_exception_handler
        },
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=['*'],
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )


api = create_app()


@cli.command()
def serve(
    host: t.Optional[str] = "localhost",
    port: t.Optional[int] = 8000,
    reload: t.Optional[bool] = True,
    debug: t.Optional[bool] = True
):

    uvicorn.run(
        "manage:api",
        host=host,
        port=port,
        debug=debug,
        reload=reload
    )


@cli.command()
def run_tests():
    pytest.main(["-s", "tests/"])


if __name__ == "__main__":
    cli()
