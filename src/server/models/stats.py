import typing as t

from pydantic import BaseModel


class DockerInfo(BaseModel):
    api_version: str
    go_version: str
    platform_name: str
    platform_version: str


class SystemWideInfo(BaseModel):
    class ContainersInfo(BaseModel):
        total: int
        paused: int
        running: int
        stopped: int

    class OsInfo(BaseModel):
        type: str
        version: str
        name: str

    os: OsInfo
    containers: ContainersInfo
    root_dir: str
    kernel_version: str
    images: int
    cpu_count: int
    total_memory: str

class DockerAndSystemInfo(BaseModel):
    docker_info:DockerInfo
    system_wide_info:SystemWideInfo