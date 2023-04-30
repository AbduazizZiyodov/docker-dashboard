import aiodocker
import typing as t

from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint

from server.models.image import DockerPullRequest
from server.exceptions import websocket_request_handler

client = aiodocker.Docker()


class PullImages(WebSocketEndpoint):
    encoding: str = "json"

    async def on_connect(self, ws: WebSocket) -> None:
        await ws.accept()

    async def on_receive(self, ws: WebSocket, data: t.Any) -> None:
        """Handle `on_receive` event and errors, establish websocket session."""
        pull_data: DockerPullRequest
        pull_data, error = websocket_request_handler(data, DockerPullRequest)
        if error:
            await ws.send_json(error)
        else:
            stream_data: dict
            async for stream_data in client.images.pull(
                from_image=pull_data.repository, tag=pull_data.tag, stream=True
            ):
                await ws.send_json(stream_data)
