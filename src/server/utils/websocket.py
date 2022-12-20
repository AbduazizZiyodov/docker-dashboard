import json
import typing as t
from pydantic import ValidationError, BaseModel

from server.schemas import DockerPullRequest

NoneType = type(None)


async def validate_websocket_request(data: dict, PydanticModel: BaseModel = DockerPullRequest) -> \
        t.Tuple[BaseModel, t.Union[NoneType, t.Dict[str, dict]]]:
    try:
        body = PydanticModel(**data)

        if body.__repr_name__ == "DockerPullRequest":
            if body.action == "create" and len(body.repository) == 0:
                return None, {"detail": "Repository can't be None if action == create"}
        return body, None
    except ValidationError as exc:
        return None, {"detail": json.loads(exc.json())}
