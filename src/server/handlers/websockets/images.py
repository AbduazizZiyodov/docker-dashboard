import aiodocker
import typing as t
from docker.errors import DockerException

from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

from server.models.image import DockerPullRequest
from server.exceptions import websocket_request_handler

client = aiodocker.Docker()


class PullImages(WebSocketEndpoint):
    tasks: set = set({})
    encoding: str = "json"

    async def on_connect(self, ws: WebSocket) -> None:
        await ws.accept()

    async def pull(self, ws: WebSocket, data: DockerPullRequest) -> None:
        stream_data: dict
        async for stream_data in client.images.pull(
            from_image=data.repository, tag=data.tag, stream=True
        ):
            await ws.send_json(stream_data)

    async def on_receive(self, ws: WebSocket, data: t.Any) -> None:
        """Handle `on_receive` event and errors, establish websocket session."""
        pull_data: DockerPullRequest
        pull_data, error = websocket_request_handler(data, DockerPullRequest)

        if error:
            await ws.send_json(error)
            return

        if pull_data.action == "start":
            if pull_data.to_string() in self.tasks:
                try:
                    await self.pull(ws, pull_data)
                    self.tasks.remove(pull_data.to_string())  # remove after pulling
                except (DockerException, aiodocker.exceptions.DockerError) as exc:
                    await ws.send_json({"error": exc.__str__()})
            else:
                await ws.send_json({"error": "Before pulling process, create task!"})

        elif pull_data.action == "add":
            self.tasks.add(pull_data.to_string())
            await ws.send_json(
                {"message": f"Image {pull_data.to_string() } is added to tasks!"}
            )

        elif pull_data.action == "list":
            await ws.send_json(list(self.tasks))

        elif pull_data.action == "delete":
            if pull_data.to_string() in self.tasks:
                self.tasks.remove(pull_data.to_string())
                await ws.send_json(list(self.tasks))

        elif pull_data.action == "clear":
            self.tasks.clear()

        else:
            await ws.send_json({"error": "You picked wrong action!"})
