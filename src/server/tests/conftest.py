import json
import pytest
import docker

from server.tests.settings import *


@pytest.fixture(scope='session', autouse=True)
def fixture():
    """
    We will need docker image for testing.
    Before running test cases, we should pull it.
    """
    print(f"\nPulling docker image: {TEST_IMAGE_NAME}")
    docker_client = docker.from_env()
    pulled_image = docker_client.images.pull(
        TEST_IMAGE_NAME,
        tag=TEST_IMAGE_TAG,

    )
    print(f"Pulled docker imaeg: {TEST_IMAGE_NAME}, id: {pulled_image.short_id}")
