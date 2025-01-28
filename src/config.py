from decouple import config

DEBUG: bool = config("DEBUG", cast=bool, default=True)
OPENAPI_TITLE: str = config("OPENAPI_TITLE", default="RestAPI")
WEBHOOK_SECRET: str = config("WEBHOOK_SECRET", default=None)
