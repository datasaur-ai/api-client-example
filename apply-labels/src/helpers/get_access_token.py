from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from termcolor import colored


def get_access_token(
    client_id: str,
    client_secret: str,
    base_url="https://app.datasaur.ai",
    verbose=False,
):
    if verbose:
        print(colored(f"Getting access token for {client_id}", "green"))
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(
        token_url=f"{base_url}/api/oauth/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    if verbose:
        print(colored(f"{token=}", "green"))
    return token["access_token"]
