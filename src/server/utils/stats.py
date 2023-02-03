import typing as t
from docker import DockerClient
from docker.models.images import Image


def get_image_name_tag(image: Image) -> t.Tuple[str, str]:
    """Get image's name from model.
    Attrs dictionary of image model:
        e.g. RepoTags: ['python:latest']

    Returns tuple, first element is image_name
    second is image_tag
    """
    attrs = image.attrs

    if attrs.get("RepoTags") == []:
        return "<none>", "<none_tag>"

    repo_tag: str = attrs.get("RepoTags")[0].split(":")
    return repo_tag[0], repo_tag[1]


def human_readable_size(size: int = None, image: Image = None, precision: int = 1, system: str = 'decimal') -> str:
    """Converts size (in bytes) to human readable system.
    It can be used with 2 system, docker CLI uses decimal (10's power).
    """
    if not size and image:
        size = image.attrs['Size']

    suffixIndex = 0
    decimal_suffixes = ['Byte', 'KB', 'MB', 'GB', 'TB']
    binary_suffixes = ['Byte', 'KiB', 'MiB', 'GiB', 'TiB']

    if system == 'decimal':
        divisor = min_size = 10**3
        suffixes = decimal_suffixes
    else:
        divisor = min_size = 2**5
        suffixes = binary_suffixes

    while size > min_size and suffixIndex < 4:
        suffixIndex += 1
        size = size/divisor

    return "%.*f%s" % (precision, size, suffixes[suffixIndex])


def calculate_image_disk_space(client: DockerClient):
    images: t.List[Image] = []
    total_images_size: int = 0
    unused_images_size: int = 0

    for image in client.images.list(all=True):

        if image.attrs['RepoTags'] == []:
            unused_images_size += image.attrs['Size']

        total_images_size += image.attrs['Size']

        image_name, _ = get_image_name_tag(image)

        images.append({
            image_name: human_readable_size(image=image),
        })

    return {
        'total': human_readable_size(total_images_size),
        'unsused': human_readable_size(unused_images_size),
        'images ': images
    }
