from dataclasses import dataclass
from typing import Dict, List


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
