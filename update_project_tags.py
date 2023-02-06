import asyncio
import fire
import json
import os
import requests
import time

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def update_project_tags(base_url, client_id, client_secret, team_id, method):
    url = base_url + "/graphql"
    access_token = get_access_token(base_url, client_id, client_secret)
    operations = get_operations("update_project_tags.json")

    project_id = operations["variables"]["input"]["projectId"]
    project_tags = get_single_project(url, access_token, project_id)["tags"]

    team_tags = get_team_tags(url, access_token, team_id)
    team_tag_names = [tag["name"] for tag in team_tags]

    tags_to_be_applied = operations["variables"]["input"]["tags"]

    # create non-existing tags
    for tag_name in tags_to_be_applied:
        if len(tag_name) > 0 and tag_name not in team_tag_names:
            create_tag(url, access_token, team_id, tag_name)
            time.sleep(0.5)

    # refetch after create
    team_tags = get_team_tags(url, access_token, team_id)

    # filter tag by method
    if method == "PUT":
        project_global_tags = [tag for tag in project_tags if tag.get("globalTag")]
        tag_ids_to_be_applied = [tag["id"] for tag in project_global_tags]
    else:
        tag_ids_to_be_applied = [tag["id"] for tag in project_tags]

    # apply tags to project
    for tag_name in tags_to_be_applied:
        if len(tag_name) == 0:
            continue

        tag_item = next(
            team_tag for team_tag in team_tags if team_tag["name"] == tag_name
        )
        tag_ids_to_be_applied.append(tag_item["id"])

    operations["variables"]["input"]["tagIds"] = tag_ids_to_be_applied
    del operations["variables"]["input"]["tags"]

    response = asyncio.run(post_request(url, access_token, operations))
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]
        return result
    else:
        print(response)


def get_access_token(base_url, client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(
        token_url=base_url + "/api/oauth/token",
        client_id=client_id,
        client_secret=client_secret,
        verify=False,
    )
    return token["access_token"]


def get_operations(file_name):
    with open(file_name, "r") as file:
        return json.loads(file.read())


def get_team_tags(url, access_token, team_id):
    operations = get_operations("get_tags.json")
    operations["variables"]["input"]["teamId"] = team_id

    response = asyncio.run(post_request(url, access_token, operations))
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]
        return result
    else:
        print(response)


def create_tag(url, access_token, team_id, tag_name):
    operations = get_operations("create_tag.json")
    operations["variables"]["input"]["teamId"] = team_id
    operations["variables"]["input"]["name"] = tag_name

    response = asyncio.run(post_request(url, access_token, operations))
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["createTag"]
        return result
    else:
        print(response)


def get_single_project(url, access_token, project_id):
    operations = get_operations("get_single_project.json")
    operations["variables"]["input"]["projectId"] = project_id

    response = asyncio.run(post_request(url, access_token, operations))
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]
        return result
    else:
        print(response)


async def post_request(url, access_token, operations):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    result = requests.request(
        "POST", url, headers=headers, data=json.dumps(operations), verify=False
    )
    return result


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire(update_project_tags)
