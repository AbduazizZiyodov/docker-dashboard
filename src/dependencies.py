import hmac
import hashlib

from fastapi import status, Header, HTTPException, Request

from src import config
from src.logging import log

__all__ = ["validate_webhook_secret"]


async def validate_webhook_secret(
    request: Request, x_hub_signature_256_header: str | None = Header(default=None)
) -> None:
    request_payload: bytes = await request.body()

    if not (check_signature(request_payload, x_hub_signature_256_header)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook secret, check the value of x_hub_signature_256 header from request",
        )


def check_signature(
    request_payload: bytes, x_hub_signature_256_header: str | None
) -> bool:
    if x_hub_signature_256_header is None or "=" not in x_hub_signature_256_header:
        return False

    _, signature = x_hub_signature_256_header.split("=")
    calculated_signature: str = calc_signature_from_payload(request_payload)

    log.debug(f"Checking signature: {signature=} {calculated_signature=}")

    return calculated_signature == signature


def calc_signature_from_payload(payload: bytes) -> str:
    """Reference: https://stackoverflow.com/a/69474148/15695328"""

    signature_bytes = bytes(config.WEBHOOK_SECRET, "utf-8")

    digest: hmac.HMAC = hmac.new(
        key=signature_bytes,
        msg=payload,
        digestmod=hashlib.sha256,
    )
    signature = digest.hexdigest()

    return signature
