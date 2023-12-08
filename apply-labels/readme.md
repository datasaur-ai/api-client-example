# Apply labels as labeler from file.

## Table of contents

- [Table of contents](#table-of-contents)
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)

## Prerequisites

- A Datasaur workspace with OAuth credentials enabled. 
- Python 3 (3.10 recommended)

## Quickstart

1. Setup a Datasaur workspace and generate admin OAuth credentials. Save the client id and secret in the `.env` file. We have provided an example `.env.example` you can copy. 
2. Create and invite the labeler accounts you will be applying labels as. For each one, generate OAuth credentials and save the client id and secret. This time, in the .env file, but in a `labelers.json` file. We have provided an example `labelers.json.example` you can refer to.

