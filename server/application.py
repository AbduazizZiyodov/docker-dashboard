from fastapi import FastAPI

from server import config
from server.endpoints import router

application = FastAPI(title=config.OPENAPI_TITLE, debug=config.DEBUG)

application.include_router(router)
