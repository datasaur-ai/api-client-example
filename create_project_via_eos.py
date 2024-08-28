import fire
import json
import os

from toolbox.get_access_token import get_access_token
from toolbox.get_operations import get_operations
from toolbox.post_request import post_request

def create_project_via_eos(base_url, client_id, client_secret):
    url = base_url + "/graphql"
    access_token = get_access_token(base_url, client_id, client_secret)
    operations = get_operations("create_project_via_eos.json")

    response = post_request(url, access_token, operations)
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        return json_response
    else:
        return response.text

if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire(create_project_via_eos)
