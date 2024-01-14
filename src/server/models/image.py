import typing as t
from pydantic import BaseModel


class DockerSearchRequest(BaseModel):
    term: str
    limit: t.Optional[int] = 10


class DockerPullRequest(BaseModel):
    action: str
    repository: str
    tag: str = "latest"

    def to_string(self) -> str:
        return f"{self.repository}:{self.tag}"


class ImageResponseModel(BaseModel):
    tag: str
    name: str
    size: str
    long_id: str
    short_id: str
    labels: dict[str, t.Any]
