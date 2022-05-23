import docker
import typing as t

from starlette.routing import Route

from docker.models.images import Image
from starlette.requests import Request
from starlette.responses import JSONResponse

from .utils import image_as_dict, remove_image
from .schemas import DockerPullRequest, DockerSearchRequest

client = docker.from_env()


async def get_images(request: Request) -> JSONResponse:
    images: t.List[Image] = client.images.list(all=True)
    response = image_as_dict(images)

    return JSONResponse(response)


async def get_image(request: Request) -> JSONResponse:
    image: Image = client.images.get(
        request.path_params["image_id"]
    )
    response: Image = image_as_dict(image)

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


image_routes = [
    Route("/api/images", get_images, methods=["GET"]),
    Route("/api/images/{image_id}", get_image, methods=["GET"]),
    Route("/api/images/{image_id}/delete", delete_image, methods=["DELETE"]),
    Route("/api/images/search", search_image, methods=["POST"]),
    Route("/api/images/pull", pull_image, methods=["POST"]),
]
