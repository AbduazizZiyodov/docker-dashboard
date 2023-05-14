import docker

from docker.models.images import Image

import starlette.status as status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from server import types

from server.utils.api import (
    image_as_dict,
    container_as_dict,
    filter_containers_by_image
)

from server.models import DockerSearchRequest

client = docker.from_env()


async def get_images(_) -> JSONResponse:
    """Get list of all docker images.
    * `docker images || docker image ls`
    """
    images: types.Images = client.images.list(all=True)
    response = image_as_dict(images, client)

    return JSONResponse(response)


async def get_image(request: Request) -> JSONResponse:
    """Get a specific docker image by IMAGE_ID.
    * `docker images || docker image ls ... [FILTER OPTIONS]`
    """
    image: Image = client.images.get(
        request.path_params["image_id"]
    )
    response: Image = image_as_dict(image, client, True)

    return JSONResponse(response)


async def remove_image(request: Request) -> JSONResponse:
    """Remove a specific docker image by IMAGE_ID (force mode!!!).
    * `docker rmi -f`
    """
    image: Image = client.images.get(
        request.path_params["image_id"]
    )

    client.images.remove(image.short_id, force=True)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def search_image(request: Request) -> JSONResponse:
    """Perform search for docker image. Search options defined
    in the DockerSearchRequest pydantic model.
    * `docker search [OPTIONS]`
    """
    request_body: DockerSearchRequest = DockerSearchRequest(
        **await request.json()
    )

    results = client.images.search(**request_body.dict())

    return JSONResponse(results)


async def get_containers_by_image(request: Request) -> JSONResponse:
    """Get list of containers by IMAGE_ID.
    * `docker ps -a ... [FILTER OPTIONS]`
    """
    containers: types.Containers = filter_containers_by_image(
        request.path_params["image_id"], client
    )

    return JSONResponse(container_as_dict(containers))
