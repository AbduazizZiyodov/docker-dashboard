from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container

import server.types as types
from server.utils.stats import (
    human_readable_size,
    get_image_name_tag
)


def get_additional_info(client: DockerClient, term: str) -> types.Union[dict, None]:
    """Fetch additional info from docker registry.
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
    images: types.Union[types.Images, Image],
    client: DockerClient = None,
    additional_info: types.Optional[bool] = False, 
) -> dict:
    """Convert docker Image model to python dictionary object
    """
    def build_dict(image: Image):
        image_dict: dict = dict()

        # basic info
        image_dict['labels'] = getattr(image, 'labels')
        image_dict['size'] = human_readable_size(image=image)
        image_dict['long_id'] = format_id(getattr(image, 'id'))
        image_dict['short_id'] = format_id(getattr(image, 'short_id'))
        image_dict['name'], image_dict['tag'] = get_image_name_tag(image)

        if additional_info and image_dict['name'] != "<none>":
            if (info := get_additional_info(client, image_dict['name'])) is not None:
                info.pop("name") # pop duplicates
                image_dict = {**image_dict, **info}

        return image_dict
    
    # for multiple instances
    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def container_as_dict(containers: types.Union[types.Containers, Container]) -> dict:
    """Convert docker Container model to python dictionary object
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
    
    # for multiple instances
    if isinstance(containers, list):
        return list(map(build_dict, containers))

    return build_dict(containers)


def format_id(element_id: str) -> str:
    """Get long ID.
    """
    return element_id.split(":")[1]


def filter_containers_by_image(image_short_id: str, client: DockerClient)\
        -> types.Containers:
    """Filter by image short ID (simple)
    """
    filter_results = filter(
        lambda container: container.image.short_id == image_short_id,
        client.containers.list(all=True)
    )

    return list(filter_results)
