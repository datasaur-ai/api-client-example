import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import os
import json
import sys

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

baseUrl = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]
teamId = sys.argv[4]
documentSize = int(sys.argv[5])
url = baseUrl + "/graphql"

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url= baseUrl + '/api/oauth/token', client_id=client_id,
        client_secret=client_secret)

with open('options-simple.json', 'r') as file:
    optionsString = file.read()
    options = json.loads(optionsString)


with open('create_project_doc.json', 'r') as file:
    operationsString = file.read()
    operations = json.loads(operationsString)

operations["variables"]["input"]["teamId"] = str(teamId)


for x in range(documentSize):
  idx = x + 1
  if x == 0:
    document = {
      "teamId": teamId,
      "name": "littleprince.txt",
      "fileName": "littleprince.txt",
      "fileUrl": "https://vulcan-prod.s3.amazonaws.com/files/gitbook/littleprince.txt",
      "docFileOptions": {
        "customHeaderColumns": [
          "Document"
        ],
        "firstRowAsHeader": True
      },
      "settings" : {
        "questions" : [
          {
            "name": "Q1",
            "label": "Question 1",
            "required": False,
            "type": "HIERARCHICAL_DROPDOWN",
            "config" : {
              "multiple": False,
              "options": options,
            },
          },
          {
            "name": "Q2 name",
            "label": "Question 2 Label",
            "required": False,
            "type": "DATE",
            "config" : {
              "multiple": False,
              "options": options,
            },
          },
        ]
      }
    }
  else:
    document = {
      "teamId": "1",
      "name": "littleprince" + str(idx) + ".txt",
      "fileName": "littleprince" + str(idx) + ".txt",
      "fileUrl": "https://vulcan-prod.s3.amazonaws.com/files/gitbook/littleprince.txt",
      "docFileOptions": {
        "customHeaderColumns": [
          "Document"
        ],
        "firstRowAsHeader": True
      },
    }
  operations["variables"]["input"]["documents"].append(document)

payload = json.dumps(operations)

headers = {
  'Authorization': 'Bearer ' + token['access_token'],
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)
print(response.text.encode('utf8'))