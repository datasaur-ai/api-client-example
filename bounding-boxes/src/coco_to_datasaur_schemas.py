import json
import logging
import os
from argparse import ArgumentParser
from dataclasses import asdict
from math import floor
from typing import Any, List, Set

from common.defaults import defaults
from common.logger import log as _log
from common.random_color import random_color
from common.scrub import scrub
from formats.coco import validate_segmentation
from formats.datasaur_schema import (
    DatasaurSchema,
    DSBBoxLabel,
    DSBBoxLabelClass,
    DSBBoxLabelClassQuestions,
    DSBboxLabelSet,
    DSBBoxProjectData,
    DSPage,
    DSPoint,
    DSShape,
    GenericIdAndName,
    QuestionConfig,
)


def log(message, level=logging.DEBUG, **kwargs):
    logger = logging.getLogger(
        __name__ if __name__ != "__main__" else "coco_to_datasaur_schemas"
    )
    return _log(message=message, logger=logger, level=level, **kwargs)


def coco_to_datasaur_schemas(coco_json: Any, custom_labelset: Any | None) -> List[dict]:
    """
    Raises:
        Exception: If the segmentation of an annotation does not have 8 elements.
    """

    # validate segmentation first
    for annot in coco_json["annotations"]:
        for segmentation in annot["segmentation"]:
            validate_segmentation(segmentation=segmentation)

    log(message="creating BBoxLabelSet from COCO categories", level=logging.DEBUG)
    bbox_label_set = DSBboxLabelSet(
        id=None,
        name="BBox Label Set",
        classes=bbox_label_classes_from_coco(coco_json["categories"], custom_labelset),
    )
    images = coco_json["images"]

    retval: List[dict] = []
    for image in images:
        annotations_by_images = [
            annot
            for annot in coco_json["annotations"]
            if annot["image_id"] == image["id"]
        ]

        bbox_labels = [
            bbox_label_from_coco_annotation(annot, bbox_label_set)
            for annot in annotations_by_images
        ]

        schema = DatasaurSchema(
            version="1",
            data=DSBBoxProjectData(
                kinds=["BBOX_BASED"],
                bboxLabels=bbox_labels,
                bboxLabelSets=[bbox_label_set],
                document=GenericIdAndName(name=image["file_name"], id=None),
                project=None,
                pages=[
                    DSPage(
                        pageIndex=0,
                        pageHeight=floor(image["height"]),
                        pageWidth=floor(image["width"]),
                    )
                ],
            ),
        )

        retval.append(asdict(schema))

    return retval


def main() -> None:
    parser = ArgumentParser(prog="coco_to_datasaur_schemas")
    parser.add_argument("coco_filepath", type=str, help="Path to COCO JSON file")
    parser.add_argument(
        "--custom-labelset",
        type=str,
        help="Path to custom labelset JSON file (useful for specifying DROPDOWN attributes)",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        help="Output directory for Datasaur schemas",
        default="./outdir/",
    )
    parser.add_argument("--log-level", type=str, default="INFO")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format="%(message)s")

    coco_filepath = os.path.abspath(args.coco_filepath)
    log("reading COCO JSON file", filepath=coco_filepath)
    with open(coco_filepath) as f:
        json_data = json.load(f)

    custom_labelset = None
    if args.custom_labelset:
        custom_labelset_filepath = os.path.abspath(args.custom_labelset)
        with open(custom_labelset_filepath) as f:
            custom_labelset = json.load(f)

    log("converting COCO to Datasaur Schema")
    schemas = coco_to_datasaur_schemas(json_data, custom_labelset)

    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    log("writing to file", directory=outdir)
    for schema in schemas:
        filename = schema["data"]["document"]["name"].split(".")[0] + ".json"

        with open(os.path.join(outdir, filename), "w") as f:
            json.dump(scrub(schema), f, indent=2)


def bbox_label_classes_from_coco(
    coco_categories: List[dict],
    custom_labelset: Any | None,
) -> List[DSBBoxLabelClass]:
    custom_classes = custom_labelset["classes"] if custom_labelset else []

    retval = []
    for category in coco_categories:
        # check and use questions from custom class
        custom_class = next(
            (item for item in custom_classes if item["name"] == category["name"]), None
        )

        questions = [
            DSBBoxLabelClassQuestions(
                id=q.get("id", index),
                label=q.get("label", f"Question {index}"),
                config=QuestionConfig(
                    multiline=q.get("config", {}).get("multiline", False),
                    multiple=q.get("config", {}).get("multiple", False),
                    options=q.get("config", {}).get("options", []),
                    defaultValue=q.get("config", {}).get("defaultValue", None),
                ),
                required=q.get("required", False),
                type=q.get("type", "TEXT"),
            )
            for index, q in enumerate(defaults(custom_class, "questions", []))
        ]

        retval.append(
            DSBBoxLabelClass(
                id=str(category["id"]),
                name=category["name"],
                captionAllowed=defaults(custom_class, "captionAllowed", True),
                captionRequired=defaults(custom_class, "captionRequired", False),
                color=defaults(custom_class, "color", random_color(category["name"])),
                questions=questions,
            )
        )

    return retval


def shape_from_coco_segmentation(segmentation: List[float]) -> DSShape:
    validate_segmentation(segmentation=segmentation)
    points: List[DSPoint] = []

    for i in range(0, 8, 2):
        points.append(DSPoint(x=segmentation[i], y=segmentation[i + 1]))

    return DSShape(pageIndex=0, points=points)


def bbox_label_from_coco_annotation(
    annotation: dict, labelset: DSBboxLabelSet
) -> DSBBoxLabel:
    attributes = annotation["attributes"]

    stringified_id = str(annotation["category_id"])
    bbox_label_class = next(
        item for item in labelset.classes if item.id == stringified_id
    )

    bbox_shapes = [
        shape_from_coco_segmentation(segment) for segment in annotation["segmentation"]
    ]

    # check if attributes have any other key
    # if found, add to labelset.classes
    answers = None
    if attributes.keys() - {"text"}:
        answers = {}
        keys: Set = attributes.keys() - {"text"}

        for key in keys:
            questions = bbox_label_class.questions
            if questions is None:
                questions = []

            if key not in [q.label for q in questions]:
                questions.append(
                    DSBBoxLabelClassQuestions(
                        id=len(questions),
                        label=key,
                        required=False,
                        type="TEXT",
                        config=QuestionConfig(
                            multiline=False,
                            multiple=False,
                            options=None,
                            defaultValue=None,
                        ),
                    )
                )

            question_id = next(q.id for q in questions if q.label == key)
            answers[str(question_id)] = str(attributes[key])

            bbox_label_class.questions = questions

    return DSBBoxLabel(
        id=str(annotation["id"]),
        caption=str(attributes.get("text", "")),
        bboxLabelClassId=bbox_label_class.id,
        bboxLabelClassName=bbox_label_class.name,
        shapes=bbox_shapes,
        labeledBy=None,
        acceptedByUserId=None,
        labeledByUserId=None,
        rejectedByUserId=None,
        status=None,
        answers=answers,
    )


if __name__ == "__main__":
    main()
