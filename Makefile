run:
	@cd src/ && uvicorn server.asgi:application --reload --port 2121 && cd ..

test:
	@cd src/ && pytest -s server/