from typing import Optional
from pydantic import BaseModel


class DockerSearchRequest(BaseModel):
    term: str
    limit: Optional[int] = 10


class DockerPullRequest(BaseModel):
    action: str
    repository: str
    tag: Optional[str] = "latest"

    @property
    def repo_with_tag(self):
        return f"{self.repository}:{self.tag}"
