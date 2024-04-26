import json
import os
from dataclasses import asdict
from math import floor
from typing import Any, List

from formats.coco import COCO, COCOAnnotation
from formats.datasaur_schema import (
    DSBBoxProjectData,
    DSBBoxLabel,
    DSBBoxLabelClass,
    DSBboxLabelSet,
    DatasaurSchema,
    GenericIdAndName,
    DSPage,
    DSPoint,
    DSShape,
)
from common.scrub import scrub
from dacite import from_dict


def coco_to_datasaur_schemas(coco_json: Any) -> List[dict]:
    """
    One COCO JSON contains many images, hence the return value of this function needs to be a list of objects.

    Since the return value is a list of Python dataclass object, we need to use dataclasses.asdict before json.dump-ing it.

    See the main() function for an example usage.
    """
    # convert JSON dict to COCO representation
    coco_object = from_dict(data=coco_json, data_class=COCO)

    # validate segmentation first
    for annot in coco_object.annotations:
        for segmentation in annot.segmentation:
            if len(segmentation) != 8:
                raise Exception(
                    f"expect segmentation to be a list-of-list of 8 elements, faulty annotation.id={annot.id}",
                )

    bbox_label_set = DSBboxLabelSet(
        id=None,
        name="BBox Label Set",
        classes=bbox_label_classes_from_coco(coco_object),
    )
    images = coco_object.images

    retval: List[dict] = []
    for image in images:
        annotations_by_images = [
            annot for annot in coco_object.annotations if annot.image_id == image.id
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
                document=GenericIdAndName(name=image.file_name, id=None),
                project=None,
                pages=[
                    DSPage(
                        pageIndex=0,
                        pageHeight=floor(image.height),
                        pageWidth=floor(image.width),
                    )
                ],
            ),
        )

        retval.append(asdict(schema))

    return retval


def main() -> None:
    sample_coco = "./samples/COCO.json"
    with open(sample_coco) as f:
        json_data = json.load(f)

    schemas = coco_to_datasaur_schemas(json_data)

    outdir = "./outdir/"
    os.makedirs(outdir, exist_ok=True)
    for schema in schemas:
        filename = schema["data"]["document"]["name"].split(".")[0] + ".json"

        with open(os.path.join(outdir, filename), "w") as f:
            json.dump(scrub(schema), f, indent=2)


def bbox_label_classes_from_coco(
    coco_object: COCO,
) -> List[DSBBoxLabelClass]:
    categories = coco_object.categories

    retval = []
    for category in categories:
        retval.append(
            DSBBoxLabelClass(
                id=str(category.id),
                name=category.name,
                # since these attributes are nowhere in COCO,
                # set it to the most flexible option, allow caption but don't require it
                captionAllowed=True,
                captionRequired=False,
                color=None,
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
    annotation: COCOAnnotation, labelset: DSBboxLabelSet
) -> DSBBoxLabel:
    # TODO process once custom attribute is supported
    """
    text = caption
    occluded = 0?
    type = TEXT & HW
    """
    attributes = annotation.attributes

    stringified_id = str(annotation.category_id)
    bbox_label_class = next(
        item for item in labelset.classes if item.id == stringified_id
    )

    bbox_shapes = [
        shape_from_coco_segmentation(segment) for segment in annotation.segmentation
    ]

    return DSBBoxLabel(
        id=str(annotation.id),
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
