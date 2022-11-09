# API Client Sample

## Pre-requisite

```
# install dependencies
python -m pip install -r src/requirements.txt
```

## Create Project

### With Local Files

Local files are located under `document/` folder.  
Every file inside the directory will be uploaded to Datasaur as part of the project creation process.

```
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID
```

### With Remote Files

```
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID \
  --documents_path PATH_TO_DOCUMENTS_JSON
```

Provide a JSON file with `--documents_path`.  
Example file available under `documents-example.json`.

```json
[
  {
    "url": "<publicly accessible link to the file>",
    "fileName": "<a unique filename>"
  }
]
```

If your team already have [External Object Storage](https://datasaurai.gitbook.io/datasaur/basics/workforce-management/external-object-storage) integration configured, the list of documents can be simplified. You can skip generating the URLs to each file, and just provide the path to the file instead.

Example file available under `eos-documents-example.json`

```json
[
  {
    "externalObjectStorageFileKey": "path/to/file.txt",
    "fileName": "<a unique filename>"
  }
]
```

The value of `fileName` does not have to match the actual file's name.

## Get Job Status

```
python api_client.py get_job_status \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --job_id JOB_ID
```
