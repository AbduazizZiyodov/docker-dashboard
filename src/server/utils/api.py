# All rest-api utils included
import typing as t

from docker import DockerClient
from docker.models.images import Image
from docker.models.containers import Container


def parse_image_name(image: Image) -> str:
    """Function for getting name of image from image model.
    Note: str(image) is equvalient to image.__str__.
    By using this we can extract name of image.
    e.g str(<docker.Image>) will print <Image: 'nginx:latest'>

    If image is pulled wrong way, this image
    may not have correct name (or name could be like a null). 
    For these kind of cases we will return <none> (docker CLI).
    """
    image_name = str(image).split("'")[1].split(":")[0]
    return "<none>" if len(image_name) == 0 else image_name


def get_additional_info(client: DockerClient, term: str) -> t.Union[dict, None]:
    """This function helps us to extract additional info from docker hub.
    We will use it in case of details of pulled image are not enough.
    e.g If you pulled nginx image, you can't get information about `repository stars`.

    Function sends search request to dockerhub, and manipulates response data.
    Name of images could be like this:
    * nginx (length of slashes = 0)
    * username/repository (length of slashes = 1)
    * gcr.io/k8s-minikube/kicbase ((length of slashes > 1)  # spec.case
    """
    term_original = term

    if len(term_split := term.split("/")) > 1:  # spec.case
        # from the example above: gcr.io/k8s-minikube/kicbase -> k8s-minikube (first index, second element)
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
        image_name = parse_image_name(image)

        # basic attrs that we need
        attrs: list[str] = ["id", "short_id", "labels"]

        if len(image.tags) == 0:  # if you saw SDK docs, image.tag == image.name
            image_dict["name"] = image_name
        else:
            # e.g If tag is nginx:latest. [0] -> nginx and [1] -> latest
            image_dict["name"] = image.tags[0].split(":")[0]
            image_dict["tag"] = image.tags[0].split(":")[1]

        for attr in attrs:
            # retrieve basic info from attrs
            image_dict[attr] = getattr(image, attr)

        if additional_info and image_name != "<none>" and len(image.tags) > 0:
            # check if we need additional info, then reuse util function.
            if (info := get_additional_info(client, image_name)) is not None:
                # if there are some info (!None), update our image_dict
                # we will not need name attr from add. info, because we already have this
                info.pop("name")
                image_dict = {**image_dict, **info}

        return image_dict
    # If there are many images, apply function all of them
    if isinstance(images, list):
        return list(map(build_dict, images))

    return build_dict(images)


def filter_containers_by_image(image_short_id: str, client: DockerClient)\
        -> t.List[Container]:
    """Filter by image short ID (simple)
    """
    filter_results = filter(
        lambda container: container.image.short_id == image_short_id,
        client.containers.list(all=True)
    )

    return list(filter_results)


def container_as_dict(containers: t.Union[t.List[Container], Container]) -> dict:
    """Convert container model to python dictionary.
    """
    def convert(container: Container) -> dict:
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
        return list(map(convert, containers))

    return convert(containers)
