import pytest

from client import *


client = CustomAsyncTestClient()
TEST_IMAGE_NAME = "nginx"
TEST_PULL_IMAGE = "hello-world"


async def test_get_images():
    response = await client.get("images")

    assert response.status_code == 200
    assert response.text is not None

    pytest.IMAGE_ID = response.json()[0]["id"]


async def test_get_image():
    response = await client.get(f"images/{pytest.IMAGE_ID}")

    assert response.status_code == 200
    assert response.json()["id"] == pytest.IMAGE_ID


async def test_search_image():
    response = await client.post(
        f"images/search",
        {"term": TEST_IMAGE_NAME}
    )

    assert response.status_code == 200
    assert TEST_IMAGE_NAME in [
        image["name"]
        for image in response.json()
    ]


async def test_get_containers_by_image():
    response = await client.post(
        "containers/run",
        {"image": TEST_IMAGE_NAME}
    )

    assert response.status_code == 201
    pytest.CONTAINER_ID = response.json()["id"]

    response = await client.get(
        f"images/{pytest.IMAGE_ID}/containers"
    )

    assert all([
        container["image"]["name"].startswith(TEST_IMAGE_NAME)
        for container in response.json()
    ])

    response = await client.delete(
        f"containers/{pytest.CONTAINER_ID}/delete"
    )

    assert response.status_code == 204


async def test_pull_images():
    response = await client.post(
        "images/pull",
        {"repository": TEST_PULL_IMAGE}
    )
    assert response.status_code == 200
    assert response.json()["name"].startswith(TEST_PULL_IMAGE)


async def test_delete_image():
    response = await client.delete(
        f"images/{TEST_PULL_IMAGE}/delete"
    )

    assert response.status_code == 204
