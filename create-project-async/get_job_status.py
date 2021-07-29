import requests
import os
import json
import sys
import time
from dotenv import load_dotenv
from helper import get_access_token, get_operations

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv()
BASE_URL = os.getenv('BASE_URL')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TEAM_ID = os.getenv('TEAM_ID')
JOB_ID = sys.argv[1]
URL = BASE_URL + "/graphql"
CHECK_JOB_INTERVAL_SECONDS = 30

# Read Json payload from external file to make it more convenient
operations = get_operations('get_job_status.json')

operations["variables"]["input"] = str(JOB_ID)

# Retrieving access token, you could store the access token instead of creating it every single time you call datasaur api.
access_token = get_access_token(BASE_URL, CLIENT_ID, CLIENT_SECRET)

# Pool Job Status
data = json.dumps(operations)
headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
while True:
    response = requests.request("POST", URL, headers=headers, data=data)
    if 'json' in response.headers['content-type']:
        json_response = json.loads(response.text.encode('utf8'))
        if response.status_code == 200:
            job = json_response['data']['job']
            if job is None:
                print('job not found')
                break
            else:
                print(json.dumps(job, indent=1))
                if job['status'] == "DELIVERED":
                    break
                elif job['status'] == "FAILED":
                    print(json.dumps(job['errors']))
                    break
                else:
                    print('getting job status..')
                    time.sleep(CHECK_JOB_INTERVAL_SECONDS)
        else:
            print(json_response['errors'])
            break
    else:
        print('invalid response headers')
        break
