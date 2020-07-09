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

fileMapping = {}
files = []

for x in range(documentSize):
  idx = x + 1
  fileMapping[idx] = ["variables.input.documents." + str(x) + ".file"]
  files.append((str(idx), open('./littleprince.txt', 'rb')))
  if x == 0:
    document = {
      "name": "littleprince.txt",
      "fileName": "littleprince.txt",
      "docFileOptions": {
        "customHeaderColumns": [
          "Document"
        ],
        "firstRowAsHeader": True
      },
      "settings" : {
        "questions" : {
          "name": "Q1",
          "label": "Question 1",
          "required": False,
          "type": "HIERARCHICAL_DROPDOWN",
          "config" : {
            "multiple": False,
            "options": options,
          },
        }
      }
    }
  else:
    document = {
      "name": "littleprince" + str(idx) + ".txt",
      "fileName": "littleprince"+ str(idx) + ".txt",
      "docFileOptions": {
        "customHeaderColumns": [
          "Document"
        ],
        "firstRowAsHeader": True
      },
    }
  operations["variables"]["input"]["documents"].append(document)

payload = {'operations': json.dumps(operations), 'map': json.dumps(fileMapping)}

headers = {
  'Authorization': 'Bearer ' + token['access_token']
}

first_time = datetime.datetime.now()
response = requests.request("POST", url, headers=headers, data = payload, files = files)
later_time = datetime.datetime.now()
difference = later_time - first_time
jsonResponse = json.loads(response.text.encode('utf8'))
print(json.dumps(jsonResponse, indent=1))
print("elapsed time " + str(difference.total_seconds()))