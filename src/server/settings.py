DESCRIPTION: str = """
API for our simple Docker-GUI !
<br>
**Author: Abduaziz Ziyodov**
"""


class Settings:
    FASTAPI_SETTINGS = {
        "title": "API for Docker-GUI",
        "openapi_tags": [
            {
                "name": "Home",
                "description": "Simple route that handles `/`"
            },
            {
                "name": "Containers",
                "description": "Operations with containers"
            },
            {
                "name": "Images",
                "description": "Operations with images"
            },

        ],
        "version": "1.0.0",
        "description": DESCRIPTION,
        "docs_url": '/swagger',
        "debug": True
    }
