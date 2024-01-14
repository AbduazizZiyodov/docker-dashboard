import typing as t

from docker.client import DockerClient
from docker.models.containers import Container

from fastapi import APIRouter
import starlette.status as status
from fastapi.responses import JSONResponse, Response

import server.types as types
from server.models.container import ContainerOptions
from server.utils.helpers import container_as_dict


client = DockerClient().from_env()
router = APIRouter(prefix="/api/containers", tags=["Containers"])


@router.get("")
async def get_containers():
    """Get the list of all containers."""
    containers: types.Containers = client.containers.list(all=True)
    return container_as_dict(containers)


@router.get("/{container_id}")
async def get_container(container_id: str):
    """Get container(single) by its ID."""
    container: Container = client.containers.get(container_id)
    return container_as_dict(container)


@router.post("/run")
async def run_container(container_options: ContainerOptions):
    """Create and run container by options in detached mode."""

    container = client.containers.run(**container_options.dict(), detach=True)

    return JSONResponse(
        content=container_as_dict(container), status_code=status.HTTP_201_CREATED
    )


@router.get("/{container_id}/unpause")
async def unpause_container(container_id: str):
    container: Container = client.containers.get(container_id)
    container.start()

    return {"started": True}


@router.get("/{container_id}/stop")
async def stop_container(container_id: str):
    """Stop running container."""
    container: Container = client.containers.get(container_id)
    container.stop()

    return {"stopped": True}


@router.delete("/{container_id}/remove")
async def remove_container(container_id: str, force_remove: t.Optional[bool] = False):
    """Remove container by its ID."""
    container: Container = client.containers.get(container_id)
    container.remove(force=force_remove)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{container_id}/logs")
async def get_logs(container_id: str):
    """Get logs from the inside of the container"""
    container: Container = client.containers.get(container_id)

    return {"logs": container.logs().decode("utf-8"), "container": container.name}
