import requests
import os
import json
import sys
import glob
from helper import get_access_token, get_operations

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

BASE_URL = sys.argv[1]
CLIENT_ID = sys.argv[2]
CLIENT_SECRET = sys.argv[3]
TEAM_ID = sys.argv[4]
URL = BASE_URL + "/graphql"

# Read Json payload from external file to make it more convenient
operations = get_operations('create_project_async.json')

# Set input.teamId
operations["variables"]["input"]["teamId"] = str(TEAM_ID)

payload_map = {}
documents = []
files = []

# Set files in documents folder as input.documents
iterator = 0
for filepath in glob.iglob('documents/*.txt'):
    file = (str(iterator), open(filepath, 'rb'))
    files.append(file)
    document = {
        "fileName": filepath[10:],
        "file": None
    }
    payload_map[str(iterator)] = ["variables.input.documents." + str(iterator) + ".file"]
    documents.append(document)
    iterator += 1

# Use documents.settings and documents.docFileOptions from operations file
if (len(operations["variables"]["input"]["documents"]) > 0 and len(documents) > 0):
    documents[0]["settings"] = operations["variables"]["input"]["documents"][0]["settings"]
    documents[0]["docFileOptions"] = operations["variables"]["input"]["documents"][0]["docFileOptions"]

operations["variables"]["input"]["documents"] = documents

# Retrieving access token, you could store the access token instead of creating it every single time you call datasaur api.
access_token = get_access_token(BASE_URL, CLIENT_ID, CLIENT_SECRET)

# Call Datasaur API
headers = {'Authorization': 'Bearer ' + access_token}
data = {'operations': json.dumps(operations), 'map': json.dumps(payload_map)}
print(data)
response = requests.request("POST", URL, headers=headers, data=data, files=files)
jsonResponse = json.loads(response.text.encode('utf8'))
print(json.dumps(jsonResponse, indent=1))
