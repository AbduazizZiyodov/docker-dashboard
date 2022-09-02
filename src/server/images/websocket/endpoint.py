import aiodocker
import typing as t
import nest_asyncio

from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint


from images.schemas import DockerPullRequest
from images.utils import validate_websocket_request
from .tasks import Tasks

client, tasks = aiodocker.Docker(), Tasks()

nest_asyncio.apply()


class PullImages(WebSocketEndpoint):
    encoding: str = "json"

    async def on_connect(self, ws: WebSocket) -> None:
        await ws.accept()

    async def on_receive(self, ws: WebSocket, data: t.Any) -> None:
        body, error = await validate_websocket_request(data)

        if error:
            await ws.send_json(error)
            return

        if body.action == "all":
            await ws.send_json(tasks.all)

        elif body.action == "create":
            await self.create_task(ws, body)

        elif body.action == "delete":
            await self.delete_task(ws, body)

        elif body.action == "start":
            await self.start_task(ws, body)
        else:
            await ws.send_json({"status": None})

    async def create_task(self, ws: WebSocket, body: DockerPullRequest) -> None:
        tasks.create(body)
        await ws.send_json(tasks.all)

    async def delete_task(self, ws: WebSocket, body: DockerPullRequest) -> None:
        tasks.delete(body)
        await ws.send_json(tasks.all)

    async def start_task(self, ws: WebSocket, body: DockerPullRequest) -> None:
        try:

            async for stream_body in client.images.pull(
                body.repository,
                tag=body.tag,
                stream=True
            ):
                tasks.update(body, stream_body)
                await ws.send_json(tasks.all)

            tasks.delete(body)

        except aiodocker.exceptions.DockerError as exc:
            await ws.send_json({"error": exc.message})
