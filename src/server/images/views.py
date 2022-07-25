import docker
import typing as t

from starlette.routing import Route

from docker.models.images import Image
from docker.models.containers import Container

import starlette.status as status

from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from containers.utils import container_as_dict
from .utils import (
    get_tags,
    image_as_dict,
    sort_tag_versions,
    filter_containers_by_image,
)
from .schemas import DockerSearchRequest, DockerPullRequest


client = docker.from_env()


async def get_images(request: Request) -> JSONResponse:
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


async def get_all_tags(request: Request) -> JSONResponse:
    request_body: dict = await request.json()
    repository = request_body.get("repository")

    tags = await get_tags(repository)

    if not isinstance(tags, list):
        return JSONResponse(
            [],
            status_code=status.HTTP_404_NOT_FOUND
        )

    tags = sort_tag_versions(tags)

    return JSONResponse(tags)


image_routes = [
    Route("/api/images", get_images, methods=["GET"]),
    Route("/api/images/{image_id:str}", get_image, methods=["GET"]),
    Route(
        "/api/images/{image_id:str}/delete",
        delete_image, methods=["DELETE"]
    ),
    Route(
        "/api/images/{image_id:str}/containers",
        get_containers_by_image, methods=["GET"]
    ),
    Route("/api/images/search", search_image, methods=["POST"]),
    Route("/api/images/pull", pull_image, methods=["POST"]),
    Route("/api/images/get-tags", get_all_tags, methods=["POST"]),
]
