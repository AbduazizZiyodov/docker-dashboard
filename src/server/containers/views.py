import docker
import typing as t

import starlette.status as status

from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from docker.models.containers import Container

from .utils import container_as_dict
from .schemas import ContainerOptions

client = docker.from_env()


async def get_containers(request: Request) -> JSONResponse:
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

container_routes = [
    Route("/api/containers", get_containers, methods=["GET"]),
    Route(
        "/api/containers/{container_id:str}",
        get_container, methods=["GET"]
    ),
    Route(
        "/api/containers/run",
        run_container, methods=["POST"]
    ),
    Route(
        "/api/containers/{container_id:str}/start",
        start_stopped_container, methods=["GET"]
    ),
    Route(
        "/api/containers/{container_id:str}/stop",
        stop_container, methods=["GET"]
    ),
    Route(
        "/api/containers/{container_id:str}/delete",
        delete_container, methods=["DELETE"]
    ),
    Route(
        "/api/containers/{container_id:str}/logs",
        get_logs, methods=["GET"]
    ),
]
