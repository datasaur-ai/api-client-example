import requests
import os
import json
import glob
from dotenv import load_dotenv
from .helper import get_access_token, get_operations

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class Project():
    def create(self, url, access_token, team_id):
        operations = get_operations('src/create_project.json')
        # Set input.teamId
        operations["variables"]["input"]["teamId"] = team_id

        payload_map = {}
        documents = []
        files = []

        # Set files in documents folder as input.documents
        iterator = 0
        for filepath in glob.iglob('documents/*'):
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

        # Call Datasaur API
        headers = {'Authorization': 'Bearer ' + access_token}
        data = {'operations': json.dumps(operations), 'map': json.dumps(payload_map)}
        response = requests.request("POST", url, headers=headers, data=data, files=files)
        if 'json' in response.headers['content-type']:
            json_response = json.loads(response.text.encode('utf8'))
            if 'errors' in json_response:
                print(json.dumps(json_response['errors'], indent=1))
            else:
                job = json_response['data']['launchTextProjectAsync']['job']
                print(json.dumps(job, indent=1))
                print('Check job status using script bellow')
                print(f'python3 get_job_status.py { job["id"] }')
        else:
            print(response)
            print(response.text.encode('utf8'))
