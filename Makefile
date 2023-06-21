run:
	@cd src/ && uvicorn server.asgi:application --reload --port 2121 && cd ..

test:
	@cd src/ && pytest -s server/

testws:
	@cd src/ && pytest -s server/tests/test_websockets.py

shell:
	@docker exec -it docker-dashboard /bin/sh