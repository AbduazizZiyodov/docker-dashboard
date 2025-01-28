from fastapi import FastAPI

from src import config
from src.endpoints import router

application = FastAPI(title=config.OPENAPI_TITLE, debug=config.DEBUG)

application.include_router(router)
