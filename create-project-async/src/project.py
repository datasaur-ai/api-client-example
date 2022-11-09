import glob
import json
import os

import requests
from src.exceptions.invalid_options import InvalidOptions
from src.helper import get_access_token, get_operations


class Project:
    @staticmethod
    def create(
        base_url, client_id, client_secret, team_id, operations_path, documents_path
    ):
        if os.path.isfile(documents_path):
            print('received a file for documents_path, processing as list of documents...')
            return Project.__handle_document_list(base_url, client_id, client_secret, team_id, operations_path, documents_path)
        

        url = f"{base_url}/graphql"
        access_token = get_access_token(base_url, client_id, client_secret)
        operations = get_operations(operations_path)
        # Set input.teamId
        operations["variables"]["input"]["teamId"] = team_id

        payload_map = {}
        documents = []
        files = []

        # Set files in documents folder as input.documents
        for iterator, filepath in enumerate(glob.iglob(f"{documents_path}/*")):
            current_file = (str(iterator), open(filepath, "rb"))
            files.append(current_file)
            document = {"fileName": filepath[10:], "file": None}
            payload_map[str(iterator)] = [
                "variables.input.documents." + str(iterator) + ".file"
            ]
            documents.append(document)

        # do not copy these properties from operations file, we already set them above
        manual_keys = ["filename", "file"]

        # apply other settings from operations file
        for iterator, op_doc in enumerate(
            operations["variables"]["input"]["documents"]
        ):
            op_doc: dict
            for key in op_doc.keys():
                if key not in manual_keys:
                    documents[iterator][key] = op_doc.get(key, None)

        operations["variables"]["input"]["documents"] = documents

        headers = {"Authorization": "Bearer " + access_token}
        data = {"operations": json.dumps(operations), "map": json.dumps(payload_map)}
        response = Project.__call_graphql(
            url=url, headers=headers, data=data, files=files
        )
        Project.__process_graphql_response(response, base_url, client_id, client_secret)

    @staticmethod
    def __handle_document_list(
        base_url,
        client_id,
        client_secret,
        team_id,
        operations_path,
        documents_list_path,
    ):
        graphql_url = f"{base_url}/graphql"
        access_token = get_access_token(base_url, client_id, client_secret)
        operations = get_operations(operations_path)
        # Set input.teamId
        operations["variables"]["input"]["teamId"] = team_id
        has_eos_id = operations["variables"]["input"].get("externalObjectStorageId", False)

        documents = []
        manual_keys = ["file", "fileName", "externalImportableUrl", "externalObjectStorageFileKey"]
        with open(documents_list_path) as reader:
            documents_list = json.load(reader)

        for d in documents_list:
            file_url = d.get("url", None) or d.get("externalImportableUrl")
            file_name = (
                d.get("fileName", None) or d.get("filename", None) or d.get("name")
            )
            file_key = d.get("externalObjectStorageFileKey", None)

            if has_eos_id and file_key is None:
                raise InvalidOptions("externalObjectStorageId needs externalObjectStorageKey in documents array")

            documents.append(
                {
                    "externalImportableUrl": file_url,
                    "fileName": file_name,
                    "file": None,
                    "externalObjectStorageFileKey": file_key
                }
            )

        for index, op_doc in enumerate(operations["variables"]["input"]["documents"]):
            for key in op_doc.keys():
                if key not in manual_keys:
                    documents[index][key] = op_doc.get(key, None)

        operations["variables"]["input"]["documents"] = documents
        headers = {"Authorization": "Bearer " + access_token}
        data = {
            "query": operations["query"],
            "variables": json.dumps(operations["variables"]),
            "operations": json.dumps(operations),
        }
        response = Project.__call_graphql(url=graphql_url, headers=headers, data=data)
        Project.__process_graphql_response(response, base_url, client_id, client_secret)

    @staticmethod
    def __call_graphql(url: str, headers: dict, data: dict, files=None):
        return requests.request("POST", url, headers=headers, data=data, files=files)

    @staticmethod
    def __process_graphql_response(response, base_url, client_id, client_secret):
        if "json" in response.headers["content-type"]:
            json_response = json.loads(response.text.encode("utf8"))
            if "errors" in json_response:
                print(json.dumps(json_response["errors"], indent=1))
            else:
                job = json_response["data"]["launchTextProjectAsync"]["job"]
                print(json.dumps(job, indent=1))
                print("Check job status using command bellow")
                get_job_status_command = f"python api_client.py get_job_status --base_url {base_url} --client_id {client_id} --client_secret {client_secret} --job_id {job['id']}"
                print(get_job_status_command)
        else:
            print(response.text.encode("utf8"))
            print(response)
