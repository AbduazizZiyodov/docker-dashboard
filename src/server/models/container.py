import typing as t
from pydantic import BaseModel


class ContainerOptions(BaseModel):
    image: str
    name: t.Optional[str] = None
    ports: t.Optional[dict] = None
    command: t.Optional[t.Union[str, list]] = None
    labels: t.Optional[t.Union[dict, list]] = None
    environment: t.Optional[t.Union[dict, list]] = None
