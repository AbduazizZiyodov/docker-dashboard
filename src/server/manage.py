import typer
import uvicorn
import typing as t

from fastapi import FastAPI, APIRouter

from settings import Settings as settings
from images.views import images_router
from containers.views import containers_router


def create_app(routers: t.List[APIRouter]) -> FastAPI:
    api = FastAPI(**settings.FASTAPI_SETTINGS)

    for router in routers:
        api.include_router(router)

    return api


cli = typer.Typer()


api = create_app([containers_router, images_router])


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
