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
labelSetIds = [labelSetJsonResponse["data"]["createLabelSet"]["id"]]

# Read create_guideline.json file
with open('create_guideline.json', 'r') as file:
    guidelineString = file.read()

with open('./sample-files/guideline.md', 'r') as file:
    guidelineContent = file.read()

# Create Guideline
createGuidelineOperation = json.loads(guidelineString)
createGuidelineOperation["variables"]["input"]["content"] = guidelineContent
response = requests.request("POST", url, headers=headers, data = json.dumps(createGuidelineOperation))
guidelineJsonResponse = json.loads(response.text.encode('utf8'))
guidelineId = guidelineJsonResponse["data"]["createGuideline"]["id"]

# Read Json payload from external file to make it more convenient
#
# -------------------- IMPORTANT --------------------------
# Please change assignee in create_project_token.json file
# -------------------- IMPORTANT --------------------------
with open('create_project_token_url.json', 'r') as file:
    operationsString = file.read()
    operations = json.loads(operationsString)

# Inject teamId
operations["variables"]["input"]["teamId"] = str(teamId)
operations["variables"]["input"]["labelSetIDs"] = labelSetIds
operations["variables"]["input"]["name"] = "NER Project from URL"

# For uploading files, you could see https://datasaurai.gitbook.io/datasaur/datasaur-apis/create-new-project/references-1
createProjectPayload = json.dumps(operations)
headers = {
  'Authorization': 'Bearer ' + token['access_token'],
  'Content-Type': 'application/json'
}

# Call Datasaur API
first_time = datetime.datetime.now()
response = requests.request("POST", url, headers=headers, data = createProjectPayload)
later_time = datetime.datetime.now()
difference = later_time - first_time
print("elapsed time " + str(difference.total_seconds()))
if 'json' in response.headers['content-type']:
  jsonResponse = json.loads(response.text.encode('utf8'))
  print(json.dumps(jsonResponse, indent=1))
else:
  print(response.text.encode('utf8'))
