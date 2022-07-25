from typing import Optional
from pydantic import BaseModel


class DockerSearchRequest(BaseModel):
    term: str
    limit: Optional[int] = 10


class DockerPullRequest(BaseModel):
    repository: str
    tag: Optional[str] = "latest"
