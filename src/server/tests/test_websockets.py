from server.tests.settings import *


from starlette.testclient import TestClient
from starlette.testclient import WebSocketTestSession

import nest_asyncio

nest_asyncio.apply()

CONNECTION_MESSAGE: str = "Connection established"
TEST_REPO: str = "python"
TEST_TAG: str = "3.10-alpine"

client = TestClient(app=application)
request_body = {"repository": TEST_REPO, "tag": TEST_TAG, "action": ""}


def test_add_tasks() -> None:
    websocket: WebSocketTestSession
    with client.websocket_connect("websocket/images/pull") as websocket:
        request_body["action"] = "add"
        websocket.send_json(request_body)
        data: dict = websocket.receive_json()

        assert "message" in data.keys()
        assert TEST_REPO in data["message"]


def test_list_of_tasks() -> None:
    websocket: WebSocketTestSession
    with client.websocket_connect("websocket/images/pull") as websocket:
        request_body["action"] = "list"
        websocket.send_json(request_body)

        data: dict = websocket.receive_json()

        assert f"{TEST_REPO}:{TEST_TAG}" in data


def test_delete_tasks() -> None:
    websocket: WebSocketTestSession
    with client.websocket_connect("websocket/images/pull") as websocket:
        request_body["action"] = "delete"
        websocket.send_json(request_body)
        data: dict = websocket.receive_json()

        assert f"{TEST_REPO}:{TEST_TAG}" not in data


def test_wrong_action() -> None:
    websocket: WebSocketTestSession
    with client.websocket_connect("websocket/images/pull") as websocket:
        # try to send another action
        request_body["action"] = "some_action"

        websocket.send_json(request_body)
        data: dict = websocket.receive_json()

        assert "error" in data.keys()


def test_pull_images() -> None:
    websocket: WebSocketTestSession
    with client.websocket_connect("websocket/images/pull") as websocket:
        # create new task before pulling
        request_body["action"] = "add"

        websocket.send_json(request_body)
        data: dict = websocket.receive_json()

        assert f"{TEST_REPO}:{TEST_TAG}" in data["message"]

        # complete with pulling ...
