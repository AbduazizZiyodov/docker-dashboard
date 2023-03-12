from pydantic import BaseModel
from starlette.exceptions import HTTPException
from typing import TypeAlias, Optional, Union, Tuple, List, Dict

from docker.models.images import Image
from docker.errors import DockerException
from docker.models.containers import Container

ModelOrDict: TypeAlias = Tuple[BaseModel, Union[None, Dict[str, dict]]]

HttpDockerException = Union[HTTPException, DockerException]

Images:TypeAlias = List[Image]
Containers:TypeAlias = List[Container]