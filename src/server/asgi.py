import docker

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.websocket.images import PullImages
from server.api.image import router as image_router
from server.utils.exceptions import exception_handlers
from server.api.container import router as container_router

application = FastAPI(
    redoc_url=None,
    version="2.0.0",
    docs_url="/swagger",
    title="Admiral Rest API",
    summary="Rest API for Admiral",
)

application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

for router in [container_router, image_router]:
    application.include_router(router)


application.add_websocket_route("/websocket/images/pull", PullImages)


for exception_class, handler in exception_handlers.items():
    application.add_exception_handler(exception_class, handler)


@application.get("/", response_model=str)
def docker_ping_request():
    """Checks the server is responsive."""
    return "ok" if bool(docker.DockerClient().ping()) else "!ok"
