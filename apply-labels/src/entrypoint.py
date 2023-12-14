from pprint import pprint

from .helpers import GraphQLClient, read_config
from .team import Team


def check_login_and_teams(
    base_url: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    verbose: bool = False,
):
    """
    Login using admin's CLIENT_ID and CLIENT_SECRET, then queries all team visible from the admin's account.
    """
    config = read_config(base_url, client_id, client_secret)
    client = GraphQLClient(
        base_url=config["base_url"],
        client_id=config["client_id"],
        client_secret=config["client_secret"],
    )
    teams = Team(base_url=config["base_url"], client=client).fetch()

    pprint(teams)
