import pytest
import docker

from server.tests.settings import *


@pytest.fixture(scope="session", autouse=True)
def fixture():
    """Before running test cases, TEST_IMAGE will be pulled."""
    print(f"\n[PULLING]: {TEST_IMAGE_NAME}")
    docker_client = docker.from_env()
    pulled_image = docker_client.images.pull(
        TEST_IMAGE_NAME,
        tag=TEST_IMAGE_TAG,
    )
    print(f"[PULLED]: {TEST_IMAGE_NAME}, id: {pulled_image.short_id}")
