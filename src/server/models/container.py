import typing as t
from enum import StrEnum
from pydantic import BaseModel
from datetime import datetime

from server.models.image import DockerImageResponse


class ContainerStatusEnum(StrEnum):
    dead = "dead"
    exited = "exited"
    paused = "paused"
    running = "running"
    created = "created"
    restarting = "restarting"


class KillSignals(StrEnum):
    SIGINT = "SIGINT"
    SIGHUP = "SIGHUP"
    SIGQUIT = "SIGQUIT"
    SIGKILL = "SIGKILL"
    SIGTERM = "SIGTERM"
    SIGSTOP = "SIGSTOP"


class ContainerRunOptions(BaseModel):
    image: str
    name: t.Optional[str] = None
    ports: t.Optional[dict] = None
    command: t.Optional[t.Union[str, list]] = None
    labels: t.Optional[t.Union[dict, list]] = None
    environment: t.Optional[t.Union[dict, list]] = None
    working_dir: t.Optional[str] = None


class ContainerResponse(BaseModel):
    id: str
    name: str
    ports: dict
    created: datetime
    status: ContainerStatusEnum
    labels: dict[str, t.Any]
    image: DockerImageResponse


class ContainerActionStatusResponse(BaseModel):
    container_id: str
    status: ContainerStatusEnum


class ContainerLogsResponse(BaseModel):
    logs: str
    container_id: str
    container_name: str
