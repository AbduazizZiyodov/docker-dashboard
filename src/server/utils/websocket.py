import json
from pydantic import ValidationError, BaseModel

import server.types as types
from server.models import DockerPullRequest


async def validate_websocket_request(data: dict, PydanticModel: BaseModel = DockerPullRequest) -> types.ModelOrDict:
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
