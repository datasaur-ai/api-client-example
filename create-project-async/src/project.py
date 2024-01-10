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

    def create(self, team_id, operations, documents_path):
        if (os.path.isfile(documents_path)):
            raise NotImplementedError("createProject with a list of documents is not yet implemented")

        access_token = get_access_token(self.base_url, self.client_id, self.client_secret)
        self.headers = self.__add_headers(key='Authorization', value=f"Bearer {access_token}")

        operations["variables"]["input"]["documents"] = []
        operations["variables"]["input"]["teamId"] = team_id

        for filepath in glob.iglob(f"{documents_path}/*"):
            upload_response = self.__upload_file(filepath=filepath)
            documents = {
                "document": {
                    "name": filepath.split('/')[-1],
                    "objectKey": upload_response["objectKey"]
                }
            }
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
                get_job_status_command = f"python api_client.py get_job_status --base_url {self.base_url} --client_id {self.client_id} --client_secret {self.client_secret} --job_id {job['id']}"
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
