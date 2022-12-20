import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container


def parse_image_name(image: Image) -> str:
    image_name = str(image).split("'")[1].split(":")[0]
    return "<none>" if len(image_name) == 0 else image_name


def get_additional_info(client: DockerClient, term: str) -> t.Union[dict, None]:
    term_original = term

    if len(term_split := term.split("/")) > 1:
        term = term_split[1]

    results: list[dict] = client.images.search(term=term, limit=10)

    for result in results:
        if result["name"] == term_original:
            return result
    return None


def image_as_dict(
    images: t.Union[t.List[Image], Image],
    client: DockerClient = None,
    additional_info: bool = False,
) -> dict:
    def build_dict(image: Image):
        image_dict: dict = dict()
        image_name = parse_image_name(image)
        attrs: list[str] = ["id", "short_id", "labels"]

        if len(image.tags) == 0:
            image_dict["name"] = image_name
        else:
            image_dict["name"] = image.tags[0].split(":")[0]
            image_dict["tag"] = image.tags[0].split(":")[1]

        for attr in attrs:
            image_dict[attr] = getattr(image, attr)

        if additional_info and image_name != "<none>" and len(image.tags) > 0:
            if (info := get_additional_info(client, image_name)) is not None:
                info.pop("name")
                image_dict = {**image_dict, **info}

        return image_dict

    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def filter_containers_by_image(image_short_id: str, client: DockerClient)\
        -> t.List[Container]:
    filter_results = filter(
        lambda container: container.image.short_id == image_short_id,
        client.containers.list(all=True)
    )

    return list(filter_results)


def container_as_dict(containers: t.Union[t.List[Container], Container]) -> dict:
    def convert(container: Container) -> dict:
        return dict(
            id=container.id,
            name=container.name,
            status=container.status,
            short_id=container.short_id,
            labels=container.labels,
            image=image_as_dict(container.image)
        )

    if isinstance(containers, list):
        return list(map(convert, containers))

    return convert(containers)
