# Datasaur API Client Sample

## Pre-requisite

```
pip3 install -r requirements.txt
```

## API Documentation

API Documentation can be found [here](https://datasaurai.gitbook.io/datasaur/advanced/apis-docs).

## Export Project

```
python3 export.py https://app.datasaur.ai <client_id> <client_secret> <project_id> <filename> <export_format> <output_dir>
python3 export.py https://app.datasaur.ai <client_id> <client_secret> <project_id> datasaur conll_2003 ./output
```

## Create Doc Based Labeling by Using External Files

```
python3 create_project_doc_file_url.py https://app.datasaur.ai <client_id> <client_secret> <team_id> <document count>
```

## Create Doc Based Labeling by Uploading Files (Simulation Only)

```
python3 create_project_doc.py https://app.datasaur.ai <client_id> <client_secret> <team_id> <file_count>
```

## Create Row Based Labeling

```
python3 create_project_row.py https://app.datasaur.ai <client_id> <client_secret> <team_id> <path_to_file>
python3 create_project_row.py https://app.datasaur.ai <client_id> <client_secret> <team_id> ./sample-files/row-based/bookcover-multiplefiles
```

## Create Token Based Labeling

```
# single file
python3 create_project_token.py https://app.datasaur.ai <client_id> <client_secret> <team_id> <path_to_file>

# multiple files in a folder
python3 create_project_token_multiple_files.py https://app.datasaur.ai <client_id> <client_secret> <team_id> ./sample-files/token-based/multiple-files

# using remote URL (you need to specify the files in create_project_token_url.json)
python3 create_project_token_url.py https://app.datasaur.ai <client_id> <client_secret> <team_id>
```

## Get Projects

Get projects query returns a paginated response. The input variables for the pagination can be configured directly in `get_projects.json`.
Refer to https://api-docs.datasaur.ai/#definition-GetProjectsFilterInput for available filters.

```
python get_projects.py https://app.datasaur.ai <client_id> <client_secret>
```

## Update Project Tags

Tag names and project id can be specified from update_project_tags.json.

Two available methods: PUT and PATCH. PUT method will replace all of the project tags with the input, just like PUT method on REST API. PATCH method will only add new tags to a project. See the example below.

- Project A has Tag1.
- PUT ["Tag2"]: Project A will have only Tag2.
- PATCH ["Tag2"]: Project A will have Tag1 and Tag2.

```
python get_projects.py https://app.datasaur.ai <client_id> <client_secret> <team_id> <method>
python get_projects.py https://app.datasaur.ai <client_id> <client_secret> <team_id> PUT
```
