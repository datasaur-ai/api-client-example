# Bounding Boxes Formats: COCO 

This folder contains Python scripts for converting annotation results from the COCO format to Datasaur Schema format and vice versa. 

- [Formats](#formats)
  - [COCO](#coco)
  - [Datasaur Schema](#datasaur-schema)
- [Prerequisite](#prerequisite)
- [Usage](#usage)
  - [`coco_to_datasaur_schemas`](#coco_to_datasaur_schemas)
  - [`datasaur_schemas_to_coco`](#datasaur_schemas_to_coco)


## Formats

### COCO

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

### Datasaur Schema

[Datasaur Schema](https://docs.datasaur.ai/compatibility-and-updates/supported-formats#datasaur-schema-format) is a customized format Datasaur uses for both creating and exporting a Datasaur project. 


## Prerequisite

```
pip install -r requirements.txt
```

The script uses [`dacite.from_dict`](https://github.com/konradhalas/dacite) to transform the JSON object into a Python dataclass.

The script was developed using Python 3.10.13

## Usage

### `coco_to_datasaur_schemas`

This function transforms a dictionary representation of a COCO file into a list of `DatasaurSchema` dicts.

Parameters: 
- `coco_json` (Any): A dictionary representation of a COCO file.

Running `python src/coco_to_datasaur_schemas.py` should run the function against a sample `COCO.json` file. The function expect a `dict` representation of a COCO file and will return an array of `DatasaurSchema` also in a `dict` format. 

Note: The function will ignore the following fields as they are not used in Datasaur Schema: 
- `licenses`
- `info`
- `annotation.area`, `annotation.bbox`

### `datasaur_schemas_to_coco`

This function transforms a list of Datasaur Schema object, represented as a list of dictionaries, into a single COCO object.

Parameters:
- `schema_objects` (list[Any]): A list of dictionaries representing the result of `json.load`-ing the Datasaur Schema JSON.
- `licenses` (list[COCOLicense] | None, optional): A list of COCOLicense objects. Defaults to None.
- `info` (COCOInfo | None, optional): A COCOInfo object. Defaults to None.

Running `python src/datasaur_schemas_to_coco.py` will read the sample zipfile `samples/bbox-export.zip` and transform the JSON file under the `REVIEW` directory into a single `COCO` object, which will be written to `outdir/out-coco.json`. 

As `licenses` and `info` parameters are optional, when not provided it will use the following values: 

```json
{
  "licenses": [
    {
      "name": "dummy-datasaur-license", 
      "id": 0,
      "URL": ""
    }
  ],
  "info": {
    "description": "Exported from Datasaur",
    "url": "https://datasaur.ai",
    "version": "v0.1",
    "year": 2024,
    "contributor": "Datasaur",
    "date_created": "2024-04-23"
  }
}
```


Example usage:
```python
schemas = [...]
coco_obj = datasaur_schemas_to_coco(schemas)

# or provide your own `licenses` and `info`
coco_obj = datasaur_schemas_to_coco(
    schemas,
    licenses=[COCOLicense(name="dummy-license", id=0, URL="")],
    info=COCOInfo(
        contributor="contributor",
        date_created="2024-01-01",
        description="dataset-description",
        URL="http://example.com",
        version="v0.1",
        year=2024,
    ),
)
```
