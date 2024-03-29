from docker.client import DockerClient
from docker.models.containers import Container

import starlette.status as status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

import server.core.types as types
from server.models import ContainerOptions
from server.core.utils import container_as_dict

client = DockerClient().from_env()


async def get_containers(_) -> JSONResponse:
    """Get the list of all containers."""
    containers: types.Containers = client.containers.list(all=True)
    return JSONResponse(container_as_dict(containers))


async def get_container(request: Request) -> JSONResponse:
    """Get container(single) by its ID."""
    container: Container = client.containers.get(request.path_params["container_id"])
    return JSONResponse(container_as_dict(container))


async def run_container(request: Request) -> JSONResponse:
    """Create and run container by options in detached mode."""
    request_body = await request.json()
    container_options = ContainerOptions.parse_obj(request_body)

    container = client.containers.run(**container_options.dict(), detach=True)

    return JSONResponse(
        container_as_dict(container), status_code=status.HTTP_201_CREATED
    )


async def unpause_container(request: Request) -> JSONResponse:
    container: Container = client.containers.get(request.path_params["container_id"])
    container.start()

    return JSONResponse({"started": True})


async def stop_container(request: Request) -> JSONResponse:
    """Stop running container."""
    container: Container = client.containers.get(request.path_params["container_id"])
    container.stop()

    return JSONResponse(
        {
            "stopped": True,
        }
    )


async def remove_container(request: Request) -> Response:
    """Remove container by its ID."""
    force_remove: bool = bool(request.query_params.get("force", False))

    container: Container = client.containers.get(request.path_params["container_id"])
    container.remove(force=force_remove)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_logs(request: Request) -> JSONResponse:
    """Get logs from the inside of the container"""
    container: Container = client.containers.get(request.path_params["container_id"])

    return JSONResponse(
        {"logs": container.logs().decode("utf-8"), "container": container.name}
    )
