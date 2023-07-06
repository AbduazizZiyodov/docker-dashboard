import docker
from starlette.responses import JSONResponse

from server.core.utils import calculate_image_disk_space


client = docker.from_env()


async def disk_space_usage(_) -> JSONResponse:
    return JSONResponse(calculate_image_disk_space(client))
