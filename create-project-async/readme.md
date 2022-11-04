# API Client Sample

## Pre-requisite

```
# install dependencies
python -m pip install -r src/requirements.txt
```

## Create Project

### With local files, 
Documents are located under `document/` folder

```
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID
```

### With List of URLs

Provide a JSON file with `documents_path`
Example file available under `documents-example.json`

```
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID
  --documents_path PATH_TO_DOCUMENTS_JSON
```

## Get Job Status

```
python api_client.py get_job_status \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --job_id JOB_ID
```
