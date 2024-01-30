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
3. Setup the labeler accounts. There are two possible approaches: 
    1. Using new, dedicated 'robot' accounts only for this workflow. This is suitable if you are doing a one-time migration from another platform, aggregating labels from multiple sources, or if you are reviewing inference results from models.
       - You'd setup the `labelers.json` file with the OAuth credentials of each labeler.
       - For your convenience, you could set-up multiple labeler accounts just for this workflow using the script from [`user_management`](../user-management/readme.md) folder.  
       **We recommend creating new accounts instead of using existing accounts as you'd be storing and using those OAuth credentials to apply the labels.**
       - Please check the convert_to_json commands for a quick way to convert the CSV result to a JSON file.  
    2. Using existing accounts and generating OAuth Credentials on-the-fly. This is only available for self-hosted installation schemes. In this mode you don't need to provide labelers' credentials, just the `email` and `documents`. The credentials will be generated at the beginning of the script.  
        - As this requires a super-admin enabled account, it is only available for self-hosted installation schemes.
        - The script must be run with a super-admin enabled account, as it will attempt to regenerate the credentials using that account's OAuth credentials.
        - Consequently, if this admin account is also to be assigned to the project, you need to provide the `client_id` and `client_secret` in the `labelers.json` file so that it does not get replaced. 
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

Replace `<team-id>`, and `<project-id>` with your actual values. These values are available in the URL. You can refer to [this page](https://docs.datasaur.ai/api/get-data#values-from-app-path) for more details.  
`[path to json file]` and `[path to csv file]` are optional. Please refer to the parameters section below for more details.


#### Parameters

Command parameters: 
- `team_id` (str): The ID of the team.
- `project_id` (str): The ID of the project. The project's ID is also visible in the URL. 
- `labelers_file` (str, optional): Path to the JSON file that contains the labelers. Defaults to "labelers.json".  
      ***SuperAdmin mode***: If you are running the script from a super-admin enabled-account, you can skip providing client_id and client_secret for the labelers. The script will attempt to fetch the labelers' credential from the user management API.
- `users_csv` (str, optional): Path to a CSV file containing users info. See [user_management readme](../user-management/readme.md) for structure. If omitted, script will only read from labelers_file.
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
    - Check for `labelers_file` and `users_csv`.  
    If you provide a `users_csv`, the script will then attempt to populate the `labelers_file` with the users' credential from the CSV file. The script will then re-write the `labelers_file` with the credentials included. 
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
- `labelers_file` (str): Path to a JSON file we'll write.  
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