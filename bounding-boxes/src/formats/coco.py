from dataclasses import dataclass
from typing import Dict, List

SUPPORTED_SEGMENTATION_LENGTH = 8


@dataclass
class COCOLicense:
    name: str
    id: int
    url: str


@dataclass
class COCOCategory:
    id: int
    name: str
    supercategory: str


@dataclass
class COCOImage:
    id: int
    width: float
    height: float
    file_name: str
    license: int
    flickr_url: str
    coco_url: str


@dataclass
class COCOAnnotation:
    id: int
    image_id: int
    category_id: int
    """
    Expected a list of 8 numbers, representing four vertices starting from top-left and going clockwise
    """
    segmentation: List[List[float]]

    """
    [x, y, width, height]
    """
    bbox: List[float]
    area: float
    """
    int, but mainly 0/1
    """
    iscrowd: int
    attributes: Dict[str, str | int | bool]


@dataclass
class COCOInfo:
    contributor: str
    date_created: str
    description: str
    url: str
    version: str
    year: int | str


@dataclass
class COCOForInput:
    categories: List[COCOCategory]
    images: List[COCOImage]
    annotations: List[COCOAnnotation]


@dataclass
class COCO(COCOForInput):
    licenses: List[COCOLicense]
    info: COCOInfo


def validate_annotation(annotation):
    """
    Ensure that the segmentation of an annotation has 8 elements,
    or failing that, ensure it has a valid bounding boxes
    """
    bbox = annotation["bbox"]

    shoud_throw = len(bbox) != 4

    if shoud_throw:
        for segmentation in annotation["segmentation"]:
            if not validate_segmentation(segmentation):
                raise Exception(
                    "expect segmentation to be a list-of-list of 8 elements"
                )


def validate_segmentation(segmentation):
    if len(segmentation) != SUPPORTED_SEGMENTATION_LENGTH:
        return False

    return True
