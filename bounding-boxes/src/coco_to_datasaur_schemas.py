import json
import os
from argparse import ArgumentParser
from dataclasses import asdict
import logging
from math import floor
from typing import Any, List

from common.random_color import random_color
from common.logger import log as _log
from common.scrub import scrub
from formats.datasaur_schema import (
    DatasaurSchema,
    DSBBoxLabel,
    DSBBoxLabelClass,
    DSBboxLabelSet,
    DSBBoxProjectData,
    DSPage,
    DSPoint,
    DSShape,
    GenericIdAndName,
)


def log(message, level=logging.DEBUG, **kwargs):
    logger = logging.getLogger(
        __name__ if __name__ != "__main__" else "coco_to_datasaur_schemas"
    )
    return _log(message=message, logger=logger, level=level, **kwargs)


def coco_to_datasaur_schemas(coco_json: Any) -> List[dict]:
    """
    Raises:
        Exception: If the segmentation of an annotation does not have 8 elements.
    """

    # validate segmentation first
    for annot in coco_json["annotations"]:
        for segmentation in annot["segmentation"]:
            if len(segmentation) != 8:
                log(
                    "found faulty annotation",
                    level=logging.ERROR,
                    annotation=annot,
                )
                raise Exception(
                    f"expect segmentation to be a list-of-list of 8 elements, faulty annotation.id={annot.id}",
                )

    log(message="creating BBoxLabelSet from COCO categories", level=logging.DEBUG)
    bbox_label_set = DSBboxLabelSet(
        id=None,
        name="BBox Label Set",
        classes=bbox_label_classes_from_coco(coco_json["categories"]),
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

    log("converting COCO to Datasaur Schema")
    schemas = coco_to_datasaur_schemas(json_data)

    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)
    log("writing to file", directory=outdir)
    for schema in schemas:
        filename = schema["data"]["document"]["name"].split(".")[0] + ".json"

        with open(os.path.join(outdir, filename), "w") as f:
            json.dump(scrub(schema), f, indent=2)


def bbox_label_classes_from_coco(
    coco_categories: List[dict],
) -> List[DSBBoxLabelClass]:

    retval = []
    for category in coco_categories:
        retval.append(
            DSBBoxLabelClass(
                id=str(category["id"]),
                name=category["name"],
                # since these attributes are nowhere in COCO,
                # set it to the most flexible option, allow caption but don't require it
                captionAllowed=True,
                captionRequired=False,
                color=random_color(category["name"]),
                # TODO support once custom attributes are supported
                questions=None,
            )
        )

    return retval


def shape_from_coco_segmentation(segmentation: List[float]) -> DSShape:
    if len(segmentation) != 8:
        raise Exception("expect segmentation to be a list-of-list of 8 elements")

    points: List[DSPoint] = []

    for i in range(0, 8, 2):
        points.append(DSPoint(x=segmentation[i], y=segmentation[i + 1]))

    return DSShape(pageIndex=0, points=points)


def bbox_label_from_coco_annotation(
    annotation: dict, labelset: DSBboxLabelSet
) -> DSBBoxLabel:
    # TODO process once custom attribute is supported
    """
    text = caption
    occluded = 0?
    type = TEXT & HW
    """
    attributes = annotation["attributes"]

    stringified_id = str(annotation["category_id"])
    bbox_label_class = next(
        item for item in labelset.classes if item.id == stringified_id
    )

    bbox_shapes = [
        shape_from_coco_segmentation(segment) for segment in annotation["segmentation"]
    ]

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
        # TODO: support once custom attributes implemented
        answers=None,
    )


if __name__ == "__main__":
    main()
