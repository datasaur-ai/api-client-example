from pprint import pprint

from pyjson5 import load as json5_load

from .helpers import GraphQLClient, read_config
from .project import Project
from .team import Team


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
