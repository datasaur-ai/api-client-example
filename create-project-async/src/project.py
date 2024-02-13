import glob
import json
import os

from requests import post
from src.helper import get_access_token, get_operations


class Project:
    def __init__(self, base_url: str, id:str, secret:str):
        self.base_url = base_url
        self.graphql_url = f"{base_url}/graphql"
        self.proxy_url = f"{base_url}/api/static/proxy/upload"
        self.client_id = id
        self.client_secret = secret
        self.headers = None

    def create(self, team_id, operations_path, documents_path):
        if (os.path.isfile(documents_path)):
            raise NotImplementedError("createProject with a list of documents is not yet implemented")

        access_token = get_access_token(self.base_url, self.client_id, self.client_secret)
        self.headers = self.__add_headers(key='Authorization', value=f"Bearer {access_token}")
        operations = get_operations(operations_path)

        operations["variables"]["input"]["documents"] = []
        operations["variables"]["input"]["teamId"] = team_id

        filepaths = list(glob.iglob(f"{documents_path}/*"))
        sorted_filepaths = self.__sort_possible_extra_files_last(filepaths)
        mapped_documents = self.__map_documents(sorted_filepaths)

        for key in mapped_documents:
            upload_document_response = self.__upload_file(filepath=mapped_documents[key]["document"])
            documents = {
                "document": {
                    "name": mapped_documents[key]["document"].split('/')[-1],
                    "objectKey": upload_document_response["objectKey"]
                }
            }

            if "extras" in mapped_documents[key]:
                upload_extras_response = self.__upload_file(filepath=mapped_documents[key]["extras"])
                documents["extras"] = [
                    {
                        "name": mapped_documents[key]["extras"].split('/')[-1],
                        "objectKey": upload_extras_response["objectKey"]
                    }
                ]

            operations["variables"]["input"]["documents"].append(documents)

        graphql_response = self.__call_graphql(
            data={
                "query": operations["query"],
                "variables": json.dumps(operations["variables"]),
                "operationName": operations.get("operationName", "Datasaur API client - createProject")
            }
        )
        self.__process_graphql_response(graphql_response)
  
    def __upload_file(self, filepath):
        with post(
        url=self.proxy_url,
        headers=self.headers,
        files=[('file', open(filepath, 'rb'))]
        ) as response: 
            response.raise_for_status()
            return response.json()

    def __call_graphql(self, data):
        return post(url=self.graphql_url, headers=self.headers, data=data)

    def __process_graphql_response(self, response):
        if "json" in response.headers["content-type"]:
            json_response: dict = json.loads(response.text.encode("utf8"))
            if "errors" in json_response:
                print(json.dumps(json_response["errors"], indent=1))
            else:
                job = json_response["data"]["result"]["job"]
                print(json.dumps(job, indent=1))
                print("Check job status using command bellow")
                get_job_status_command = f"python3 api_client.py get_job_status --base_url {self.base_url} --client_id {self.client_id} --client_secret {self.client_secret} --job_id {job['id']}"
                print(get_job_status_command)
        else:
            print(response.text.encode("utf8"))
            print(response)
    
    def __add_headers(self, key, value):
        if self.headers is None:
            self.headers = {key: value} 
        else:
            self.headers[key] = value

        return self.headers

    def __sort_possible_extra_files_last(self, filepaths):
        # Sort file paths ending with .json or .txt to be at the end
        filepaths.sort(key=lambda x: (x.endswith('.json') or x.endswith('.txt'), x))
        return filepaths

    def __map_documents(self, filepaths):
        mapped_documents = {}
        for filepath in filepaths: 
            filename = filepath.split('/')[-1].split('.')[0]
            if filename in mapped_documents: 
                mapped_documents[filename]["extras"] = filepath
            else: 
                mapped_documents[filename] = { "document": filepath }
        return mapped_documents
