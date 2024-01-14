import typing as t
from enum import StrEnum
from pydantic import BaseModel

from server.models.image import ImageResponse


class ContainerStatusEnum(StrEnum):
    dead = "dead"
    exited = "exited"
    paused = "paused"
    running = "running"
    created = "created"
    restarting = "restarting"


class ContainerRunOptions(BaseModel):
    image: str
    name: t.Optional[str] = None
    ports: t.Optional[dict] = None
    command: t.Optional[t.Union[str, list]] = None
    labels: t.Optional[t.Union[dict, list]] = None
    environment: t.Optional[t.Union[dict, list]] = None


class ContainerResponse(BaseModel):
    id: str
    name: str
    status: ContainerStatusEnum
    labels: dict[str, t.Any]
    image: ImageResponse


class ContainerActionStatusResponse(BaseModel):
    container_id: str
    status: ContainerStatusEnum


class ContainerLogsResponse(BaseModel):
    logs: str
    container_id: str
    container_name: str


class DockerPingResponse(BaseModel):
    success: bool
