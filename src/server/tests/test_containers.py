import pytest
import starlette.status as status

from server.tests.settings import *


async def test_get_containers(client: AsyncClient):
    response = await client.get("containers")

    assert response.status_code == status.HTTP_200_OK
    assert response.text is not None


async def test_run_container(client: AsyncClient):
    response = await client.post("containers/run", json={"image": TEST_IMAGE_NAME})
    body = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert body["image"]["name"].startswith(TEST_IMAGE_NAME) == True

    pytest.CONTAINER_ID = body["id"]


async def test_get_container(client: AsyncClient):
    response = await client.get(f"containers/{pytest.CONTAINER_ID}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == pytest.CONTAINER_ID


async def test_stop_container(client: AsyncClient):
    response = await client.get(f"containers/{pytest.CONTAINER_ID}/stop")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["stopped"] == True

    response = await client.get(f"containers/{pytest.CONTAINER_ID}")
    body = response.json()

    assert body["id"] == pytest.CONTAINER_ID
    assert body["status"] == "exited"


async def test_start_container(client: AsyncClient):
    response = await client.get(f"containers/{pytest.CONTAINER_ID}/start")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["started"] == True

    response = await client.get(f"containers/{pytest.CONTAINER_ID}")
    body = response.json()
    assert body["id"] == pytest.CONTAINER_ID
    assert body["status"] == "running"


async def test_delete_container(client: AsyncClient):
    query_param: str = "force=true"
    response = await client.delete(
        f"containers/{pytest.CONTAINER_ID}/delete?{query_param}"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
