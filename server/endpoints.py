from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from server.logging import log
from server.schemas import WebhookPushEventPayload
from server.dependencies import validate_webhook_secret
from server.actors import process_push_event

router = APIRouter()


@router.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@router.post("/github", dependencies=[Depends(validate_webhook_secret)])
async def process_webhook(payload: WebhookPushEventPayload) -> JSONResponse:
    log.info(
        f"Received PUSH event webhook request from github ... hook_id={payload.hook_id} repository={payload.repository.name}"
    )
    process_push_event.send(payload.model_dump())
    return JSONResponse(content={"status": "ok"})
