# User Management API Client Sample

This directory contains scripts for user management tasks. These scripts require helper functions from the `toolbox` directory.

## Prerequisites

Before using the User Management API Client Sample, ensure the following prerequisites are met:

1. **Install Requirements:**
    - Refer to the [api-client-example README](../readme.md#prerequisites) for instructions on installing the necessary Python packages and dependencies.

2. **Get Required Variables:**
    - Obtain the following variables from your self-hosted environment or API provider:
        - `base_url`: The base URL of the User Management API endpoint.
        - `client_id`: The client ID for authentication.
        - `client_secret`: The client secret for authentication.

    Make sure to follow the instructions provided in the [api-client-example README](../readme.md#use-cases) to obtain and configure these variables.

## Usage Limitations

- This script is specifically designed for self-hosted environments.
- Superadmin privileges are required to execute this script. Please refer to your installation documents or contact Datasaur support for specific steps on how-to set the privileges to your account.

## Usage

### Create Bulk Users

This script is designed to create users in bulk by reading data from a CSV file and making API requests to a specified endpoint. It is particularly useful for scenarios where you need to onboard multiple users efficiently.

```bash
python create_users.py create_users \
    --base_url <BASE_URL> \
    --client_id <CLIENT_ID> \
    --client_secret <CLIENT_SECRET> \
    --input_file_path <INPUT_FILE_PATH> \
    --output_file_path <OUTPUT_FILE_PATH> \
    --email_verified <EMAIL_VERIFIED>
```

**Options**

- `base_url` **(required)**: The base URL of the API endpoint.
- `client_id` **(required)**: The client ID for authentication.
- `client_secret` **(required)**: The client secret for authentication.
- `input_file_path` **(required)**: Path to the CSV file containing user data. Default is "./sample-files/create_users_input.csv".
- `output_file_path` **(required)**: Path to the CSV file where the output data will be written. Default is "./output-files/create_users_output.csv".
- `email_verified` **(optional)**: Flag indicating whether user emails are verified. Default is 0.

#### Input File Format

The CSV file should contain the following data, in order, separated by commas:

1. **User's Email:** The email address of the user.
2. **User's Name:** The name of the user.
3. **User's Password:** The password for the user.

Example CSV file content (located at [`sample-files/create_users_input.csv`](sample-files/create_users_input.csv)):

```csv
user1@email.com,UserName1,UserPa$$w0rd1
user2@email.com,UserName2,UserPa$$w0rd2
...
```

#### Output File Format

The output file format is same with the input file format, but it have additional datas:
1. **User's ID:** The ID of the created user.

Example CSV file content (located at [`sample-files/create_users_output.csv`](sample-files/create_users_output.csv)):

```csv
1,user1@email.com,UserName1,UserPa$$w0rd1
2,user2@email.com,UserName2,UserPa$$w0rd2
...
```

### Accept Team Invitations

This script facilitates the acceptance of users to teams by sending API requests to the specified endpoint. The script reads data from a CSV file, allowing you to process multiple team invitations at once.

```bash
python accept_team_invitations.py accept_team_invitations \
    --base_url <BASE_URL> \
    --input_file_path <INPUT_FILE_PATH>
```

**Options**

- `base_url` **(required)**: The base URL of the API endpoint.
- `input_file_path` **(required)**: Path to the CSV file containing user data. Default is "./sample-files/accept_team_invitations_input.csv".

#### Input File Format

The CSV file should contain the following data, each representing an invitation for a user to join a team. Each invitation comprises:

1. **Invited User's Client ID**: The client ID owned by the user being invited for authentication.
2. **Invited User's Client Secret**: The client secret owned by the user being invited for authentication.
3. **Team ID**: The ID of the team for which the invitation will be accepted.

Example CSV file content (located at [`sample-files/accept_team_invitations_input.csv`](sample-files/accept_team_invitations_input.csv)):

```csv
abcd1234-9afb-4d51-b9a2-db2aae188a86,1234abcd-849b-4d0a-bf8e-02ee530e1532,1
efgh5678-337a-48e3-a980-e67cc2919e4e,5678efgh-d25c-4b5d-be58-5f97209ee7ee,2
...
```

**Note:** You can automatically retrieve the Client ID and Client Secret for newly created users by utilizing the [Create Bulk Users](#create-bulk-users) script.