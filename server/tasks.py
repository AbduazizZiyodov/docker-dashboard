import os
import yaml
import typing as t

from pydantic import ValidationError

from server.logging import log
from server.schemas import TaskFile, Task

Tasks = list[Task]

__TASKS: Tasks = list()


def get_tasks() -> list[Task]:
    return __TASKS


def load_tasks(file_path: str) -> None:
    global __TASKS
    task_file = parse_task_definitions(file_path)

    __TASKS = task_file.tasks


def parse_task_definitions(file_path: str) -> TaskFile | t.Never:
    try:
        return parse_and_validate_task_file(file_path)
    except FileNotFoundError:
        log.error(f"File in {file_path} cannot be found, make sure that file exists")
        raise SystemExit(os.EX_DATAERR)


def parse_and_validate_task_file(file_path: str) -> TaskFile | t.Never:
    with open(file_path) as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)

        except yaml.YAMLError as exc:
            log.info(f"Cannot load YAML file: {exc=}")
            raise SystemExit(os.EX_DATAERR)
        else:
            return validate_task_file(file_path, parsed_yaml)


def validate_task_file(file_path: str, parsed_yaml: dict) -> TaskFile | t.Never:
    try:
        return TaskFile.model_validate(parsed_yaml)
    except ValidationError as exc:
        log.error(
            f"Task file({file_path}) validation is failed. Details from pydantic:\n {exc.json(indent=4)}"
        )
        raise SystemExit(os.EX_DATAERR)
