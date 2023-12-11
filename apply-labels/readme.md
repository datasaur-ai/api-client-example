# Apply labels as labeler from file.

This folder focuses on workflows for row-labeling, where labelers' have applied labels externally and you need to import them to Datasaur for analytics purposes. 

## Table of contents

- [Table of contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
- [How it works](#how-it-works)

## Prerequisites

- A Datasaur workspace with OAuth credentials enabled. 
- Python 3 (3.10 recommended), with `pip` installed.

## Quickstart

1. `pip install -r requirements.txt` or `pip install -r dev-requirments.txt`. Dev requirements is really only needed if you want consistent formatting with `black`.
2. Setup a Datasaur workspace and generate admin OAuth credentials. Save the client id and secret in the `.env` file. We have provided an example `.env.example` you can copy. 
3. Create and invite the labeler accounts you will be applying labels as. For each one, generate OAuth credentials and save the client id and secret. This time, in the .env file, but in a `labelers.json` file. We have provided an example `labelers.json.example` you can refer to. We'll be using the [pyjson5](https://pypi.org/project/pyjson5/) library to parse this file, so you can use comments inside. 
4. Execute the script. It is configured to read the admin credentials from the `.env` file, and the labeler credentials from the `labelers.json` file.
```console
python apply_labels.py apply_row_answers --team_id TEAM_ID --project_id PROJECT_ID [--labelers_file labelers.json] [--verbose]
```

## How it works

The script uses Datasaur's GraphQL API to apply the labels / answers.  
For this specific sample, we are using the [`updateMultiRowAnswers`](https://api-docs.datasaur.ai/#mutation-updateMultiRowAnswers) mutation to apply row-answers to the project. 
The script expect the project to have been properly configured with the necessary questions, and that the answers provided in the files are valid.  
There are some checks and validations, such as assignment and column header checks, but it does not check row-data alignment. You would need to provide the same number of rows as the number of rows in the project.

Here's a step-by-step overview of what the script does, given a team_id and a project_id:
1. Read the config. If you provide no oauth credentials, it will look into the .env file. 
2. Fetch the project by team & project id, using admin credentials. 
3. Project-level validation. Here it will check that each labeler in the `labelers_file` is actually assigned to the project. 
4. Cabinet replication. Here, the script will simulate opening the project as each labeler for the first time. This will create a cabinet - essentially a copy of the project - for each labeler.
    - After replication is finished, it will fetch the project questions and column header information. This will be used to validate the row-answer file. 
    - The script will error-out here if there are no valid columns / data detected. 
    - Any columns present in the file, but not present as a question in the project will be skipped silently. Run the command with the --verbose flag to see a log entry.
5. Row-answers application. The script will then apply the answers to the project.  

