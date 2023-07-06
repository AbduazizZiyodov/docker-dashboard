from docker.client import DockerClient
from starlette.responses import JSONResponse

from server.core.utils import calculate_image_disk_space

client = DockerClient().from_env()


async def disk_space_usage(_) -> JSONResponse:
    return JSONResponse(calculate_image_disk_space(client))
