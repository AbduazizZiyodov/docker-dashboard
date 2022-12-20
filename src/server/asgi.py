from starlette.applications import Starlette
from server.settings import STARLETTE_SETTINGS


application = Starlette(**STARLETTE_SETTINGS)
