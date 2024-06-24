import json

from requests import post


class GraphQLUtils:
    def __init__(self, base_url, client_id, client_secret, headers):
        self.base_url = base_url
        self.graphql_url = f"{base_url}/graphql"
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = headers

    def call_graphql(self, data):
        return post(url=self.graphql_url, headers=self.headers, data=data)

    def process_graphql_response(self, response):
        if "json" in response.headers["content-type"]:
            json_response: dict = json.loads(response.text.encode("utf8"))
            if "errors" in json_response:
                print(json.dumps(json_response["errors"], indent=1))
            else:
                job = json_response["data"]["result"]["job"]
                print(json.dumps(job, indent=1))
                print("Check job status using the command below")
                get_job_status_command = f"python api_client.py get_job_status --base_url {self.base_url} --client_id {self.client_id} --client_secret {self.client_secret} --job_id {job['id']}"
                print(get_job_status_command)
        else:
            print(response.text.encode("utf8"))
            print(response)
