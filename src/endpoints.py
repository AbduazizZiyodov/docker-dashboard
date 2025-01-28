from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.logging import log
from src.schemas import WebhookPushEventPayload
from src.dependencies import validate_webhook_secret


router = APIRouter()


@router.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@router.post("/github", dependencies=[Depends(validate_webhook_secret)])
async def process_webhook(payload: WebhookPushEventPayload) -> JSONResponse:
    log.info(f"Received 'push' event from github: {payload}")
    return JSONResponse(content={"status": "ok"})
