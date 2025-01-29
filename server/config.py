from decouple import config

TASKS_FILE_PATH: str = config("TASKS_FILE_PATH")

SERVER_HOST: str = config("SERVER_HOST", default="127.0.0.1")
SERVER_PORT: int = config("SERVER_PORT", default=2121)

WEBHOOK_SECRET: str = config("WEBHOOK_SECRET")
DEBUG: bool = config("DEBUG", cast=bool, default=True)
OPENAPI_TITLE: str = config("OPENAPI_TITLE", default="RestAPI")

###
# Dramatiq related
###

# broker settings
REDIS_HOST: str = config("REDIS_HOST", default="127.0.0.1")
REDIS_PORT: int = config("REDIS_PORT", default=6379)
REDIS_PASSWORD: str = config("REDIS_PASSWORD", default=None)
