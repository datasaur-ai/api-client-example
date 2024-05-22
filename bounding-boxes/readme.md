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

The script was developed and tested using Python 3.10.13

## Usage

### `coco_to_datasaur_schemas`

This function transforms a dictionary representation of a COCO file into a list of `DatasaurSchema` dicts.

Parameters: 
- `coco_json`: A dictionary representation of a COCO file.
- `custom_labelset`: Optional. A dictionary representation of a Datasaur bounding box label set to provide additional information. Useful to set default value, custom color, or setting a specific attribute as `DROPDOWN` type. See [here](./samples/custom-label-set.json) for an example JSON file.

Running `python src/coco_to_datasaur_schemas.py` should run the function against a sample `COCO.json` file. The function expect a `dict` representation of a COCO file and will return an array of `DatasaurSchema` also in a `dict` format. 

Note: The function will ignore the following fields as they are not used in Datasaur Schema: 
- `licenses`
- `info`
- `annotation.area`, `annotation.bbox`

Example usage: 
- as a function
  ```python
  coco_json = json.load(file)
  datasaur_schemas = coco_to_datasaur_schemas(coco_json)
  ```
- as a script
  ```
  $ python src/coco_to_datasaur_schemas.py -h
  usage: coco_to_datasaur_schemas [-h] [--custom-labelset CUSTOM_LABELSET] [--outdir OUTDIR] [--log-level LOG_LEVEL] coco_filepath

  positional arguments:
    coco_filepath         Path to COCO JSON file

  options:
    -h, --help            show this help message and exit
    --custom-labelset CUSTOM_LABELSET
                          Path to custom labelset JSON file (useful for specifying DROPDOWN attributes)
    --outdir OUTDIR       Output directory for Datasaur schemas
    --log-level LOG_LEVEL

  $ python src/coco_to_datasaur_schemas.py samples/COCO.json
  ```

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
- as a function
  ```python
  schemas = [...]
  coco_obj = datasaur_schemas_to_coco(schemas)

  # or provide your own `licenses` and `info`
  coco_obj = datasaur_schemas_to_coco(
      schemas,
      licenses=[{"name": "dummy-license", "id": 0, "url": ""}],
      info={
          "contributor": "contributor",
          "date_created": "2024-01-01",
          "description": "dataset-description",
          "url": "http://example.com",
          "version": "v0.1",
          "year": 2024,
      },
  )
  ```
- as a script
  ```
  $ python src/datasaur_schemas_to_coco.py -h
  usage: datasaur_schemas_to_coco [-h] [--outfile OUTFILE] [--license-and-info-json LICENSE_AND_INFO_JSON] zip_filepath

  positional arguments:
    zip_filepath          Path to Datasaur export ZIP file

  options:
    -h, --help            show this help message and exit
    --outfile OUTFILE     Output directory for COCO JSON file
    --license-and-info-json LICENSE_AND_INFO_JSON
                          Path to JSON file containing licenses and info data
  
  $ python src/datasaur_schemas_to_coco.py samples/bbox-export.zip
  ```
