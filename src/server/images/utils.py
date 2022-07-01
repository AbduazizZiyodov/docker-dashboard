import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container


def parse_image_name(image: Image) -> str:
    return str(image).split(" ")[1]\
        .split(":")[0] \
        .replace("'", "")


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
    additional_info: bool = False
) -> dict:
    def build_dict(image: Image):
        name = parse_image_name(image)
        attrs: list[str] = ["id", "short_id", "labels"]
        image_dict: dict = {"name": image.tags[0]}

        for attr in attrs:
            image_dict[attr] = getattr(image, attr)

        if additional_info:
            if (info := get_additional_info(client, name)) is not None:
                image_dict = {**image_dict, **info}

        return image_dict

    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def remove_image(image: Image, client: DockerClient) -> None:
    image_name: str = parse_image_name(image)
    client.images.remove(image_name)
    return


def filter_containers_by_image(image_id: str, client: DockerClient) -> t.List[Container]:
    filter_results = filter(
        lambda container: container.image.short_id == image_id,
        client.containers.list(all=True)
    )

    return list(filter_results)
