import pytest
import starlette.status as status

from server.tests.settings import *


from starlette.testclient import TestClient
from starlette.websockets import WebSocket


CONNECTION_MESSAGE: str = "Connection established"
TEST_REPO: str = "python"
TEST_TAG: str = "3.10-alpine"


def test_websocket_connection() -> None:
    websocket: WebSocket
    client = TestClient(app=application)
    with client.websocket_connect("websocket/images/pull") as websocket:
        data = websocket.receive_text()
        assert data == CONNECTION_MESSAGE


def test_add_tasks() -> None:
    websocket: WebSocket
    client = TestClient(app=application)
    with client.websocket_connect("websocket/images/pull") as websocket:
        data: str = websocket.receive_text()
        websocket.send_json({"repository": TEST_REPO, "tag": TEST_TAG, "action": "add"})
        websocket.send_json(
            {"repository": TEST_REPO, "tag": TEST_TAG, "action": "list"}
        )
        data: dict = websocket.receive_json()

        assert "message" in data.keys()
        assert TEST_REPO in data["message"]


def test_list_of_tasks() -> None:
    websocket: WebSocket
    client = TestClient(app=application)
    with client.websocket_connect("websocket/images/pull") as websocket:
        data: str = websocket.receive_text()
        websocket.send_json(
            {"repository": TEST_REPO, "tag": TEST_TAG, "action": "list"}
        )

        data: dict = websocket.receive_json()

        assert f"{TEST_REPO}:{TEST_TAG}" in data


def test_delete_tasks() -> None:
    websocket: WebSocket
    client = TestClient(app=application)
    with client.websocket_connect("websocket/images/pull") as websocket:
        data: str = websocket.receive_text()
        websocket.send_json(
            {"repository": TEST_REPO, "tag": TEST_TAG, "action": "delete"}
        )

        data: dict = websocket.receive_json()

        assert f"{TEST_REPO}:{TEST_TAG}" not in data


def test_pull_images() -> None:
    websocket: WebSocket
    client = TestClient(app=application)
    with client.websocket_connect("websocket/images/pull") as websocket:
        data: str = websocket.receive_text()
        request_body = {"repository": TEST_REPO, "tag": TEST_TAG, "action": ""}

        # try to send another action
        request_body["action"] = "some_action"

        websocket.send_json(request_body)
        data: dict = websocket.receive_json()
        assert "error" in data.keys()

        # try to create new task
        request_body["action"] = "add"

        websocket.send_json(request_body)
        data: dict = websocket.receive_json()

        assert f"{TEST_REPO}:{TEST_TAG}" in data["message"]

        # list of tasks
        request_body["action"] = "list"

        websocket.send_json(request_body)
        data: list = websocket.receive_json()

        assert data.__len__() > 0 and f"{TEST_REPO}:{TEST_TAG}" in data
