import typing as t

from docker.client import DockerClient
from docker.models.containers import Container

from fastapi import APIRouter
import starlette.status as status
from fastapi.responses import JSONResponse, Response

from server.utils.helpers import container_as_dict
from server.models.container import (
    ContainerResponse,
    ContainerRunOptions,
    ContainerLogsResponse,
    ContainerActionStatusResponse,
)


client = DockerClient().from_env()
router = APIRouter(prefix="/api/containers", tags=["Containers"])


@router.get("", response_model=t.List[ContainerResponse])
async def get_containers() -> JSONResponse:
    """List containers. Similar to the ``docker ps`` command."""
    containers: t.List[Container] = client.containers.list(all=True)
    return JSONResponse(container_as_dict(containers))


@router.get("/{container_id}", response_model=ContainerResponse)
async def get_container(container_id: str) -> JSONResponse:
    """Get container(single) by its ID."""
    container: Container = client.containers.get(container_id)
    return JSONResponse(container_as_dict(container))


@router.post("/run", response_model=ContainerResponse)
async def run_container(container_options: ContainerRunOptions) -> JSONResponse:
    """Run a container(detached mode), similar to ``docker run``."""

    container: Container = client.containers.run(
        **container_options.model_dump(), detach=True
    )

    return JSONResponse(
        content=container_as_dict(container), status_code=status.HTTP_201_CREATED
    )


@router.get("/{container_id}/unpause", response_model=ContainerActionStatusResponse)
async def unpause_container(container_id: str) -> ContainerActionStatusResponse:
    """Start this container. Similar to the ``docker start`` command, but
    doesn't support attach options.
    """
    query = client.containers.get
    container: Container = query(container_id)
    container.start()

    return ContainerActionStatusResponse(
        container_id=container_id, status=query(container_id).status
    )


@router.get("/{container_id}/stop", response_model=ContainerActionStatusResponse)
async def stop_container(container_id: str) -> ContainerActionStatusResponse:
    """Stops a container. Similar to the ``docker stop`` command."""
    query = client.containers.get
    container: Container = query(container_id)
    container.stop()

    return ContainerActionStatusResponse(
        container_id=container_id, status=query(container_id).status
    )


@router.delete("/{container_id}/remove")
async def remove_container(
    container_id: str,
    force_remove: t.Optional[bool] = False,
    remove_volumes: t.Optional[bool] = False,
) -> Response:
    """Remove this container. Similar to the ``docker rm`` command."""
    container: Container = client.containers.get(container_id)
    container.remove(v=remove_volumes, force=force_remove)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{container_id}/logs", response_model=ContainerLogsResponse)
async def get_logs(container_id: str) -> ContainerLogsResponse:
    """Get logs from this container. Similar to the ``docker logs`` command."""
    container: Container = client.containers.get(container_id)

    return ContainerLogsResponse(
        container_id=container_id,
        container_name=container.name,
        logs=container.logs().decode("utf-8"),
    )
