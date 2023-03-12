import asyncio
import aiodocker
import typing as t
import nest_asyncio

from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

from server.utils import (
    tasks as task_utils,
    api as api_utils,
    websocket as websocket_utils,
)
from server.models.image import DockerPullRequest

client, task_manager = aiodocker.Docker(), task_utils.Manager()

nest_asyncio.apply()


class PullImages(WebSocketEndpoint):
    encoding: str = "json"

    async def on_connect(self, ws: WebSocket) -> t.NoReturn:
        await ws.accept()

    async def match_and_perform_action(self, ws: WebSocket, data: t.Any) -> t.NoReturn:
        """Handle websocket request, perform action.
        [task - image for pulling from dockerhub]
        """
        if data.action == "list":
            await ws.send_json(task_manager.list())
            return
        elif data.action == "create":
            await self.create_task(data)
        elif data.action == "start":
            await self.start_task(ws, data)
        elif data.action == "delete":
            await self.delete_task(data)
        else:
            await ws.send_json({"status": None})

        await ws.send_json(task_manager.list())

    async def on_receive(self, ws: WebSocket, data: t.Any) -> t.NoReturn:
        body, error = await websocket_utils.validate_websocket_request(data)

        if error:
            await ws.send_json(error)
            return

        # If there are no any errors, we should handle this request
        await self.match_and_perform_action(ws, body)

    async def create_task(self, body: DockerPullRequest) -> t.NoReturn:
        task_manager.create(body)

    async def delete_task(self, body: DockerPullRequest) -> t.NoReturn:
        task_manager.delete(body)

    async def start_task(self, ws: WebSocket, body: DockerPullRequest) -> t.NoReturn:
        """Pull image from dockerhub. image.pulled = task.completed.
        Handler streams pulling progress, nest_asyncio allows us
        to pull many images at the same time.
        """
        if not task_manager.check_existence_of_task(body):
            await ws.send_json({"detail": "First, you need to create a task."})
            return

        try:
            async for stream_body in client.images.pull(
                body.repository, tag=body.tag, stream=True
            ):
                task_manager.update(body, stream_body)
                await ws.send_json(task_manager.list())
            # if task.completed, then delete it.
            task_manager.delete(body)

        except aiodocker.exceptions.DockerError as exc:
            await ws.send_json({"error": exc.message})
