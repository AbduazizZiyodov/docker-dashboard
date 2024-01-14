import typing as t
from enum import StrEnum
from pydantic import BaseModel

class ContainerStatusEnum(StrEnum):
    dead = "dead"
    exited = "exited"
    paused = "paused"
    running = "running"
    created = "created"
    restarting = "restarting"


class DockerSearchRequest(BaseModel):
    term: str
    limit: t.Optional[int] = 10


class DockerPullRequest(BaseModel):
    action: str
    repository: str
    tag: str = "latest"

    def to_string(self) -> str:
        return f"{self.repository}:{self.tag}"


class ImageResponse(BaseModel):
    tag: str
    name: str
    size: str
    long_id: str
    short_id: str
    labels: dict[str, t.Any]


class ImageSearchResult(BaseModel):
    name: str
    star_count: int
    is_official: bool
    is_automated: bool
    description: str


class ContainerResponseWithoutImage(BaseModel):
    id: str
    name: str
    status: ContainerStatusEnum
    labels: dict[str, t.Any]
