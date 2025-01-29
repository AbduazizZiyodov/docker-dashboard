from dramatiq import Middleware, Broker, Worker

from server import config
from server.logging import log
from server.tasks import load_tasks, get_tasks


class LoadTasksMiddleware(Middleware):
    def after_worker_boot(self, broker: Broker, worker: Worker) -> None:
        load_tasks(config.TASKS_FILE_PATH)
        log.info(f"Loaded tasks: {get_tasks()}")
