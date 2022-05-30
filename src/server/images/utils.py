from rich import print
import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container


def parse_image_name(image: Image) -> str:
    return str(image).split(" ")[1]\
        .split(":")[0] \
        .replace("'", "")


def get_additional_info(client: DockerClient, term: str):
    return client.images.search(term=term, limit=1)[0]


def image_as_dict(
    images: t.Union[t.List[Image], Image],
    client: DockerClient = None,
    additional_info: bool = False
) -> dict:

    def build_dict(image: Image):
        name = parse_image_name(image)
        attrs: list[str] = ["id", "short_id", "labels"]
        image_dict: dict = {"name": name}

        for attr in attrs:
            image_dict[attr] = getattr(image, attr)

        if additional_info:
            image_dict = {**image_dict, **get_additional_info(client, name)}

        return image_dict

    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def remove_image(image: Image, client: DockerClient) -> None:
    image_name: str = parse_image_name(image)
    client.images.remove(image_name)
    return


def filter_containers_by_image(image_name: str, client: DockerClient) -> t.List[Container]:
    def filter_image_name(container: Container) -> bool:
        return parse_image_name(container.image) == image_name

    return list(
        filter(
            filter_image_name, client.containers.list(all=True)
        )
    )
