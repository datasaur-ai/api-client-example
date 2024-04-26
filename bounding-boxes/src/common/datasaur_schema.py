from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class GenericIdAndName:
    id: Optional[str]
    name: str


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Shape:
    pageIndex: int
    points: List[Point]


@dataclass
class BBoxLabel:

    id: str
    bboxLabelClassId: str
    bboxLabelClassName: str
    caption: Optional[str]
    shapes: List[Shape]
    """
    tba
    """
    answers: Optional[Dict[str, str | int | bool]]

    # For Datasaur Schema used in input, we can ignore these
    status: Optional[str]
    labeledBy: Optional[str]
    labeledByUserId: Optional[int]
    acceptedByUserId: Optional[int]
    rejectedByUserId: Optional[int]


@dataclass
class BBoxLabelClassQuestions:
    """
    tba
    """

    pass


@dataclass
class BBoxLabelClass(GenericIdAndName):
    id: str
    color: Optional[str]
    captionAllowed: bool
    captionRequired: bool
    """
    tba
    """
    questions: Optional[List[BBoxLabelClassQuestions]]


@dataclass
class BboxLabelSet(GenericIdAndName):
    classes: List[BBoxLabelClass]


@dataclass
class Page:
    pageIndex: int
    pageHeight: int
    pageWidth: int


@dataclass
class BBoxDatasaurSchemaData:
    kinds: List[str]
    pages: Optional[List[Page]]
    bboxLabelSets: Optional[List[BboxLabelSet]]
    bboxLabels: Optional[List[BBoxLabel]]
    document: GenericIdAndName
    project: Optional[GenericIdAndName]


@dataclass
class DatasaurSchema:
    data: BBoxDatasaurSchemaData
    version: str
