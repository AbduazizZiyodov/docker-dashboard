import typer
import pytest
import uvicorn

from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from pydantic import ValidationError
from docker.errors import DockerException

from images import *
from handlers import *
from containers import *


cli = typer.Typer()


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


@cli.command()
def serve():
    uvicorn.run(
        create_app(),
        host="localhost",
        port=2121,
        debug=False
    )


@cli.command()
def run_tests():
    pytest.main(["-s", "tests/"])


if __name__ == "__main__":
    cli()
