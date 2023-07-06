from typing import Optional
from pydantic import BaseModel


class DockerSearchRequest(BaseModel):
    term: str
    limit: Optional[int] = 10


class DockerPullRequest(BaseModel):
    action: str
    repository: str
    tag: str = "latest"

    def to_string(self) -> str:
        return f"{self.repository}:{self.tag}"
