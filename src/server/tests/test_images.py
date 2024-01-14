import pytest
from httpx import AsyncClient
import starlette.status as status

from server.tests.settings import *


def filter_images(images: list) -> list:
    return list(filter(lambda image: image["name"] == TEST_IMAGE_NAME, images))


async def test_get_images(client: AsyncClient):
    response = await client.get("images")

    assert response.status_code == status.HTTP_200_OK
    assert response.text is not None

    pytest.IMAGE_ID = filter_images(response.json())[0]["short_id"]


async def test_get_image(client: AsyncClient):
    response = await client.get(f"images/{pytest.IMAGE_ID}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["short_id"] == pytest.IMAGE_ID


async def test_search_image(client: AsyncClient):
    response = await client.post("images/search", json={"term": TEST_IMAGE_NAME})

    assert response.status_code == status.HTTP_200_OK
    assert TEST_IMAGE_NAME in [image["name"] for image in response.json()]


async def test_get_containers_by_image(client: AsyncClient):
    async def on_begin():
        response = await client.post("containers/run", json={"image": TEST_IMAGE_NAME})

        assert response.status_code == status.HTTP_201_CREATED
        pytest.CONTAINER_ID = response.json()["short_id"]

    await on_begin()

    response = await client.get(f"images/{pytest.IMAGE_ID}/containers")

    assert all(
        [
            container["image"]["name"].startswith(TEST_IMAGE_NAME)
            for container in response.json()
        ]
    )

    assert response.status_code == status.HTTP_200_OK


async def test_delete_container_before_image(client: AsyncClient):
    query_param: str = "force_remove=true"
    response = await client.delete(
        f"containers/{pytest.CONTAINER_ID}/remove?{query_param}"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_image(client: AsyncClient):
    response = await client.delete(f"images/{TEST_IMAGE_NAME}/remove")

    assert response.status_code == status.HTTP_204_NO_CONTENT
