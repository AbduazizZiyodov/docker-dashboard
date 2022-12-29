import typing as t
from pydantic import BaseModel


class ContainerOptions(BaseModel):
    image: str
    name: t.Optional[str]
    ports: t.Optional[dict]
    command: t.Optional[t.Union[str, list]]
    labels: t.Optional[t.Union[dict, list]]
    environment: t.Optional[t.Union[dict, list]]
