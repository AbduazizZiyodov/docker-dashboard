from setuptools import setup, find_packages


setup(
    name="docker_dashboard",
    version="1.0.0",
    description="Backend for lightweight docker dashboard",
    author="Abduaziz Ziyodov",
    author_email="abduaziz.ziyodov@mail.ru",
    url="https://github.com/AbduazizZiyodov/docker-dashboard",
    license="MIT",
    entry_points={
        "console_scripts": ["docker-dashboard=server.manage:main"]
    },
    packages=find_packages(exclude=["env/", "tests/", "__pycache__/"]),
    install_requires=[
        "starlette", "typer", "pydantic",
        "uvicorn", "docker", "httpx"
    ],
    tests_require=[
        "pytest", "httpx", "pytest-asyncio"
    ]
)
