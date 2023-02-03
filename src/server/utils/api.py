import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container

from server.utils.stats import (
    human_readable_size, 
    get_image_name_tag
)


def get_additional_info(client: DockerClient, term: str) -> t.Union[dict, None]:
    """Function fetches additional info from dockerhub (stars...)
    Terms may have different pattern.
    * nginx (slashes = 0)
    * username/repository (slashes = 1)
    * gcr.io/k8s-minikube/kicbase (slashes > 1) ! edge case
    """
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
    # in some cases we may not want to get additional information
    additional_info: bool = False,
) -> dict:
    def build_dict(image: Image):
        image_dict: dict = dict()

        # retrieve basic info from attrs
        image_dict['id'] = getattr(image, 'id')
        image_dict['labels'] = getattr(image, 'labels')
        image_dict['size'] = human_readable_size(image=image)
        image_dict['short_id'] = format_id(getattr(image, 'short_id'))
        image_dict['name'], image_dict['tag'] = get_image_name_tag(image)

        if additional_info and image_dict['name'] != "<none>" and len(image.tags) > 0:
            # check if we need additional info, then reuse util function.
            if (info := get_additional_info(client, image_dict['name'])) is not None:
                # if there are some info (!None), update our image_dict
                # we will not need name attr from add. info, because we already have this
                info.pop("name")
                image_dict = {**image_dict, **info}

        return image_dict

    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def container_as_dict(containers: t.Union[t.List[Container], Container]) -> dict:
    """Convert container model to python dictionary.
    """
    def build_dict(container: Container) -> dict:
        return dict(
            id=container.id,
            name=container.name,
            status=container.status,
            short_id=container.short_id,
            labels=container.labels,
            image=image_as_dict(container.image)
        )
    # If there are many container models, apply function all of them
    if isinstance(containers, list):
        return list(map(build_dict, containers))

    return build_dict(containers)


def format_id(element_id: str) -> str:
    return element_id.split(":")[1]


def filter_containers_by_image(image_short_id: str, client: DockerClient)\
        -> t.List[Container]:
    """Filter by image short ID (simple)
    """
    filter_results = filter(
        lambda container: container.image.short_id == image_short_id,
        client.containers.list(all=True)
    )

    return list(filter_results)
