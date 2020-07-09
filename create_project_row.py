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

# Read question from external file
with open('row-based-questions.json', 'r') as file:
    questionsString = file.read()
    questions = json.loads(questionsString)

# Read Json payload from external file to make it more convenient
with open('create_project_row.json', 'r') as file:
    operationsString = file.read()
    operations = json.loads(operationsString)

# Inject teamId
operations["variables"]["input"]["teamId"] = str(teamId)
documents = []
onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]

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

# Inject question from row-based-questions.json only for first document
operations["variables"]["input"]["documents"] = documents
operations["variables"]["input"]["documents"][0] = {
  "name": operations["variables"]["input"]["documents"][0]["name"],
  "fileName": operations["variables"]["input"]["documents"][0]["fileName"],
  "settings": {
    "questions": questions
  },
  "docFileOptions": {
    "customHeaderColumns": [
      "Book Cover 1",
      "Book Cover 2"
    ]
    # "firstRowAsHeader": true
  }
}

# For uploading files, you could see https://datasaurai.gitbook.io/datasaur/datasaur-apis/create-new-project/references-1
payload = {'operations': json.dumps(operations), 'map': json.dumps(fileMap)}


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