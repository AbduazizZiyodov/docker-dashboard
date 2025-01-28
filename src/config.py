from decouple import config

DEBUG: bool = config("DEBUG", cast=bool, default=True)
