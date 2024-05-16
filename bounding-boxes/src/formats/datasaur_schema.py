from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class GenericIdAndName:
    id: Optional[str]
    name: str


@dataclass
class DSPoint:
    x: float
    y: float


@dataclass
class DSShape:
    pageIndex: int
    points: List[DSPoint]


@dataclass
class DSBBoxLabel:
    id: str
    bboxLabelClassId: str
    bboxLabelClassName: str
    caption: Optional[str]
    shapes: List[DSShape]
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
class DropdownOption:
    id: str
    label: str


@dataclass
class QuestionConfig:
    multiline: bool
    multiple: bool
    options: List[DropdownOption]


@dataclass
class DSBBoxLabelClassQuestions:
    id: int
    label: str
    required: bool
    type: str
    config: QuestionConfig
    pass


@dataclass
class DSBBoxLabelClass(GenericIdAndName):
    id: str
    color: Optional[str]
    captionAllowed: bool
    captionRequired: bool
    """
    tba
    """
    questions: Optional[List[DSBBoxLabelClassQuestions]]


@dataclass
class DSBboxLabelSet(GenericIdAndName):
    classes: List[DSBBoxLabelClass]


@dataclass
class DSPage:
    pageIndex: int
    pageHeight: int
    pageWidth: int


@dataclass
class DSBBoxProjectData:
    kinds: List[str]
    pages: Optional[List[DSPage]]
    bboxLabelSets: Optional[List[DSBboxLabelSet]]
    bboxLabels: Optional[List[DSBBoxLabel]]
    document: GenericIdAndName
    project: Optional[GenericIdAndName]


@dataclass
class DatasaurSchema:
    data: DSBBoxProjectData
    version: str
