import asyncio
import json
from toolbox.get_operations import get_operations
from toolbox.post_request import post_request


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
