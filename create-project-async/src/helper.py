from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
from csv import reader as csvreader


def get_access_token(base_url, client_id, client_secret):
    print("Getting access token...")
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(
        token_url=base_url + "/api/oauth/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    print("Access token received.")
    return token["access_token"]


def get_operations(file_name):
    with open(file_name, "r") as file:
        return json.loads(file.read())


def parse_multiple_config(config_path: str):
    with open(config_path, "r") as file:
        config_reader = csvreader(file)
        yield from config_reader
