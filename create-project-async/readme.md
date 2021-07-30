# Datasaur API Client Sample

## API Documentation
API Documentation can be found [here](https://datasaurai.gitbook.io/advanced/apis-docs).

## Pre-requisite
```
# install dependencies
pip install -r src/requirements.txt

# create .env file and fill it with appropriate values
cp env.example .env
```

## Create Project
```
python datasaur_api.py create_project \
  --base_url=BASE_URL \
  --client_id=CLIENT_ID \
  --client_secret=CLIENT_SECRET \
  --team_id=team_id
```

## Get Job Status
```
python datasaur_api.py get_job_status \
  --base_url=BASE_URL \
  --client_id=CLIENT_ID \
  --client_secret=CLIENT_SECRET \
  --job_id=JOB_ID
```
