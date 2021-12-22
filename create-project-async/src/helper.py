from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json


def get_access_token(base_url, client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=base_url + '/api/oauth/token',
                              client_id=client_id, client_secret=client_secret)
    return token['access_token']


def get_operations(file_name):
    with open(file_name, 'r') as file:
        return json.loads(file.read())
