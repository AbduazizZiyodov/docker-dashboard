import typing as t

import docker
from docker.models.containers import Container

import starlette.status as status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from server.utils.api import container_as_dict
from server.schemas.container import ContainerOptions

client = docker.from_env()


async def get_containers(_) -> JSONResponse:
    containers: t.List[Container] = client.containers.list(all=True)
    response = container_as_dict(containers)

    return JSONResponse(response)


async def get_container(request: Request) -> JSONResponse:
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    response: Container = container_as_dict(container)

    return JSONResponse(response)


async def run_container(request: Request) -> JSONResponse:
    request_body = await request.json()
    container_options = ContainerOptions.parse_obj(request_body)
    container = client.containers.run(
        **container_options.dict(),
        detach=True
    )

    return JSONResponse(
        container_as_dict(container),
        status_code=status.HTTP_201_CREATED
    )


async def start_stopped_container(request: Request) -> JSONResponse:
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    container.start()

    return JSONResponse({"started": True})


async def stop_container(request: Request) -> JSONResponse:
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    container.stop()

    return JSONResponse({"stopped": True, })


async def delete_container(request: Request) -> JSONResponse:
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    container.remove(force=True)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_logs(request: Request) -> JSONResponse:
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )

    logs = container.logs().decode("utf-8")

    return JSONResponse({"logs": logs})
