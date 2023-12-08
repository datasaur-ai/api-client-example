from pprint import pprint

import fire
from dotenv import load_dotenv
from pyjson5 import load as json5_load

from src.entrypoint import check_login_and_teams
from src.helpers import GraphQLClient, read_config
from src.project import Project

load_dotenv()


def validate_project(
    team_id: str,
    project_id: str,
    labelers_file: str = "labelers.json",
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

    with open(labelers_file, "r") as f:
        data = json5_load(f)
        labelers = [l["email"] for l in data["labelers"]]

    project = Project(client=client).validate(
        team_id=team_id,
        project_id=project_id,
        labelers=labelers,
    )
    pprint(project)


if __name__ == "__main__":
    fire.Fire(
        {"check_teams": check_login_and_teams, "validate_project": validate_project}
    )
