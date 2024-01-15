import typing as t

from docker.client import DockerClient

from fastapi import APIRouter
import starlette.status as status
from fastapi.responses import JSONResponse

from pprint import pprint as print

from server.models.stats import DockerAndSystemInfo
from server.utils.helpers import get_docker_and_system_info

client = DockerClient().from_env()
router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("/dashboard", response_model=DockerAndSystemInfo)
async def get_images() -> JSONResponse:
    """Version information from the server and system wide info"""
    return get_docker_and_system_info(client)
