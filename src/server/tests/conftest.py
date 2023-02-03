import json
import pytest
import docker


@pytest.fixture(scope='session', autouse=True)
def fixture():
    """
    We will need docker image for testing.
    Before running test cases, we should pull it.
    """
    docker_client = docker.from_env()
    for stream_message in docker_client.api.pull(
        'hello-world',
        tag='latest',
        stream=True
    ):
        data: dict = json.loads(stream_message)

        print(data.get('status'))
