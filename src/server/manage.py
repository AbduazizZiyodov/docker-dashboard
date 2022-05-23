import typer
import uvicorn
import typing as t

from starlette.applications import Starlette
from starlette.exceptions import HTTPException

from pydantic import ValidationError
from docker.errors import DockerException

from pydantic import ValidationError
from images.views import image_routes
from containers.views import container_routes

from exceptions import (
    http_exception_handler,
    pydantic_exception_handler
)

cli = typer.Typer()


def create_app() -> Starlette:
    routes = container_routes + image_routes

    return Starlette(
        routes=routes,
        exception_handlers={
            HTTPException: http_exception_handler,
            DockerException: http_exception_handler,
            ValidationError: pydantic_exception_handler
        }
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


if __name__ == "__main__":
    cli()
