import logging
import typing as t
from os import PathLike

from docker.client import DockerClient
from docker.models.images import Image
from docker.models.containers import Container

import server.types as types


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


def get_image_name_tag(image: Image) -> list[str]:
    """Get image's name from model.
    Attrs dictionary of image model:
    e.g. RepoTags: ['python:latest']

    Returns tuple, first element is image_name
    second is image_tag
    """
    attrs: dict = image.attrs

    if not (repo_tags := attrs.get("RepoTags")):
        return ["<none>", "<none_tag>"]

    tag: str = repo_tags[0]
    return tag.split(":")


def human_readable_size(
    size: int = 0,
    image: Image | None = None,
    precision: int = 1,
    system: str = "decimal",
) -> str:
    """Converts size (in bytes) to human readable system.
    It can be used with 2 system, docker CLI uses decimal (10's power).
    """
    if not size and image:
        size = image.attrs["Size"]

    suffixIndex: int = 0
    decimal_suffixes: list[str] = ["Byte", "KB", "MB", "GB", "TB"]
    binary_suffixes: list[str] = ["Byte", "KiB", "MiB", "GiB", "TiB"]

    if system == "decimal":
        divisor = min_size = 10**3
        suffixes = decimal_suffixes
    else:
        divisor = min_size = 2**5
        suffixes = binary_suffixes

    while size > min_size and suffixIndex < 4:
        suffixIndex += 1
        size = size // divisor

    return "%.*f%s" % (precision, size, suffixes[suffixIndex])


def calculate_image_disk_space(client: DockerClient):
    images: t.Dict[str, str] = dict()
    total_images_size: int = 0
    unused_images_size: int = 0

    for image in client.images.list(all=True):
        if image.attrs["RepoTags"] == []:
            unused_images_size += image.attrs["Size"]

        total_images_size += image.attrs["Size"]

        image_name, _ = get_image_name_tag(image)

        images[image_name] = human_readable_size(image=image)

    return {
        "total": human_readable_size(size=total_images_size),
        "unsused": human_readable_size(size=unused_images_size),
        "images ": images,
    }


def get_additional_info(client: DockerClient, term: str) -> types.Union[dict, None]:
    """Fetch additional info from docker registry."""
    term_original = term

    if len(term_split := term.split("/")) > 1:
        term = term_split[1]

    results: list[dict] = client.images.search(term=term, limit=10)

    for result in results:
        if result["name"] == term_original:
            logger.debug(f"Search results: {result} for {term}")
            return result

    return None


def image_as_dict(
    images: types.Union[types.Images, Image],
    client: DockerClient = None,
    additional_info: types.Optional[bool] = False,
) -> list[dict] | dict:
    """Convert docker Image model to python dictionary object"""

    logger.debug(images)

    def build_dict(image: Image):
        image_dict: dict = dict()

        # basic info
        image_dict["labels"] = getattr(image, "labels")
        image_dict["size"] = human_readable_size(image=image)
        image_dict["long_id"] = format_id(getattr(image, "id"))
        image_dict["short_id"] = format_id(getattr(image, "short_id"))
        image_dict["name"], image_dict["tag"] = get_image_name_tag(image)

        if additional_info and image_dict["name"] != "<none>":
            if (info := get_additional_info(client, image_dict["name"])) is not None:
                info.pop("name")  # pop duplicates
                image_dict = {**image_dict, **info}

        return image_dict

    # for multiple instances
    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def container_as_dict(
    containers: types.Union[types.Containers, Container]
) -> list[dict] | dict:
    """Convert docker Container model to python dictionary object"""

    logger.debug(containers)

    def build_dict(container: Container) -> dict:
        return dict(
            id=container.id,
            name=container.name,
            status=container.status,
            short_id=container.short_id,
            labels=container.labels,
            image=image_as_dict(container.image),
        )

    # for multiple instances
    if isinstance(containers, list):
        return list(map(build_dict, containers))

    return build_dict(containers)


def format_id(element_id: str) -> str:
    """Get long ID."""
    return element_id.split(":")[1]


def filter_containers_by_image(
    image_short_id: str, client: DockerClient
) -> types.Containers:
    """Filter by image short ID (simple)"""
    filter_results = filter(
        lambda container: container.image.short_id == image_short_id,
        client.containers.list(all=True),
    )

    return list(filter_results)


logger: logging.Logger = configure_logger()
