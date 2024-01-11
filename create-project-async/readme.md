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
  - The number of labelers assigned to each multi-pass files can be configured with the `multi_pass_labeler_count` argument
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

### Example use case

<details>
<summary>Expand here</summary>

- `multi_pass_labeler_count` arg is set to the default `2`
- Say there are 10 documents inside the `documents/` folder, divided into 2 multi-pass and 8 single-pass files.

  ```
  single-sample-1.txt
  single-sample-2.txt
  single-sample-3.txt
  single-sample-4.txt
  single-sample-5.txt
  single-sample-6.txt
  single-sample-7.txt
  single-sample-8.txt
  multi-sample-1.txt
  multi-sample-2.txt
  multi-sample-3.txt
  ```

- In the `create_project.json`, the assignments are the following:

  - 3 labelers (`teamMemberId 1, 2, 3`)
  - 2 reviewers (`teamMemberId 4, 5`)

  ```json
  {
    "operationName": "CreateProjectMutation",
    "variables": {
      "input": {
        ...
        "documentAssignments": [
          {
            "teamMemberId": "1",
            "documents": [
              ...
            ],
            "role": "LABELER"
          },
          {
            "teamMemberId": "2",
            "documents": [
              ...
            ],
            "role": "LABELER"
          },
          {
            "teamMemberId": "3",
            "documents": [
              ...
            ],
            "role": "LABELER"
          },
          {
            "teamMemberId": "4",
            "documents": [
              ...
            ],
            "role": "REVIEWER"
          },
          {
            "teamMemberId": "5",
            "documents": [
              ...
            ],
            "role": "REVIEWER"
          }
        ],
        ...
      }
    },
    "query": "..."
  }
  ```

The resulting assignment should be like this:

```md
# Labeler assignees

Single-pass files will be assigned to one labeler each

- single-sample-1.txt -> teamMemberId 1
- single-sample-2.txt -> teamMemberId 2
- single-sample-3.txt -> teamMemberId 3
- single-sample-4.txt -> teamMemberId 1
- single-sample-5.txt -> teamMemberId 2
- single-sample-6.txt -> teamMemberId 3
- single-sample-7.txt -> teamMemberId 1
- single-sample-8.txt -> teamMemberId 2

Multi-pass files will be assigned to two labelers of different combination

- multi-sample-1.txt -> teamMemberId 1, 2
- multi-sample-2.txt -> teamMemberId 1, 3
- multi-sample-3.txt -> teamMemberId 2, 3

# Reviewer assignees

Reviewers will be assigned to all the files
```

</details>

### Sample CLI command

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
