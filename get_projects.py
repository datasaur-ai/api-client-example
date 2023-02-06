import fire
import json
import os

from toolbox.get_access_token import get_access_token
from toolbox.get_operations import get_operations
from toolbox.get_team_tags import get_team_tags
from toolbox.post_request import post_request


def get_projects(base_url, client_id, client_secret):
    url = base_url + "/graphql"
    access_token = get_access_token(base_url, client_id, client_secret)
    operations = get_operations("get_projects.json")

    team_id = operations["variables"]["input"]["filter"]["teamId"]

    team_tags = get_team_tags(url, access_token, team_id)
    filter_tag_names = operations["variables"]["input"]["filter"]["tags"]

    filter_tag_ids = []
    for tag_name in filter_tag_names:
        if len(tag_name) == 0:
            continue

        tag_item = next(
            team_tag for team_tag in team_tags if team_tag["name"] == tag_name
        )
        filter_tag_ids.append(tag_item["id"])
    operations["variables"]["input"]["filter"]["tags"] = filter_tag_ids

    response = post_request(url, access_token, operations)
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]["nodes"]
        return result
    else:
        print(response)


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire(get_projects)
