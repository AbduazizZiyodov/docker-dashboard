from pydantic import BaseModel
from starlette.exceptions import HTTPException
from typing import TypeAlias, Optional, Union, Tuple, List, Dict

from docker.models.images import Image
from docker.errors import DockerException
from docker.models.containers import Container

ModelOrDict: TypeAlias = Tuple[BaseModel, Union[None, Dict[str, dict]]]

HttpDockerException = Union[HTTPException, DockerException]

Images: TypeAlias = List[Image]
Containers: TypeAlias = List[Container]


from typing import Protocol, TypeVar, runtime_checkable

T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class SupportsRead(Protocol[T_co]):
    def read(self, __length: int = ...) -> T_co:
        ...
