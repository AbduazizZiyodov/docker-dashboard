DOCKER_EXEC_COMMAND=/bin/sh
WEBSOCKET_TEST_PATH=server/tests/test_websockets.py
CONTAINER_NAME=docker-dashboard
IMAGE_NAME=abduaziz/docker-dashboard

run:
	@cd src/ && uvicorn server.asgi:application --reload --port 2121 && cd ..

test:
	@cd src/ && pytest -s server/

testws:
	@cd src/ && pytest -s $(WEBSOCKET_TEST_PATH)

shell:
	@docker exec -it $(CONTAINER_NAME) $(DOCKER_EXEC_COMMAND)
