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

Local files are located under `documents/` folder.
Every file inside the directory will be uploaded to Datasaur as part of the project creation process.

```bash
python api_client.py create_project \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID
```

## Create Project with Portioned Assignments

This function allows you to create a project with portioned labeler assignments.

The portioning is determined by prefixes in the file names.

- Single-pass
  - These files are only assigned to 1 labeler
  - The name of single-pass files should be prefixed by `single-`
    - The expected prefix can be overridden by providing the `single_pass_prefix` argument
- Multi-pass
  - These files are assigned to several labelers
  - The number of labelers assigned to multi-pass files can be configured with the `multi_pass_labeler_count` argument
  - The name of single-pass files should be prefixed by `multi-`
    - The expected prefix can be overridden by providing the `multi_pass_prefix` argument

The assignee's role determines how the files will be distributed and accessed

- Reviewer
  - Reviewer will be assigned and have access to all files
- Labeler
  - The files will be distributed and accessible to labelers accordingly, depending on if it's single-pass or multi-pass
- Reviewer & Labeler
  - The files will be distribtued the same way like Labeler assignees
  - When opening the project in labeler mode, the assignee will only have access to the assigned files
  - When opening the project in reviewer mode, the assignee will have access to every files

```bash
python api_client.py create_project_portioned_assignment \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --team_id TEAM_ID \
  --single_pass_prefix "single-" \
  --multi_pass_prefix "multi-" \
  --multi_pass_labeler_count 2
```

## Get Job Status

```bash
python api_client.py get_job_status \
  --base_url BASE_URL \
  --client_id CLIENT_ID \
  --client_secret CLIENT_SECRET \
  --job_id JOB_ID
```
