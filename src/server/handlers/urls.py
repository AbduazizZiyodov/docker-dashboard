from .api import *
from .websockets import *
from starlette.routing import (
    Route,
    WebSocketRoute
)


container_routes = [
    Route("/api/containers", get_containers, methods=["GET"]),
    Route(
        "/api/containers/{container_id:str}",
        get_container, methods=["GET"]
    ),
    Route(
        "/api/containers/run",
        run_container, methods=["POST"]
    ),
    Route(
        "/api/containers/{container_id:str}/start",
        start_stopped_container, methods=["GET"]
    ),
    Route(
        "/api/containers/{container_id:str}/stop",
        stop_container, methods=["GET"]
    ),
    Route(
        "/api/containers/{container_id:str}/delete",
        delete_container, methods=["DELETE"]
    ),
    Route(
        "/api/containers/{container_id:str}/logs",
        get_logs, methods=["GET"]
    )
]

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
]

websocket_routes = [
    WebSocketRoute("/websocket/images/pull", PullImages),
]


routes = container_routes + image_routes + websocket_routes
