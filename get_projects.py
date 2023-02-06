import asyncio
import fire
import json
import os
import requests

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


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

    response = asyncio.run(post_request(url, access_token, operations))
    if "json" in response.headers["content-type"]:
        json_response = json.loads(response.text.encode("utf8"))
        result = json_response["data"]["result"]["nodes"]
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


async def post_request(url, access_token, operations):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    result = requests.request("POST", url, headers=headers, data=json.dumps(operations))
    return result


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire(get_projects)
