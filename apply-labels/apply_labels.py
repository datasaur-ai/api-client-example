import logging
import traceback
from operator import le

import fire
from dotenv import load_dotenv

from src.entrypoint import check_login_and_teams
from src.helpers import GraphQLClient, load_jsonc, read_config
from src.project import Project

load_dotenv()


def apply_row_answers(
    team_id: str,
    project_id: str,
    labelers_file="labelers.json",
    base_url: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
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

        data = load_jsonc(labelers_file)

        Project(client=client).apply_row_answers(
            team_id=team_id,
            project_id=project_id,
            labelers=data["labelers"],
        )
    except Exception as e:
        logging.error(e)
        traceback.print_exc()
        SystemExit(e)


if __name__ == "__main__":
    fire.Fire(
        {
            "check_teams": check_login_and_teams,
            "apply_row_answers": apply_row_answers,
        }
    )
