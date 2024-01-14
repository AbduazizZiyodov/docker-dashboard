from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.image import router as image_router
from server.api.container import router as container_router

from server.websocket.images import PullImages

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
