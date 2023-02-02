import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container


def get_image_name_tag(image: Image) -> t.Tuple[str,str]:
    """Get image's name from model.
    Attrs dictionary of image model:
        e.g. RepoTags: ['python:latest']
    
    Returns tuple, first element is image_name
    second is image_tag
    """
    attrs = image.attrs

    if attrs.get("RepoTags") == []:
        return "<none>","<none_tag>"

    repo_tag:str = attrs.get("RepoTags")[0].split(":")
    return repo_tag[0], repo_tag[1]


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
        image_dict['short_id'] = format_id(getattr(image, 'short_id'))
        image_dict['size'] = human_readable_size(image.attrs.get('Size'))
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


def human_readable_size(size,precision:int=1,system:str = 'decimal')->str:
    """Converts size (in bytes) to human readable system.
    It can be used with 2 system, docker CLI uses decimal (10's power).
    """
    suffixIndex = 0
    decimal_suffixes=['Byte','KB','MB','GB','TB']
    binary_suffixes=['Byte','KiB','MiB','GiB','TiB']

    if system == 'decimal':
        divisor = min_size = 10**3
        suffixes = decimal_suffixes 
    else:
        divisor = min_size = 2**5
        suffixes = binary_suffixes 

    while size > min_size and suffixIndex < 4:
        suffixIndex += 1
        size = size/divisor

    return "%.*f%s"%(precision,size,suffixes[suffixIndex])


def format_id(element_id:str)->str:
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