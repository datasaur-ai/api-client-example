# Datasaur API Client Sample

This repository focuses on examples in Python and only covers common use cases, hence not giving all query and mutation examples. Hopefully, these illustrations will be enough to be used as a reference for other queries and mutations.

## Prerequisites

1. `pip3` CLI installed
2. Clone this repository and go to the root folder.
3. Run `pip3 install -r  requirements.txt`.
4. [Genereate OAuth credentials](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs/oauth-2.0).

## API Documentation

- Start the API explanation from our [GitBook](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs).
- For the API docs detailing the GraphQL can be accessed [here](https://api-docs.datasaur.ai).

## Use Cases

- These variables will be the same for multiple use cases below.
  - `api_url`: depends on the server that you request, e.g. https://app.datasaur.ai. This one should be adjusted if you're on a self hosted version.
  - `client_id` and `client_secret`: generated from OAuth credentials, see [here](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs/oauth-2.0).

### Create Project

- The detailed explanation can be accessed [here](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs/create-new-project).
- Note that the process is asynchronous.
- This is an HTTP POST multipart request because it needs to handle a list of files that will be used when creating the project.
- Reference: `/create-project-async` and follow the README.

### Export Project

- The detailed explanation can be accessed [here](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs/export-project).
- Syntax: `python3 export.py <api_url> <client_id> <client_secret> <project_id> <filename> <export_format> <output_dir>`
  - `project_id`: project resource ID that can be accessed from the URL, e.g. `YOfkM6jKHzN` will be the ID if the project URL is https://app.datasaur.ai/teams/1/projects/YOfkM6jKHzN/review/ac35a379-2367-4d25-81d5-cf1184832b30.
  - `filename`: any alphanumeric string that will be used as the export result name (without the extension).
  - `export_format`: the list of value options could be seen on the GitBook above.
  - `output_dir`: prefix that will be added to specify the export result path.

### Get Projects

- The detailed explanation can be accessed [here](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs/get-list-of-projects).
- This query returns a paginated response.
- The input variables for the pagination can be configured directly on `get_projects.json`.
- Syntax: `python3 get_projects.py <api_url> <client_id> <client_secret>`

### Update Project Tags

- Tag names and project ID can be specified from `update_project_tags.json`.
- Two available methods: PUT and PATCH.
  - PUT method will replace all of the project tags with the input, just like PUT method on REST API.
  - PATCH method will only add new tags to a project, just like PATCH method on REST API.
- For example, Project A has Tag1.
  - PUT ["Tag2"]: Project A will only have Tag2.
  - PATCH ["Tag2"]: Project will have both Tag1 and Tag2.
- Syntax: `python update_project_tags.py <server_url> <client_id> <client_secret> <team_id> <method>`
