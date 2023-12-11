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


def create_users(base_url, client_id, client_secret, input_file_path="./sample-files/create_users_input.csv", output_file_path="./sample-files/create_users_output.csv", email_verified=0):
    try:
        api_url = base_url + "/api/v1/users"
        access_token = get_access_token(base_url, client_id, client_secret)

        with open(input_file_path, newline='') as input_file:
            with open(output_file_path, 'w') as output_file:
                users = csv.reader(input_file, delimiter=',')
                writer = csv.writer(output_file)

                for user in users:
                    new_user = {
                        "email": user[0],
                        "name": user[1],
                        "password": user[2],
                        "emailVerified": email_verified
                    }
                    response = post_request(api_url, access_token, new_user)

                    if "json" in response.headers["content-type"]:
                        json_response = response.json()
                        if response.status_code == 200:
                            user_id = json_response["data"]["id"]
                            writer.writerow([user_id, new_user["email"], new_user["name"], new_user["password"]])
                            pprint.pprint(json_response)
                        else:
                            raise Exception("{email} ERROR: {message}".format(email=new_user["email"], message=json_response["message"]))
                    else:
                        raise Exception("{email} ERROR: {status_code}".format(email=new_user["email"], status_code=response.status_code))
    except Exception as e:
        raise SystemExit(e)


if __name__ == "__main__":
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire()
