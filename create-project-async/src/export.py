import requests
import os
import json
import glob
from src.helper import get_access_token, get_operations


class Export():
    @staticmethod
    def export(base_url, client_id, client_secret, operations_path, project_id, export_file_name, export_format, output_dir):
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
                "fileName": os.path.basename(filepath),
                "file": None
            }
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
            "POST", url, headers=headers, data=data, files=files)
        if 'json' in response.headers['content-type']:
            json_response = json.loads(response.text.encode('utf8'))
            if 'errors' in json_response:
                print(json.dumps(json_response['errors'], indent=1))
            else:
                job = json_response['data']['launchTextProjectAsync']['job']
                print(json.dumps(job, indent=1))
                print('Check job status using command bellow')
                get_job_status_command = f"python api_client.py get_job_status --base_url {base_url} --client_id {client_id} --client_secret {client_secret} --job_id {job['id']}"
                print(get_job_status_command)
        else:
            print(response)
            print(response.text.encode('utf8'))
