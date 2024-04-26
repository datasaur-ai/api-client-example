import json
import os
import zipfile
from dataclasses import asdict
from typing import Any, Dict
from shutil import rmtree

from formats.coco import (
    COCO,
    COCOCategory,
    COCOImage,
    COCOLicense,
    COCOAnnotation,
    COCOInfo,
)
from formats.datasaur_schema import DatasaurSchema, DSShape
from dacite import from_dict


def datasaur_schemas_to_coco(
    schema_objects: list[Any],
    licenses: list[COCOLicense] | None = None,
    info: COCOInfo | None = None,
) -> dict:
    """
    schema_objects: a list of dict, the result of json.load-ing the Datasaur Schema json
    """
    if licenses is None:
        licenses = [COCOLicense(name="dummy-datasaur-license", id=0, URL="")]

    if info is None:
        info = COCOInfo(
            contributor="datasaur.ai",
            date_created="2024-04-23",
            description="Description of the dataset",
            URL="",
            version="v0.1",
            year=2024,
        )

    schemas = [from_dict(data=s, data_class=DatasaurSchema) for s in schema_objects]

    # assuming all DatasaurSchema are from the same project,
    # there will be the same bboxLabelSet
    categories: list[COCOCategory] = coco_categories_from_datasaur_schema(schemas[0])

    # images from datasaur schemas -- name, dimension info
    images: list[COCOImage] = [
        coco_images_from_datasaur_schema(id, schema)
        for id, schema in enumerate(schemas)
    ]

    # annotations from bboxLabels
    annotations: list[COCOAnnotation] = coco_annots_from_datasaur_schemas(
        schemas, categories
    )

    return asdict(
        COCO(
            info=info,
            licenses=licenses,
            categories=categories,
            images=images,
            annotations=annotations,
        )
    )


def main() -> None:
    export_zip = "./samples/bbox-export.zip"
    temp_destination = "./temp/"
    os.makedirs(temp_destination, exist_ok=True)
    extracted_files: list[str] = unzip_export_result(
        export_zip=export_zip, dest=temp_destination
    )

    schemas = [load_datasaur_schema_file(f) for f in extracted_files]
    coco = datasaur_schemas_to_coco(schemas)

    outdir = "./outdir/"
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "out-coco.json"), "w") as wf:
        json.dump(coco, wf, indent=2)

    # clean-up
    rmtree(temp_destination)


def coco_annots_from_datasaur_schemas(
    schemas: list[DatasaurSchema], categories: list[COCOCategory]
) -> list[COCOAnnotation]:

    name_to_id: Dict[str, int] = {x.name: x.id for x in categories}
    annots: list[COCOAnnotation] = []
    for image_id, schema in enumerate(schemas):
        annot_id = 1
        if schema.data.bboxLabels is None:
            continue

        for bbox_label in schema.data.bboxLabels:
            annots.append(
                COCOAnnotation(
                    id=annot_id,
                    image_id=image_id,
                    category_id=name_to_id[bbox_label.bboxLabelClassName],
                    segmentation=shapes_to_segmentation(bbox_label.shapes),
                    bbox=shapes_to_bbox(bbox_label.shapes),
                    attributes={},
                    area=0,
                    iscrowd=0,
                )
            )

    return annots


def coco_categories_from_datasaur_schema(schema: DatasaurSchema) -> list[COCOCategory]:
    if schema.data.bboxLabelSets is None or len(schema.data.bboxLabelSets) < 1:
        return []

    retval: list[COCOCategory] = []

    # Currently, there can only be 1 bboxLabelSets
    bbox_label_set = schema.data.bboxLabelSets[0]
    for i, label_class in enumerate(bbox_label_set.classes, 1):
        retval.append(COCOCategory(id=i, name=label_class.name, supercategory=""))

    return retval


def coco_images_from_datasaur_schema(id: int, schema: DatasaurSchema) -> COCOImage:
    width, height = 0, 0
    if schema.data.pages is not None and len(schema.data.pages) >= 1:
        width = schema.data.pages[0].pageWidth
        height = schema.data.pages[0].pageHeight

    return COCOImage(
        id=id,
        file_name=schema.data.document.name,
        width=width,
        height=height,
        license=0,
        flickr_url="",
        coco_url="",
    )


def shapes_to_bbox(shapes: list[DSShape]) -> list[float]:
    x_coords = [point.x for shape in shapes for point in shape.points]
    y_coords = [point.y for shape in shapes for point in shape.points]

    x_min = min(*x_coords)
    x_max = max(*x_coords)
    y_min, y_max = min(*y_coords), max(*y_coords)

    return [min(*x_coords), min(*y_coords), x_max - x_min, y_max - y_min]


def shapes_to_segmentation(shapes: list[DSShape]) -> list[list[float]]:
    retval: list[list[float]] = []
    for shape in shapes:
        segmentation: list[float] = [
            dot for point in shape.points for dot in [point.x, point.y]
        ]
        retval.append(segmentation)
    return retval


def unzip_export_result(export_zip: str, dest: str) -> list[str]:
    retval: list[str] = []
    with zipfile.ZipFile(export_zip, "r") as zf:
        project_dir: str | None = None
        for zippath in zipfile.Path(zf).iterdir():
            if zippath.is_dir():
                project_dir = zippath.name
                break
        if not (project_dir):
            raise Exception("no project dir found")

        for zip_content in zf.infolist():
            if not zip_content.filename.startswith(os.path.join(project_dir, "REVIEW")):
                continue

            if zip_content.is_dir():
                zf.extract(zip_content.filename, dest)
                continue
            retval.append(zf.extract(zip_content, dest))

    return retval


def load_datasaur_schema_file(filepath: str):
    with open(filepath) as f:
        data = json.load(f)

    return data


if __name__ == "__main__":
    main()
