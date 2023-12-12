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