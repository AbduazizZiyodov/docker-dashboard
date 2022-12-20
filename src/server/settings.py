from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from pydantic import ValidationError
from docker.errors import DockerException

from server.exceptions import *
from server.handlers.urls import routes

routes += [
    Route("/", lambda _:JSONResponse("ok"), methods=["GET"])
]

STARLETTE_SETTINGS: dict = {
    "routes": routes,
    "exception_handlers": {
        HTTPException: http_exception_handler,
        DockerException: http_exception_handler,
        ValidationError: pydantic_exception_handler
    },
    "middleware": [
        Middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
}
