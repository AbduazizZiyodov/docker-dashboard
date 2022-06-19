import pytest
from rich import print

from client import *

TEST_IMAGE_NAME: str = "nginx"
client = CustomAsyncTestClient()


async def test_get_containers():
    response = await client.get("containers")

    assert response.status_code == 200
    assert response.text is not None


async def test_run_container():

    response = await client.post(
        "containers/run",
        {"image": TEST_IMAGE_NAME}
    )
    body = response.json()

    assert response.status_code == 201
    assert body["image"]["name"]\
        .startswith(TEST_IMAGE_NAME) == True

    pytest.CONTAINER_ID = body["id"]


async def test_get_container():
    response = await client.get(f"containers/{pytest.CONTAINER_ID}")

    assert response.status_code == 200
    assert response.json()["id"] == pytest.CONTAINER_ID


async def test_stop_container():
    response = await client.get(f"containers/{pytest.CONTAINER_ID}/stop")

    assert response.status_code == 200
    assert response.json()["stopped"] == True

    response = await client.get(f"containers/{pytest.CONTAINER_ID}")
    body = response.json()

    assert body["id"] == pytest.CONTAINER_ID
    assert body["status"] == "exited"


async def test_start_container():
    response = await client.get(f"containers/{pytest.CONTAINER_ID}/start")

    assert response.status_code == 200
    assert response.json()["started"] == True

    response = await client.get(f"containers/{pytest.CONTAINER_ID}")
    body = response.json()

    assert body["id"] == pytest.CONTAINER_ID
    assert body["status"] == "running"


async def test_delete_container():
    response = await client.delete(f"containers/{pytest.CONTAINER_ID}/delete")

    assert response.status_code == 204
