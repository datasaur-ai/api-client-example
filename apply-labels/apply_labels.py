import logging
import os
import traceback

import fire
from dotenv import load_dotenv
from helpers.users.load_labelers_and_populate_credentials import (
    load_labelers_and_populate_credentials,
)

from src.entrypoint import check_login_and_teams
from src.helpers import (
    GraphQLClient,
    create_labelers_file,
    populate_existing_labelers_file,
    read_config,
)
from src.project import Project

load_dotenv()


def apply_row_answers(
    team_id: str,
    project_id: str,
    labelers_file="labelers.json",
    base_url: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    users_csv: str | None = None,
    verbose: bool = False,
):
    """
    The script will query the project's assignment and cabinet detail, then:
    1. Replicate cabinet to each assigned member, if not exist
    2. Open and apply labels to each document in the cabinet for each assignee.

    Uses BASE_URL, CLIENT_ID, and CLIENT_SECRET from .env by default.
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        config = read_config(base_url, client_id, client_secret)
        client = GraphQLClient(
            base_url=config["base_url"],
            client_id=config["client_id"],
            client_secret=config["client_secret"],
        )

        if (users_csv is not None) and (os.path.isfile(labelers_file)):
            logging.info(
                f"mapping users from {users_csv} to labelers file: {labelers_file}"
            )
            populate_existing_labelers_file(users_csv, labelers_file)

        # data = load_jsonc(labelers_file)
        data = load_labelers_and_populate_credentials(
            labelers_file=labelers_file, config=config
        )

        Project(client=client).apply_row_answers(
            team_id=team_id,
            project_id=project_id,
            labelers=data,
        )
        logging.info("apply_row_answers completed")
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        raise SystemExit(e)


def convert_to_json(users_csv: str, labelers_file: str):
    if os.path.exists(labelers_file):
        populate_existing_labelers_file(users_csv, labelers_file)
    else:
        create_labelers_file(users_csv, labelers_file)


if __name__ == "__main__":
    fire.Fire(
        {
            "check_teams": check_login_and_teams,
            "apply_row_answers": apply_row_answers,
            "convert_to_json": convert_to_json,
        }
    )
