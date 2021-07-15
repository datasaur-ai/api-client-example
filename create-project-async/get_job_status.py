import requests
import os
import json
import sys
import datetime
from helper import get_access_token, get_operations

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

BASE_URL = sys.argv[1]
CLIENT_ID = sys.argv[2]
CLIENT_SECRET = sys.argv[3]
JOB_ID = sys.argv[4]
URL = BASE_URL + "/graphql"

# Read Json payload from external file to make it more convenient
operations = get_operations('get_job_status.json')

operations["variables"]["input"] = str(JOB_ID)

# Retrieving access token, you could store the access token instead of creating it every single time you call datasaur api.
access_token = get_access_token(BASE_URL, CLIENT_ID, CLIENT_SECRET)

# Call Datasaur API
headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
data = json.dumps(operations)
response = requests.request("POST", URL, headers=headers, data=data)
jsonResponse = json.loads(response.text.encode('utf8'))
print(json.dumps(jsonResponse, indent=1))
