import pytest
from httpx import AsyncClient
from server.asgi import application

TEST_IMAGE_ID: str = None
TEST_IMAGE_NAME: str = "nginx"
TEST_IMAGE_TAG: str = "1.18-alpine"

TEST_PULL_IMAGE: str = "hello-world"


@pytest.fixture
def client():
    global application
    
    (
        (
    )
    )
    return AsyncClient(
        app=application,
        timeout=60*2,  # seconds
        base_url="http://127.0.0.1:2121/api/"
    )


__all__ = [
    "client",
    "application",
    "TEST_IMAGE_NAME",
    "TEST_IMAGE_ID",
    "TEST_IMAGE_NAME",
    "TEST_IMAGE_TAG",
    "TEST_PULL_IMAGE"
]
