import json
import typing as t
from pydantic import ValidationError, BaseModel

from server.models import DockerPullRequest

NoneType = type(None)


async def validate_websocket_request(data: dict, PydanticModel: BaseModel = DockerPullRequest) -> \
        t.Tuple[BaseModel, t.Union[NoneType, t.Dict[str, dict]]]:
    """Util function for validating websocket requests via pydantic models.
    """
    try:
        if "DockerPullRequest" in str(PydanticModel):
            if data.get("action") == "list":
                data["repository"] = ""

        body = PydanticModel(**data)
        return body, None
        
    except ValidationError as exc:
        return None, {"detail": json.loads(exc.json())}
