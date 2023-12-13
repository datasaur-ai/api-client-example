import csv
import fire
import os
import sys

# This code is necessary for the script to access essential functions from the toolbox directory
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing required helper functions from the toolbox directory
from toolbox.get_access_token import get_access_token
from toolbox.get_operations import get_operations
from toolbox.post_request import post_request


def accept_team_invitations(base_url, input_file_path="./sample-files/accept_team_invitations_input.csv"):
    try:
        url = base_url + "/graphql"

        with open(input_file_path, newline='') as input_file:
            users_data = list(csv.reader(input_file, delimiter=','))

        for user_data in users_data:
            client_id = user_data[0]
            client_secret = user_data[1]
            team_id = user_data[2]

            access_token = get_access_token(base_url, client_id, client_secret)
            operations = get_operations("get_team_detail.json")

            operations["variables"]["input"]["id"] = team_id

            response = post_request(url, access_token, operations)

            if "json" in response.headers["content-type"]:
                json_response = response.json()
                if response.status_code == 200 and "errors" not in json_response:
                    print("accepted user to team {team_id} ({team_name})".format(team_id=team_id, team_name=json_response["data"]["getTeamDetail"]["name"]))
                else:
                    error_messages = []
                    for error in json_response["errors"]:
                        error_messages.append(error["message"])
                    raise Exception("team {team_id} ERROR: {message}".format(team_id=team_id, message=",".join(error_messages)))
            else:
                raise Exception("team {team_id} ERROR: {status_code})".format(team_id=team_id, status_code=response.status_code))
    except Exception as e:
        raise SystemExit(e)


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire()
