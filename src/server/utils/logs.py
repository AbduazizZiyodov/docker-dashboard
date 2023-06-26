import logging
import typing as t


def configure_logger(
    log_file_name: t.Optional[str] = "docker_dashboard.log",
) -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)-5.5s] -> %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.FileHandler(log_file_name)],
    )

    return logging.getLogger("events_logger")


logger: logging.Logger = configure_logger()


__all__ = [
    "logger",
]
