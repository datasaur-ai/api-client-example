import requests
import os
import json
import glob
from src.helper import get_access_token, get_operations
from src.job import Job

class Project():
    @staticmethod
    def create(base_url, client_id, client_secret, team_id, operations_path, documents_path):
        verify = os.environ['VERIFY_SSL'] == '1'
        url = f'{base_url}/graphql'
        access_token = get_access_token(base_url, client_id, client_secret)
        operations = get_operations(operations_path)
        # Set input.teamId
        operations["variables"]["input"]["teamId"] = team_id

        payload_map = {}
        documents = []
        files = []
        # Set files in documents folder as input.documents
        for iterator, filepath in enumerate(glob.iglob(f'{documents_path}/*')):
            file = (str(iterator), open(filepath, 'rb'))
            files.append(file)
            document = {
                "fileName": os.path.basename(filepath) + '.txt',
                "file": None,
            }
            if "customScriptId" in operations["variables"]["input"]["documentSettings"]:
                document["customScriptId"] = operations["variables"]["input"]["documentSettings"]["customScriptId"]

            payload_map[str(iterator)] = [
                "variables.input.documents." + str(iterator) + ".file"]
            documents.append(document)

        # do not copy these properties from operations file, we already set them above
        manual_keys = ["filename", "file"]

        # apply other settings from operations file
        for iterator, op_doc in enumerate(operations["variables"]["input"]["documents"]):
            op_doc: dict
            for key in op_doc.keys():
                if not (key in manual_keys):
                    documents[iterator][key] = op_doc.get(key, None)

        operations["variables"]["input"]["documents"] = documents

        # Call Datasaur API
        headers = {'Authorization': 'Bearer ' + access_token}
        data = {'operations': json.dumps(operations), 'map': json.dumps(payload_map)}
        response = requests.request(
            "POST", url, headers=headers, data=data, files=files, verify=verify)
        if 'json' in response.headers['content-type']:
            json_response = json.loads(response.text.encode('utf8'))
            if 'errors' in json_response:
                print(json.dumps(json_response['errors'], indent=1))
            else:
                job = json_response['data']['launchTextProjectAsync']['job']
                print(json.dumps(job, indent=1))

                # Check Project Creation Status
                Job.get_status(base_url, client_id, client_secret, job_id=str(job['id']), operations_path='src/get_job_status.json')
        else:
            print(response)
            print(response.text.encode('utf8'))
