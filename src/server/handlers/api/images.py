import docker
import typing as t

from docker.models.images import Image
from docker.models.containers import Container

import starlette.status as status
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from server.utils.api import (
    image_as_dict,
    container_as_dict,
    filter_containers_by_image
)

from server.schemas import DockerSearchRequest, DockerPullRequest

client = docker.from_env()


async def get_images(_) -> JSONResponse:
    images: t.List[Image] = client.images.list(all=True)
    response = image_as_dict(images, client)

    return JSONResponse(response)


async def get_image(request: Request) -> JSONResponse:
    image: Image = client.images.get(
        request.path_params["image_id"]
    )
    response: Image = image_as_dict(image, client, True)

    return JSONResponse(response)


async def delete_image(request: Request) -> JSONResponse:
    image: Image = client.images.get(
        request.path_params["image_id"]
    )

    client.images.remove(image.short_id, force=True)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def search_image(request: Request) -> JSONResponse:
    request_body: DockerSearchRequest = DockerSearchRequest(
        **await request.json()
    )

    results = client.images.search(**request_body.dict())

    return JSONResponse(results)


async def pull_image(request: Request) -> JSONResponse:
    request_body = DockerPullRequest(**await request.json())
    image: Image = client.images.pull(**request_body.dict())

    return JSONResponse(image_as_dict(image))


async def get_containers_by_image(request: Request) -> JSONResponse:
    image_id: str = request.path_params["image_id"]

    containers: t.List[Container] = filter_containers_by_image(
        image_id, client
    )

    return JSONResponse(container_as_dict(containers))
