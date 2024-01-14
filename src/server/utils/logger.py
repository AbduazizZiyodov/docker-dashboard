import logging
import typing as t
from os import PathLike


def configure_logger(
    log_file_name: str | PathLike[str] = "docker_dashboard.log",
) -> logging.Logger:
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)-5.5s] -> %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.FileHandler(log_file_name)],
    )

    return logging.getLogger("events_logger")
