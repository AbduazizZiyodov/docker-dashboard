DOCKER_EXEC_COMMAND=/bin/sh
IMAGE_NAME=docker-dashboard
WEBSOCKET_TEST_PATH=server/tests/test_websockets.py

run:
	@cd src/ && uvicorn server.asgi:application --reload --port 2121 && cd ..

test:
	@cd src/ && pytest -s server/

testws:
	@cd src/ && pytest -s $(WEBSOCKET_TEST_PATH)

shell:
	@docker exec -it $(IMAGE_NAME) $(DOCKER_EXEC_COMMAND)