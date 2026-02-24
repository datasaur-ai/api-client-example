import json
import os
import time
import requests
import fire

from urllib.parse import urlparse
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

POOLING_INVERVAL = 0.5  # 0.5s


def export_project(base_url, client_id, client_secret, project_id, export_file_name, export_format, output_dir, operation_path='export.json'):
    url = base_url + "/graphql"
    access_token = get_access_token(base_url, client_id, client_secret)
    operations = get_operations(operation_path)

    operations["variables"]["input"]["fileName"] = export_file_name
    operations["variables"]["input"]["projectIds"] = [project_id]
    operations["variables"]["input"]["format"] = export_format

    response = post_request(url, access_token, operations)
    if 'json' in response.headers['content-type']:
        json_response = json.loads(response.text.encode('utf8'))
        print(json.dumps(json_response, indent=1))

        if json_response["data"]["result"]["fileUrl"]:
            export_id = json_response["data"]["result"]["exportId"]
            poll_export_delivery_status(url, access_token, export_id)

            file_url = json_response["data"]["result"]["fileUrl"]
            file_response = requests.request("GET", file_url)
            os.makedirs(output_dir, exist_ok=True)
            file_response_url = urlparse(file_url)
            file_name = os.path.basename(file_response_url.path)
            output_file = output_dir + '/' + file_name
            open(output_file, 'wb').write(file_response.content)
            return "Success downloading the file. Output file:" + output_file
        else: 
            export_id = json_response["data"]["result"]["exportId"]
            poll_export_delivery_status(url, access_token, export_id)
            return "Success exporting the project. Check your storage bucket for the file."
    else:
        return response


def poll_export_delivery_status(url, access_token, export_id):
    operations = get_operations('get_export_delivery_status.json')
    operations["variables"]["exportId"] = export_id
    while True:
        time.sleep(POOLING_INVERVAL)
        response = post_request(url, access_token, operations)
        if 'json' in response.headers['content-type']:
            json_response = json.loads(response.text.encode('utf8'))
            delivery_status = json_response["data"]["exportDeliveryStatus"]["deliveryStatus"]
            if (delivery_status == "QUEUED"):
                print("Waiting for exported file to be ready...")
            elif (delivery_status == "DELIVERED"):
                print("Exported file is ready")
                break
            elif (delivery_status == "FAILED"):
                print("Failed to export file")
                break
        else:
            print(response)
            break


def get_access_token(base_url, client_id, client_secret):
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=base_url + '/api/oauth/token', client_id=client_id,
                              client_secret=client_secret)
    return token['access_token']


def get_operations(file_name):
    with open(file_name, 'r') as file:
        return json.loads(file.read())


def post_request(url, access_token, operations):
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    return requests.request("POST", url, headers=headers, data=json.dumps(operations))


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    fire.Fire(export_project)
