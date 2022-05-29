import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container


def parse_image_name(image: Image) -> str:
    return str(image).split(" ")[1]\
        .split(":")[0] \
        .replace("'", "")


def image_as_dict(images: t.Union[t.List[Image], Image]):
    def util(image: Image):
        return dict(
            id=image.id,
            name=parse_image_name(image),
            short_id=image.short_id,
            labels=image.labels,
        )

    if isinstance(images, list):
        return list(map(util, images))

    return util(images)


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
