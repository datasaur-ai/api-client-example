import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from os import listdir
from os.path import isfile, join
import os
import json
import sys
import datetime

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

baseUrl = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]
teamId = sys.argv[4]
folderPath = sys.argv[5]
url = baseUrl + "/graphql"

# Retrieving access token, you could store the access token instead of creating it every single time you creating the project.
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url= baseUrl + '/api/oauth/token', client_id=client_id,
        client_secret=client_secret)

headers = {
  'Authorization': 'Bearer ' + token['access_token'],
  'Content-Type': 'application/json'
}

# Read Create Label Set Request
with open('create_label_set.json', 'r') as file:
    labelSetString = file.read()

# Create Label Set
response = requests.request("POST", url, headers=headers, data = labelSetString)
labelSetJsonResponse = json.loads(response.text.encode('utf8'))
labelSetId = labelSetJsonResponse["data"]["createLabelSet"]["id"]

# Read Json payload from external file to make it more convenient
#
# -------------------- IMPORTANT --------------------------
# Please change assignee in create_project_token.json file
# -------------------- IMPORTANT --------------------------
with open('create_project_token.json', 'r') as file:
    operationsString = file.read()
    operations = json.loads(operationsString)

# Inject teamId
operations["variables"]["input"]["teamId"] = str(teamId)
operations["variables"]["input"]["labelSetId"] = str(labelSetId)

documents = []
onlyfiles = [f for f in listdir(folderPath) if not f.startswith('.') and isfile(join(folderPath, f))]

files = []
fileMap = {}
# fileMap example
# '{"1":["variables.input.documents.0.file"]}'

idx = 1
for file in onlyfiles:
  documents.append({
    "name": file,
    "fileName": file
  })
  files.append((str(idx), open(folderPath + '/' + file, 'rb')))
  fileMap[str(idx)] = ['variables.input.documents.' + str(idx - 1) + '.file']
  idx = idx + 1

operations["variables"]["input"]["documents"] = documents
operations["variables"]["input"]["name"] = "NER Project with " + str(idx - 1) + " files"


# For uploading files, you could see https://datasaurai.gitbook.io/datasaur/datasaur-apis/create-new-project/references-1
createProjectPayload = {'operations': json.dumps(operations), 'map': json.dumps(fileMap)}
headers = {
  'Authorization': 'Bearer ' + token['access_token']
}
# Call Datasaur API
first_time = datetime.datetime.now()
response = requests.request("POST", url, headers=headers, data = createProjectPayload, files = files)
later_time = datetime.datetime.now()
difference = later_time - first_time
print("elapsed time " + str(difference.total_seconds()))
print(response)
if 'json' in response.headers['content-type']:
  jsonResponse = json.loads(response.text.encode('utf8'))
  print(json.dumps(jsonResponse, indent=1))
