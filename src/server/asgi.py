from starlette.applications import Starlette
from server.settings import STARLETTE_SETTINGS
from server.exceptions import exception_handlers


application = Starlette(**STARLETTE_SETTINGS)

for exception_class, handler in exception_handlers.items():
    application.add_exception_handler(exception_class, handler)
