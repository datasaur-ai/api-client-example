# API Client Sample

## Pre-requisites

- python
- pip
- google application credentials, follow this https://cloud.google.com/storage/docs/reference/libraries#more_examples

## Setup

```
# install dependencies
python -m pip install -r src/requirements.txt
cp .env.example .env
# adjust .env with GOOGLE_APPLICATION_CREDENTIALS
```

## Create Project

```
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID
```

## Export Single Project

### Store the exported project locally

```
python api_client.py export_single_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --project_id projectId \
  --export_file_name datasaur \
  --export_format JSON_ADVANCED \
  --output_dir ./outputs
```

### Store the exported project in Google Cloud Storage

```
python api_client.py export_single_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --project_id projectId \
  --export_file_name datasaur \
  --export_format JSON_ADVANCED \
  --output_dir gs://bucket-name/folder
```

## Export Multiple Projects

### Store the exported projects locally

```
python api_client.py export_projects \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id teamId \
  --project_status  "[\"COMPLETE\", \"REVIEW_READY\", \"IN_REVIEW\"]" \
  --export_format JSON_ADVANCED \
  --output_dir ./outputs
```

### Store the exported projects in Google Cloud Storage

```
python api_client.py export_projects \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id teamId \
  --project_status  "[\"COMPLETE\", \"REVIEW_READY\", \"IN_REVIEW\"]" \
  --export_format JSON_ADVANCED \
  --output_dir gs://bucket-name/folder
```

## Get Job Status

```
python api_client.py get_job_status \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --job_id JOB_ID
```

## Troubleshooting

- In case you get "certificate verify failed error", check server certificate or run this command in terminal to ignore SSL verification `export VERIFY_SSL=0`
