import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
import json
import sys
import datetime

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

baseUrl = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]
teamId = sys.argv[4]
csvFile = sys.argv[5]
url = baseUrl + "/graphql"

# Retrieving access token, you could store the access token instead of creating it every single time you creating the project.
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url= baseUrl + '/api/oauth/token', client_id=client_id,
        client_secret=client_secret)

# Read options for Hierarchical Dropdown's Answer Set 
with open('google-taxonomy-full-options.json', 'r') as file:
    optionsString = file.read()
    options = json.loads(optionsString)

# Read Json payload from external file to make it more convenient
with open('create_project_row.json', 'r') as file:
    operationsString = file.read()
    operations = json.loads(operationsString)

# Inject teamId
operations["variables"]["input"]["teamId"] = str(teamId)
# Inject Options into first question (take a look at create_project_row.json, I put hierarchical dropdown question as a first one)
operations["variables"]["input"]["documents"][0]["settings"]["questions"][0]["config"]["options"] = options

files = [
  ('1', open(csvFile,'rb'))
]

# For uploading files, you could see https://datasaurai.gitbook.io/datasaur/datasaur-apis/create-new-project/references-1
payload = {'operations': json.dumps(operations), 'map': '{"1":["variables.input.documents.0.file"]}'}

headers = {
  'Authorization': 'Bearer ' + token['access_token']
}

# Call Datasaur API
first_time = datetime.datetime.now()
response = requests.request("POST", url, headers=headers, data = payload, files = files)
later_time = datetime.datetime.now()
difference = later_time - first_time
jsonResponse = json.loads(response.text.encode('utf8'))
print(json.dumps(jsonResponse, indent=1))
print("elapsed time " + str(difference.total_seconds()))