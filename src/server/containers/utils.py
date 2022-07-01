import typing as t
from docker.models.images import Image
from docker.models.containers import Container

from server.images.utils import image_as_dict


def parse_image_name(image: Image) -> str:
    return str(image).split(" ")[1]\
        .split(":")[0] \
        .replace("'", "")


def container_as_dict(containers: t.Union[t.List[Container], Container]):
    def util(container: Container):
        return dict(
            id=container.id,
            name=container.name,
            status=container.status,
            short_id=container.short_id,
            labels=container.labels,
            image=image_as_dict(container.image)
        )

    if isinstance(containers, list):
        return list(map(util, containers))
    return util(containers)
