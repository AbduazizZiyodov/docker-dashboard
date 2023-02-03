import pytest
from httpx import AsyncClient

from .client import *


def filter_images(images: list) -> dict:
    return list(
        filter(
            lambda image: image["name"] == TEST_IMAGE_NAME, images
        )
    )


async def test_get_images(client: AsyncClient):
    response = await client.get("images")

    assert response.status_code == 200
    assert response.text is not None

    pytest.IMAGE_ID = filter_images(response.json())[0]["short_id"]


async def test_get_image(client: AsyncClient):
    response = await client.get(f"images/{pytest.IMAGE_ID}")

    assert response.status_code == 200
    assert response.json()["short_id"] == pytest.IMAGE_ID


async def test_search_image(client: AsyncClient):
    response = await client.post(
        "images/search",
        json={"term": TEST_IMAGE_NAME}
    )

    assert response.status_code == 200
    assert TEST_IMAGE_NAME in [
        image["name"]
        for image in response.json()
    ]


async def test_get_containers_by_image(client: AsyncClient):
    response = await client.post(
        "containers/run",
        json={"image": TEST_IMAGE_NAME}
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


async def test_delete_image(client: AsyncClient):
    response = await client.delete(
        f"images/{TEST_PULL_IMAGE}/delete"
    )

    assert response.status_code == 204
