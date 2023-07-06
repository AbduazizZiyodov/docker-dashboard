from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from server.urls import routes

routes += [Route("/", lambda _: JSONResponse("ok"), methods=["GET"])]

STARLETTE_SETTINGS: dict = {
    "routes": routes,
    "middleware": [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
}
