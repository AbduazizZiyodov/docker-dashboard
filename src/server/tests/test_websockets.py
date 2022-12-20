import asyncio
from .client import *
from starlette.testclient import WebSocketTestSession


async def test_list_tasks(websocket_client: WebSocketTestSession):
    websocket_client.send_json({"action": "list", "repository": ""})
    data = websocket_client.receive_json()
    assert data == []


async def test_create_task(websocket_client: WebSocketTestSession):
    websocket_client.send_json(
        {"action": "create", "repository": TEST_PULL_IMAGE}
    )
    data = websocket_client.receive_json()
    assert isinstance(data, (list)) and len(data) == 1
    assert any([TEST_PULL_IMAGE in task.values() for task in data])


async def test_create_task(websocket_client: WebSocketTestSession):
    websocket_client.send_json(
        {"action": "delete", "repository": TEST_PULL_IMAGE}
    )
    data = websocket_client.receive_json()
    assert data == []
