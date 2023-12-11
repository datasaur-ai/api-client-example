import csv
import fire
import os
import pprint
import sys

# This code is necessary for the script to access essential functions from the toolbox directory
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing required helper functions from the toolbox directory
from toolbox.get_access_token import get_access_token
from toolbox.post_request import post_request


def create_users(base_url, client_id, client_secret, input_file_path="./sample-files/create_users_sample.csv", email_verified=0):
    try:
        api_url = base_url + "/api/v1/users"
        access_token = get_access_token(base_url, client_id, client_secret)

        with open(input_file_path, newline='') as input_file:
            users = csv.reader(input_file, delimiter=',')
            for user in users:
                new_user = {
                    "email": user[0],
                    "name": user[1],
                    "password": user[2],
                    "emailVerified": email_verified
                }
                response = post_request(api_url, access_token, new_user)

                if "json" in response.headers["content-type"]:
                    pprint.pprint(response.json())
                else:
                    print(response)
    except Exception as e:
        raise SystemExit(e)


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire()
