# API Client Sample

## Pre-requisite

```
# install dependencies
python -m pip install -r src/requirements.txt
```

## Create Project (v2)

This version uses the new [`createProject`](https://docs.datasaur.ai/#mutation-createProject) mutation over the existing [`launchTextProjectAsync`](https://docs.datasaur.ai/#mutation-launchTextProjectAsync). We are planning to deprecate the launchTextProjectAsync mutation in the future.

> For v1 version of the script, please navigate to the Releases / Tag page or checkout the `v1` branch.

In this new mutation, we no longer support uploading files directly to the GraphQL mutation, and instead you must upload the files ahead of time, either to Datasaur-owned storage bucket via a separate POST endpoint `/api/static/proxy/upload`, or to your own storage bucket. The script currently only supports the first method.

### With Local Files

Local files are located under `document/` folder.  
Every file inside the directory will be uploaded to Datasaur as part of the project creation process.

**Note**: If you want to use pairing files, such as inputfile.jpg with inputfile.txt, ensure that they share the same filename. These paired files are commonly used for OCR / Audio projects with transcription.

```
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID
```

## Get Job Status

```
python api_client.py get_job_status \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --job_id JOB_ID
```
