import fire
import json
import os

from toolbox.get_operations import get_operations
from toolbox.post_request import post_request


def get_single_project(url, access_token, project_id):
    operations = get_operations("get_single_project.json")
    operations["variables"]["input"]["projectId"] = project_id

    response = post_request(url, access_token, operations)
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]
        return result
    else:
        print(response)


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire(get_single_project)
