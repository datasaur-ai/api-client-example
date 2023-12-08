from pprint import pprint
from os import getenv

import fire
from dotenv import load_dotenv

from src.team import Team
from src.project import Project
from src.helpers import GraphQLClient

load_dotenv()


def check_login_and_teams(
    i_base_url: str | None = None,
    i_client_id: str | None = None,
    i_client_secret: str | None = None,
    verbose: bool = False,
):
    """
    Login using admin's CLIENT_ID and CLIENT_SECRET, then queries all team visible from the admin's account.
    """
    config = read_config(i_base_url, i_client_id, i_client_secret)
    client = GraphQLClient(
        base_url=config["base_url"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        verbose=verbose,
    )
    teams = Team(base_url=config["base_url"], client=client).fetch()

    pprint(teams)


def get_project(
    team_id: str,
    project_id: str,
    i_base_url: str | None = None,
    i_client_id: str | None = None,
    i_client_secret: str | None = None,
    verbose: bool = False,
):
    """
    Get a project's assignment and cabinet detail
    """
    config = read_config(i_base_url, i_client_id, i_client_secret)
    client = GraphQLClient(
        base_url=config["base_url"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        verbose=verbose,
    )
    project = Project(client=client).fetch(team_id=team_id, project_id=project_id)
    pprint(project)


def read_config(base_url, client_id, client_secret):
    base_url = base_url or getenv("BASE_URL")
    client_id = client_id or getenv("CLIENT_ID")
    client_secret = client_secret or getenv("CLIENT_SECRET")

    if not base_url or not client_id or not client_secret:
        raise ValueError("base_url, client_id, and client_secret are required")

    return dict(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
    )


if __name__ == "__main__":
    fire.Fire({"check_teams": check_login_and_teams, "get_project": get_project})
