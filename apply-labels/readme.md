# Apply labels as labeler from file.

This folder focuses on workflows for row-labeling, where labelers' have applied labels externally and you want to import them to Datasaur and view the [IAA](https://docs.datasaur.ai/workspace-management/analytics/inter-annotator-agreement).

## Table of contents

- [Table of contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [Commands](#commands)
  - [apply\_row\_answers](#apply_row_answers)
    - [Usage](#usage)
    - [Parameters](#parameters)
    - [How it Works](#how-it-works)
    - [Limitations](#limitations)
  - [convert\_to\_json](#convert_to_json)
    - [Usage](#usage-1)
  - [check\_teams](#check_teams)
    - [Usage](#usage-2)

## Prerequisites

- A Datasaur account, able to create / have access to a workspace and able to generate OAuth credentials. 
    - Please refer to the root [readme](../readme.md#prerequisites) to generate your OAuth Credentials 
- Python 3 (3.10 recommended), with `pip` installed.
    - Run `pip install -r requirements.txt` or `pip install -r dev-requirments.txt`. Dev requirements is really only needed if you are modifying the code and want consistent formatting with `black`.

## Quickstart

1. Ensure you have your Datasaur account ready, and that it can create / have access to a team workspace. **This will be your admin account.**
2. Setup a Datasaur workspace and generate OAuth credentials from the admin account. For convenience, you can store the client id and secret as environment variables. The script will look for a `.env` file. We have provided a `.env.example` you can refer to. 
3. Create and invite the labeler accounts you will be applying labels as. For each one, generate OAuth credentials and save the client id and secret. This time, not in the `.env` file, but in a `labelers.json` file. We have provided an example `labelers.json.example` you can refer to. We'll be using the [pyjson5](https://pypi.org/project/pyjson5/) library to parse this file, so you can use comments inside.
    - For your convenience, you could set-up multiple labeler accounts just for this workflow using the script from [`user_management`](../user-management/readme.md) folder.  
    **We recommend creating new accounts instead of using existing accounts as you'd be storing and using those OAuth credentials to apply the labels.**
    - Please check the convert_to_json commands for a quick way to convert the CSV result to a JSON file.
4. Execute the script. It is configured to read the admin credentials from the `.env` file, and the labeler credentials from the specified json file.  
    Please refer to the `apply_row_answers` section below for detailed explanation. 
    ```console
    python apply_labels.py apply_row_answers --team_id TEAM_ID --project_id PROJECT_ID [--labelers_file labelers.json] [--verbose]
    ```

## Commands

### apply_row_answers

This function queries a project's assignment and cabinet detail, then replicates the cabinet to each assigned member (if it doesn't exist), and opens and applies row answers to each document in the cabinet for each assignee.

#### Usage

```console
python apply_labels.py apply_row_answers --team_id <team-id> --project_id <project-id> --labelers_file [path to json file] --users_csv [path to csv file]
```

Replace `<team-id>`, `<project-id>`, and `<path to json file>` with your actual values.

#### Parameters

Command parameters: 
- `team_id` (str): The ID of the team.
- `project_id` (str): The ID of the project.
- `labelers_file` (str, optional): The path to the JSON file that contains the labelers. Defaults to "labelers.json".
- `users_csv` (str, optional): Path to a CSV file containing users info. See user_management readme for structure. If omitted, script will only read from labelers_file.
- `verbose` (bool, optional): Whether to output verbose messages. Defaults to False.


OAuth credentials - You can set these as environment variables, in `.env` file, or pass them as command line arguments.
- `base_url` (str | None, optional): The base URL. Defaults to None. Env: `BASE_URL`
- `client_id`(str | None, optional): Admin's client ID. Defaults to None. Env: `CLIENT_ID`
- `client_secret` (str | None, optional): Admin's client secret. Defaults to None. Env: `CLIENT_SECRET`


#### How it Works

The script uses Datasaur's GraphQL API to apply the answers.  
It is using the [`updateMultiRowAnswers`](https://api-docs.datasaur.ai/#mutation-updateMultiRowAnswers) mutation to apply row-answers to the project. 
The script expect the project to have been properly configured with the necessary questions, and that the answers provided in the files are valid.  
There are some checks and validations, such as assignment and column header checks, but it does not check row-data alignment or answers. You would need to provide the same number of rows as the number of rows in the project.

Here's a step-by-step overview of what the script does, given a team_id and a project_id:
1. Read the config. If you provide no OAuth credentials, it will read from the `.env` file. 
2. Fetch the project by team & project id, using admin's OAuth credentials. 
3. Project-level validation. Here it will check that each labeler in the `labelers_file` is actually assigned to the project. 
4. Cabinet replication. Here, the script will simulate opening the project as each labeler for the first time. This will create a cabinet - essentially a copy of the project - for each labeler.
    - After replication is finished, it will fetch the project questions and column header information. This will be used to validate the row-answer file. 
    - The script will error-out here if there are no valid columns / data detected. 
    - Any columns present in the file, but not present as a question in the project will be skipped silently. Run the command with the `--verbose` flag to see a log entry.
5. Applying row-answers. The script will then apply the answers to the project.
    Answer application is done in batches of 100 rows at a time. This can be configured via the `.env` file as well.

#### Limitations

There are a couple of limitations to this script:
- It relies on files's name to associate the documents in Datasaur and the row-answer file here. As such, projects created with [our split file feature](https://docs.datasaur.ai/nlp-projects/creating-a-project/split-files) will not work, as the splitted file will have the same name. A workaround for working with large files would be to split them manually before creating the projects in Datasaur. 
- Minimal script-side validation. The script assumes that the row-answer file and the associated document contains the same number of rows. Answer values provided in the file are also passed as graphql input without validation.

### convert_to_json

#### Usage

```console
python apply_labels.py convert_to_json --users_csv <filepath> --labelers_file <filepath>
```

- `users_csv` (str): The path to the CSV file containing the users' information. This should be the output you get after running the command from the [`user_management`](../user-management/readme.md) folder.
- labelers_file (str): Path to a JSON file we'll write.  
    If the file exists, the script will populate the client_id & client_secret of the users that don't have them yet, and add missing users to the JSON file with empty documents assignment.  
    If it doesn't exist, the script will create the file and populate it with the users' information.

### check_teams

#### Usage

```console
python apply_labels.py check_teams
```

This function will attempt to authenticate with the Datasaur API using the credentials provided in the `.env` file. It will then fetch all the teams the admin has access to, and prints out the detail.

You can also check a labeler's credential by passing them in as command line arguments:
```console
python apply_labels.py check_teams --client_id <client-id> --client_secret <client-secret>
```