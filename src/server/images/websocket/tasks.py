from images.schemas import DockerPullRequest


class Tasks:
    def __init__(self) -> None:
        self.storage = []

    @property
    def all(self) -> dict:
        return self.storage

    def create(self, body: DockerPullRequest) -> None:

        if not any(
            [self.match_body_task(body, task)
             for task in self.storage]
        ):
            self.storage.append(
                {
                    "repository": body.repository,
                    "tag": body.tag,
                    "stream": "",
                    "status": "Not started"
                }
            )

    def update(self, body: DockerPullRequest, stream_body: dict) -> None:
        for task in self.storage:
            if self.match_body_task(body, task):
                status, stream_body = self.format_stream_body(stream_body)

                task["status"] = status
                task["stream"] += stream_body

    def delete(self, body: DockerPullRequest) -> None:
        for task in self.storage:
            if self.match_body_task(body, task):
                self.storage.remove(task)

    def match_body_task(self, body: DockerPullRequest, task: dict) -> bool:
        return bool(
            body.repository == task["repository"] and
            body.tag == task["tag"]
        )

    def format_stream_body(self, stream_body: dict) -> tuple:
        keys = stream_body.keys()
        body_text: str = ""

        if "id" in keys:
            body_text += "Id: {} ".format(
                stream_body.get("id")
            )

        if "progress" in keys:
            body_text += "| Progress: {}".format(
                stream_body.get("progress")
            )

        body_text+= "\n"

        return stream_body.get("status"), body_text
