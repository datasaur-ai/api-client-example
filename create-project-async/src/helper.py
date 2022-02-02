from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests
import os

def get_access_token(base_url, client_id, client_secret):
    verify = os.environ['VERIFY_SSL'] == '1'
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=base_url + '/api/oauth/token',
                              client_id=client_id, client_secret=client_secret, verify=verify)
    return token['access_token']


def get_operations(file_name):
    with open(file_name, 'r') as file:
        return json.loads(file.read())

def post_request(url, access_token, operations, verify):
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    return requests.request("POST", url, headers=headers, data=json.dumps(operations), verify=verify)