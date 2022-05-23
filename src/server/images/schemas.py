from typing import Optional
from pydantic import BaseModel


class DockerSearchRequest(BaseModel):
    term: str
    limit: Optional[str]


class DockerPullRequest(BaseModel):
    username: str
    password: str
    repository: str
