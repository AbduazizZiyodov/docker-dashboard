import docker
import typing as t

from starlette.requests import Request
from starlette.responses import JSONResponse
from docker.models.containers import Container

from .utils import container_as_dict

client = docker.DockerClient()


async def get_containers(request: Request) -> JSONResponse:
    containers: t.List[Container] = client.containers.list()
    response = container_as_dict(containers)

    return JSONResponse(response)


async def get_container(request: Request) -> JSONResponse:
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    response: Container = container_as_dict(container)

    return JSONResponse(response)



__all__ = ["get_containers", "get_container"]
