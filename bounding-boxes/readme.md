# Bounding Boxes Formats: COCO 

This folder contains python scripts you can use to convert annotation results in COCO into a natively accepted format in Datasaur, namely Datasaur Schema. 

There will be two scripts, one for transforming into Datasaur Schema, while the other will be transforming from Datasaur Schema.

## COCO

[COCO (Common Objects in Context)](https://cocodataset.org/#home) has formats for several annotation tasks. 
The script here will only support cases where the `segmentation` mask are in a quadrilateral shape. 
In other words, it will only work for cases where there are 8 values per list in the `segmentation` key. 

```json
{
  "annotations": [
    {
      "segmentation": [["x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4", "x5", "y5", "x6", "y6", "x7", "y7", "x8", "y8"]]
    }
  ]
}
```

## Datasaur Schema

[Datasaur Schema](https://docs.datasaur.ai/compatibility-and-updates/supported-formats#datasaur-schema-format) is a customized format Datasaur uses for both creating and exporting a Datasaur project. 


## Prerequisite

```
pip install -r requirements.txt
```

The script uses [`dacite.from_dict`](https://github.com/konradhalas/dacite) to transform the JSON object into a Python dataclass

## Usage

### `coco_to_datasaur_schemas`

Running `python src/coco_to_datasaur_schemas.py` should run the function against a sample `COCO.json` file. The function expect a `dict` representation of a COCO file and will return an array of [`DatasaurSchema`](src/common/datasaur_schema.py) object. 

The function will ignore the following fields as they are not used in Datasaur Schema: 
- `licenses`
- `info`
- `annotation.area`, `annotation.bbox`

### `datasaur_schemas_to_coco`

The function expects a list of `DatasaurSchema` represented as `dict` and will return a single `COCO` object as its output. 

Running `python src/datasaur_schemas_to_coco.py` will read the sample zipfile `samples/bbox-export.zip` and transform the JSON file under the `REVIEW` directory into a single `COCO` object, which will be written to `outdir/out-coco.json`

You can provide your own `licenses` and `info` values as a second parameter to the function. 