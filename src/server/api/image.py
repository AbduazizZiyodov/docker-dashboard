from docker.client import DockerClient
from docker.models.images import Image

from fastapi import APIRouter, Response
import starlette.status as status

import server.types as types
from server.utils.helpers import (
    image_as_dict,
    container_as_dict,
    filter_containers_by_image,
)

from server.models.image import DockerSearchRequest

client = DockerClient().from_env()
router = APIRouter(prefix="/api/images", tags=["Images"])


@router.get("")
async def get_images():
    images: types.Images = client.images.list(all=True)
    response = image_as_dict(images, client)

    return response


@router.get("/{image_id}")
async def get_image(image_id: str):
    image: Image = client.images.get(image_id)
    response: Image = image_as_dict(image, client, True)

    return response


@router.delete("/{image_id}/remove")
async def remove_image(image_id: str) -> Response:
    image: Image = client.images.get(image_id)

    client.images.remove(image.short_id, force=True)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/search")
async def search_image(search_params: DockerSearchRequest):
    results = client.images.search(**search_params.model_dump())

    return results


@router.get("/{image_id}/containers")
async def get_containers_by_image(image_id: str):
    containers: types.Containers = filter_containers_by_image(image_id, client)

    return container_as_dict(containers)
