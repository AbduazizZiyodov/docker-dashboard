from fastapi import FastAPI

from src.endpoints import router

application = FastAPI()

application.include_router(router)
