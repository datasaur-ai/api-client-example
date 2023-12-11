import fire
from dotenv import load_dotenv

from src.entrypoint import check_login_and_teams
from src.helpers import GraphQLClient, load_jsonc, read_config
from src.project import Project

load_dotenv()


def apply_labels(
    team_id: str,
    project_id: str,
    labelers_file="labelers.json",
    i_base_url: str | None = None,
    i_client_id: str | None = None,
    i_client_secret: str | None = None,
    verbose: bool = False,
):
    """
    The script will query the project's assignment and cabinet detail, then:
    1. Replicate cabinet to each assigned member, if not exist
    2. Open and apply cabinet for each assignee.

    Uses BASSE_URL, CLIENT_ID, and CLIENT_SECRET from .env by default.
    """
    config = read_config(i_base_url, i_client_id, i_client_secret)
    client = GraphQLClient(
        base_url=config["base_url"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        verbose=verbose,
    )

    data = load_jsonc(labelers_file)

    Project(client=client).apply_labels(
        team_id=team_id,
        project_id=project_id,
        labelers=data["labelers"],
    )


if __name__ == "__main__":
    fire.Fire(
        {
            "check_teams": check_login_and_teams,
            "apply_labels": apply_labels,
        }
    )
