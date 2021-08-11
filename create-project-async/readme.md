# API Client Sample

## Pre-requisite

```
# install dependencies
python -m pip install -r src/requirements.txt
```

## Create Project

```
python datasaur_api.py create_project \
  --base_url=BASE_URL \
  --client_id=CLIENT_ID \
  --client_secret=CLIENT_SECRET \
  --team_id=TEAM_ID
```

## Get Job Status

```
python datasaur_api.py get_job_status \
  --base_url=BASE_URL \
  --client_id=CLIENT_ID \
  --client_secret=CLIENT_SECRET \
  --job_id=JOB_ID
```
