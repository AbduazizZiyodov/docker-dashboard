import dramatiq
from dramatiq.brokers.redis import RedisBroker

from server import config
from server.logging import log
from server.schemas import WebhookPushEventPayload
from server.middlewares import LoadTasksMiddleware

redis_broker = RedisBroker(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
)
dramatiq.set_broker(redis_broker)
redis_broker.add_middleware(LoadTasksMiddleware())


@dramatiq.actor(max_retries=3)
def process_push_event(payload: dict) -> None:
    event: WebhookPushEventPayload = WebhookPushEventPayload.model_validate(payload)

    log.info(f"Processing ... {event.hook_id=}")
    log.info("Done ... !")

    return
