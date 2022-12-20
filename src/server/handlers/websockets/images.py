import aiodocker
import typing as t
import nest_asyncio

from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

from server.utils.tasks import Manager
from server.schemas.image import DockerPullRequest
from server.utils.websocket import validate_websocket_request


NoneType = type(None)
client, task_manager = aiodocker.Docker(), Manager()

nest_asyncio.apply()


class PullImages(WebSocketEndpoint):
    encoding: str = "json"

    async def on_connect(self, ws: WebSocket) -> NoneType:
        await ws.accept()

    async def match_and_perform_action(self, ws: WebSocket, data: t.Any) -> NoneType:
        for method in dir(self):
            if callable(getattr(self, method)):
                if method.startswith(data.action):
                    await self.__getattribute__(method)(ws, data)
                    return
        await ws.send_json({"status": None})

    async def on_receive(self, ws: WebSocket, data: t.Any) -> NoneType:
        body, error = await validate_websocket_request(data)

        if error:
            await ws.send_json(error)
        else:
            await self.match_and_perform_action(ws, body)
            await ws.send_json(task_manager.list())

    async def list_task(self, *_) -> NoneType:
        ...

    async def create_task(self, _, body: DockerPullRequest) -> NoneType:
        task_manager.create(body)

    async def delete_task(self, _, body: DockerPullRequest) -> NoneType:
        task_manager.delete(body)

    async def start_task(self, ws: WebSocket, body: DockerPullRequest) -> NoneType:
        if not task_manager.check_existence_of_task(body):
            await ws.send_json({"detail": "You must create task! (before starting it)"})
            return
        try:
            async for stream_body in client.images.pull(
                body.repository,
                tag=body.tag,
                stream=True
            ):
                task_manager.update(body, stream_body)
                await ws.send_json(task_manager.list())

            task_manager.delete(body)

        except aiodocker.exceptions.DockerError as exc:
            await ws.send_json({"error": exc.message})
