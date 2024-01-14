import aiodocker
import typing as t
from docker.errors import DockerException

import json
from pydantic import ValidationError

from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

from server.models.image import DockerPullRequest

client = aiodocker.Docker()


def websocket_request_handler(data: dict, Model: t.Any) -> t.Any:
    try:
        return Model.parse_obj(data), None
    except ValidationError as exc:
        return None, json.loads(exc.json())


class PullImages(WebSocketEndpoint):
    """Websocket endpoint"""

    tasks: set = set({})
    encoding: str = "json"

    async def on_connect(self, ws: WebSocket) -> None:
        await ws.accept()

    async def on_receive(self, ws: WebSocket, data: t.Any) -> None:
        """Handle `on_receive` event and errors, establish websocket session."""
        pull_data: DockerPullRequest
        pull_data, error = websocket_request_handler(data, DockerPullRequest)

        if error:
            await ws.send_json(error)
            return

        if pull_data.action == "start":
            await self.handle_start(ws, pull_data)

        elif pull_data.action == "add":
            await self.handle_add(ws, pull_data)

        elif pull_data.action == "list":
            await ws.send_json(list(self.tasks))

        elif pull_data.action == "delete":
            await self.handle_delete(ws, pull_data)

        elif pull_data.action == "clear":
            self.tasks.clear()

        else:
            await ws.send_json({"error": "You picked wrong action!"})

    async def pull(self, ws: WebSocket, data: DockerPullRequest) -> None:
        """Pull docker image, and stream chunks through websocket."""
        stream_data: dict
        async for stream_data in client.images.pull(
            data.repository, tag=data.tag, stream=True
        ):
            await ws.send_json(stream_data)

    async def handle_start(self, ws: WebSocket, pull_data: DockerPullRequest) -> None:
        """Handle start event, check existance of task. Then pull docker image."""

        if pull_data.to_string() in self.tasks:
            try:
                await self.pull(ws, pull_data)
                self.tasks.remove(pull_data.to_string())  # remove after pulling
            except (DockerException, aiodocker.exceptions.DockerError) as exc:
                await ws.send_json({"error": str(exc)})
        else:
            await ws.send_json({"error": "Before pulling process, create task!"})

    async def handle_add(self, ws: WebSocket, pull_data: DockerPullRequest) -> None:
        self.tasks.add(pull_data.to_string())
        await ws.send_json(
            {"message": f"Image {pull_data.to_string() } is added to tasks!"}
        )

    async def handle_delete(self, ws: WebSocket, pull_data: DockerPullRequest) -> None:
        if pull_data.to_string() in self.tasks:
            self.tasks.remove(pull_data.to_string())
            await ws.send_json(list(self.tasks))
