import typing as t

from docker.client import DockerClient
from docker.models.images import Image

from fastapi import APIRouter
import starlette.status as status
from fastapi.responses import Response, JSONResponse

import server.types as types
from server.utils.helpers import (
    image_as_dict,
    container_as_dict,
    filter_containers_by_image,
)

from server.models.image import (
    ImageResponse,
    ImageSearchResult,
    ContainerResponseWithoutImage,
)


client = DockerClient().from_env()
router = APIRouter(prefix="/api/images", tags=["Images"])


@router.get("", response_model=t.List[ImageResponse])
async def get_images() -> JSONResponse:
    """List images on the server."""
    images: types.Images = client.images.list(all=True)
    return image_as_dict(images, client)


@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(image_id: str):
    """Gets an image by id(short or long)."""
    image: Image = client.images.get(image_id)
    return image_as_dict(image, client, True)


@router.delete("/{image_id}/remove/")
async def remove_image(image_id: str) -> Response:
    """Remove an image. Similar to the ``docker rmi`` command."""
    image: Image = client.images.get(image_id)
    client.images.remove(image.short_id, force=True)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/search/", response_model=t.List[ImageSearchResult])
async def search_image(term: str, limit: t.Optional[int] = 10):
    """Search for images on Docker Hub. Similar to the ``docker search``
    command."""
    search_results = client.images.search(term=term, limit=limit)

    return search_results


@router.get(
    "/{image_id}/containers",
    response_model=t.List[ContainerResponseWithoutImage],
    response_model_exclude=["image"],
)
async def get_containers_by_image(image_id: str):
    """Gets the list of containers that are using this image."""
    containers: types.Containers = filter_containers_by_image(image_id, client)

    return container_as_dict(containers)
