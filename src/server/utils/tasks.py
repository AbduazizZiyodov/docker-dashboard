import typing as t
from pydantic.main import ModelMetaclass

from server.schemas.image import DockerPullRequest


class Task:
    """Simple class that represents tasks for pulling docker images.
    """

    def __init__(self, repository: str, tag: str) -> None:
        self.repository, self.tag = repository, tag
        self.stream_data, self.status = "", ""

    def get(self, __name: str) -> t.Any:
        return super().__getattribute__(__name)

    def __eq__(self, __obj: t.Any) -> bool:
        """Overload equality operator.
        """
        if isinstance(type(__obj), (ModelMetaclass)):
            __obj = __obj.dict()

        if isinstance(__obj, (dict, type(self))):
            return bool(
                self.repository == __obj.get("repository")
                and
                self.tag == __obj.get("tag")
            )

        return False

    def to_dict(self) -> t.Dict[str, str]:
        """From object to dictionary
        """
        return dict(
            repository=self.repository,
            tag=self.tag,
            stream_data=self.stream_data,
            status=self.status
        )


class Manager:
    tasks: t.List[Task] = list()

    def list(self) -> t.List[Task]:
        """Convert all tasks to python dict.
        """
        return list(map(lambda task: task.to_dict(), self.tasks))

    def create(self, body: DockerPullRequest) -> None:
        if not self.check_existence_of_task(body):
            self.tasks.append(Task(body.repository, body.tag))

    def update(self, body: DockerPullRequest, stream: dict) -> None:
        """In the pulling progress, application should update
        stream records. This method takes stream as an argument, 
        adds it to the task's stream data by formatting it.
        """
        for task in self.tasks:
            if task == body:
                status, stream = self.format_stream_body(stream)

                task.status = status
                task.stream_data += stream

    def delete(self, body: DockerPullRequest) -> None:
        for task in self.tasks:
            if task == body:
                self.tasks.remove(task)

    def format_stream_body(self, stream: dict) -> t.Tuple[str, str]:
        body_text: str = ""
        keys = stream.keys()

        if "id" in keys:
            body_text += "Id: {} ".format(
                stream.get("id")
            )

        if "progress" in keys:
            body_text += "| Progress: {}".format(
                stream.get("progress")
            )

        body_text += "\n"

        return stream.get("status"), body_text

    def check_existence_of_task(self, body: DockerPullRequest) -> bool:
        for task in self.tasks:
            if task == body:
                return True
        return False
