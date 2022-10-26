import requests
import os
import json
import time
import glob
from typing import List
from urllib.parse import urlparse
from google.cloud import storage
from src.helper import get_access_token, get_operations, get_projects, get_bucket_path_information, post_request

POOLING_INVERVAL = 0.5  # 0.5s

class Export():
    @staticmethod
    def export_projects(base_url, client_id, client_secret, team_id, project_status: List[str], export_format, output_dir):
        verify = os.environ['VERIFY_SSL'] == '1'
        url = f'{base_url}/graphql'
        access_token = get_access_token(base_url, client_id, client_secret)

        print("project_status has " + str(len(project_status)) + " parameters")
        if (len(project_status) == 0):
            print("we will retrieve projects without filtering by status")
        print(project_status)
        parameters = { 'statuses': project_status }
        print("parameters")
        print(parameters)
        projects = get_projects(url, access_token, team_id, parameters, verify)
        print("exporting " + str(len(projects)) + " project(s)")
        for project in projects:
            project_id = project["id"]
            project_name = project['name']
            Export.export(url, access_token, project_id, project_id + "_" + project_name, export_format, output_dir, verify)

    @staticmethod
    def export_single_project(base_url, client_id, client_secret, project_id, export_file_name, export_format, output_dir):
        verify = os.environ['VERIFY_SSL'] == '1'
        url = f'{base_url}/graphql'
        access_token = get_access_token(base_url, client_id, client_secret)
        Export.export(url, access_token, project_id, export_file_name, export_format, output_dir, verify)

    @staticmethod
    def export(url, access_token, project_id, export_file_name, export_format, output_dir, verify):
        operations = get_operations("src/export.json")
        operations["variables"]["input"]["fileName"] = export_file_name
        operations["variables"]["input"]["projectIds"] = [project_id]
        operations["variables"]["input"]["format"] = export_format

        json_response = post_request(url, access_token, operations, verify)
        if len(json_response["data"]["result"]["fileUrl"]) > 0:
            export_id = json_response["data"]["result"]["exportId"]
            Export.poll_export_delivery_status(url, access_token, export_id)
            file_url = json_response["data"]["result"]["fileUrl"]
            Export.store_file(output_dir, file_url)
            
    @staticmethod
    def download_file(file_url):
        file_response = requests.request("GET", file_url)
        print("Success downloading the file:" + file_url)
        return file_response.content;

    @staticmethod
    def store_file(output_dir, file_url):
        content = Export.download_file(file_url)
        file_response_url = urlparse(file_url)
        file_name = os.path.basename(file_response_url.path)
        bucket_path_information = get_bucket_path_information(output_dir)
        if bucket_path_information is None:
            # store locally
            os.makedirs(output_dir, exist_ok=True)            
            output_file = output_dir + '/' + file_name
            open(output_file, 'wb').write(content)
            print("Successfully write the file to local filesystem. Output file:" + output_file)
        else:
            storage_client = storage.Client()
            bucket_name = bucket_path_information["bucket_name"]
            path = bucket_path_information["path"]
            bucket = storage_client.bucket(bucket_name)
            output_file_path = path + '/' + file_name
            blob = bucket.blob(output_file_path)
            blob.upload_from_string(content)
            print('Successfuly write the file to gcs. Bucket:' + bucket_name + ' path: ' + output_file_path.strip(' /'))

    @staticmethod
    def poll_export_delivery_status(url, access_token, export_id):
        verify = os.environ['VERIFY_SSL'] == '1'
        operations = get_operations('src/get_export_delivery_status.json')
        operations["variables"]["exportId"] = export_id
        while True:
            time.sleep(POOLING_INVERVAL)
            json_response = post_request(url, access_token, operations, verify)
            delivery_status = json_response["data"]["exportDeliveryStatus"]["deliveryStatus"]
            if (delivery_status == "QUEUED"):
                print("Waiting for exported file to be ready...")
            elif (delivery_status == "DELIVERED"):
                print("Exported file is ready")
                break
            elif (delivery_status == "FAILED"):
                print("Failed to export file")
                print(json_response["data"]["exportDeliveryStatus"]["errors"])
                break
    
