import fire
import json
import os

from get_single_project import get_single_project

from toolbox.get_access_token import get_access_token
from toolbox.get_operations import get_operations
from toolbox.post_request import post_request


def remove_project_tags(base_url, client_id, client_secret, project_id, tags_to_be_removed):
    url = base_url + "/graphql"
    access_token = get_access_token(base_url, client_id, client_secret)
    operations = get_operations("update_project_tags.json")

    operations["variables"]["input"]["projectId"] = project_id

    project_tags = get_single_project(url, access_token, project_id)["tags"]
    tags_to_be_preserved = []
    for tag in project_tags:
        if tag["name"] not in tags_to_be_removed or tag["globalTag"] == True:
            tags_to_be_preserved.append(tag)
    
    if len(project_tags) == len(tags_to_be_preserved):
        return
    
    tag_ids_to_be_preserved = [tag["id"] for tag in tags_to_be_preserved]

    operations["variables"]["input"]["tagIds"] = tag_ids_to_be_preserved
    del operations["variables"]["input"]["tags"]

    response = post_request(url, access_token, operations)
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]
        return result
    else:
        return response


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire(remove_project_tags)
