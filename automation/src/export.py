import requests
import os
import json
import time
import glob
from typing import List
from urllib.parse import urlparse
from src.helper import get_access_token, get_operations, get_projects, post_request

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
            file_response = requests.request("GET", file_url)
            os.makedirs(output_dir, exist_ok=True)
            file_response_url = urlparse(file_url)
            file_name = os.path.basename(file_response_url.path)
            output_file = output_dir + '/' + file_name
            open(output_file, 'wb').write(file_response.content)
            print("Success downloading the file. Output file:" + output_file)
        

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
    
