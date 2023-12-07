from os import getenv

import fire
from dotenv import load_dotenv

from src.teams import Team

load_dotenv()


def check_login_and_teams(
    base_url: str | None = None,
    client_id: str | None = None,
    client_secret: str | None = None,
    verbose: bool = False,
):
    """
    Check admin's CLIENT_ID and CLIENT_SECRET
    """
    base_url = base_url or getenv("BASE_URL")
    client_id = client_id or getenv("CLIENT_ID")
    client_secret = client_secret or getenv("CLIENT_SECRET")

    if not base_url or not client_id or not client_secret:
        raise ValueError("base_url, client_id, and client_secret are required")

    teams = Team(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
        verbose=verbose,
    ).fetch()

    print(teams)


if __name__ == "__main__":
    fire.Fire({"check_teams": check_login_and_teams})
