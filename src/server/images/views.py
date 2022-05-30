import docker
import typing as t

from starlette.routing import Route

from docker.models.images import Image
from docker.models.containers import Container

from starlette.requests import Request
from starlette.responses import JSONResponse

from containers.utils import container_as_dict
from .schemas import DockerPullRequest, DockerSearchRequest
from .utils import image_as_dict, remove_image, filter_containers_by_image

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
    remove_image(image, client)

    return JSONResponse({"deleted": True})


async def search_image(request: Request) -> JSONResponse:
    request_body: DockerSearchRequest = DockerSearchRequest(
        **await request.json()
    )

    results = client.images.search(**request_body.dict())

    return JSONResponse(results)


async def pull_image(request: Request) -> JSONResponse:
    request_body: DockerPullRequest = DockerPullRequest(** await request.json())
    image: Image = client.images.pull(
        request_body.repository,
        auth_config={
            "username": request_body.username,
            "password": request_body.password
        }
    )

    return JSONResponse(image_as_dict(image))


async def get_containers_by_image(request: Request) -> JSONResponse:
    image_id: str = request.path_params["image_id"]

    containers: t.List[Container] = filter_containers_by_image(
        image_id, client
    )

    return JSONResponse(container_as_dict(containers))


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
    Route("/api/images/containers", search_image, methods=["POST"]),
]
