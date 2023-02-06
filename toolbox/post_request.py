import json
import requests


def post_request(url, access_token, operations):
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
    }
    result = requests.request("POST", url, headers=headers, data=json.dumps(operations))
    return result
