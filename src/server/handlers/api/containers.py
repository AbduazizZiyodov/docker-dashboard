import typing as t

import docker
from docker.models.containers import Container

import starlette.status as status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from server.schemas import ContainerOptions
from server.utils.api import container_as_dict

client = docker.from_env()


async def get_containers(_) -> JSONResponse:
    """Get the list of all containers (despite of their status)
    * `docker ps -a`
    """
    containers: t.List[Container] = client.containers.list(all=True)
    response = container_as_dict(containers)

    return JSONResponse(response)


async def get_container(request: Request) -> JSONResponse:
    """Get container(single) by its ID (short ID ... doesn't matter)
    * `docker ps -a ... [FILTER OPTIONS]`
    """
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    response: Container = container_as_dict(container)

    return JSONResponse(response)


async def run_container(request: Request) -> JSONResponse:
    """Run new container by options in detached mode. Options defined
    by ContainerOptions pydantic model.
    * `docker run -d` (-d for detached mode)
    """
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
    """Start container, if it exists and status == stopped.
    * `docker start`
    """
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    container.start()

    return JSONResponse({"started": True})


async def stop_container(request: Request) -> JSONResponse:
    """Stop running container.
    * `docker stop`
    """
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    container.stop()

    return JSONResponse({"stopped": True, })


async def remove_container(request: Request) -> JSONResponse:
    """Remove container by its ID.
    * `docker rm` (force mode)
    """
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )
    container.remove(force=True)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_logs(request: Request) -> JSONResponse:
    """Get logs from the inside of the container
    * `docker logs`
    """
    container: Container = client.containers.get(
        request.path_params["container_id"]
    )

    logs = container.logs().decode("utf-8")

    return JSONResponse({"logs": logs})
