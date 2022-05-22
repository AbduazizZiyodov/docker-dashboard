import typer
import uvicorn
import typing as t

from starlette.routing import Route
from starlette.applications import Starlette
from starlette.exceptions import HTTPException

from docker.errors import DockerException

from containers.views import *
from exceptions import http_exception_handler

cli = typer.Typer()


def create_app() -> Starlette:
    routes = [
        Route("/api/containers", get_containers, methods=["GET"]),
        Route(
            "/api/containers/{container_id:str}",
            get_container, methods=["GET"]
        ),
    ]

    return Starlette(
        routes=routes,
        exception_handlers={
            HTTPException: http_exception_handler,
            DockerException: http_exception_handler
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
