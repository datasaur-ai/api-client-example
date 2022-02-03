from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests
import os
import copy


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
    response = requests.request("POST", url, headers=headers, data=json.dumps(operations), verify=verify)
    json_response = json.loads(response.text.encode('utf8'))
    print('--- request begin --- ')
    print('request:')
    print(operations)
    print('response:')
    print(json.dumps(json_response, indent=1))
    print('--- request end ---')
    return json_response

def request_all_pages(url, access_token, operations, verify):
  pagination = { 'page': {'skip': 0, 'take': 1} }

  all_nodes = []
  while True: 
    query_operations = copy.deepcopy(operations)
    query_operations['variables']['input'].update(pagination)
    json_response = post_request(url, access_token, query_operations, verify)
    data = json_response['data']
    all_nodes.extend(data['result']['nodes'])
    if data['result']['pageInfo']['nextCursor'] is None:
        break
    pagination = { 'cursor': data['result']['pageInfo']['nextCursor'] }

  return all_nodes


def get_projects(url, access_token, team_id, parameters, verify):
    operations = get_operations('src/get_projects.json')

    operations["variables"]["input"]["filter"]["teamId"] = team_id
    if 'keyword' in parameters:
        operations["variables"]["input"]["filter"]["keyword"] = parameters['keyword']
    if 'statuses' in parameters:
        operations["variables"]["input"]["filter"]["statuses"] = parameters['statuses']

    return request_all_pages(url, access_token, operations, verify)