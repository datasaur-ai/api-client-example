import requests
import os
import json
import time
import glob
from urllib.parse import urlparse
from src.helper import get_access_token, get_operations, post_request

POOLING_INVERVAL = 0.5  # 0.5s

class Export():
    @staticmethod
    def export(base_url, client_id, client_secret, project_id, export_file_name, export_format, output_dir):
        verify = os.environ['VERIFY_SSL'] == '1'
        url = f'{base_url}/graphql'
        access_token = get_access_token(base_url, client_id, client_secret)
        operations = get_operations("src/export.json")
        operations["variables"]["input"]["fileName"] = export_file_name
        operations["variables"]["input"]["projectIds"] = [project_id]
        operations["variables"]["input"]["format"] = export_format

        response = post_request(url, access_token, operations, verify)
        if 'json' in response.headers['content-type']:
            json_response = json.loads(response.text.encode('utf8'))
            print(json.dumps(json_response, indent=1))

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
        else:
            print(response)

    @staticmethod
    def poll_export_delivery_status(url, access_token, export_id):
        verify = os.environ['VERIFY_SSL'] == '1'
        operations = get_operations('src/get_export_delivery_status.json')
        operations["variables"]["exportId"] = export_id
        while True:
            time.sleep(POOLING_INVERVAL)
            response = post_request(url, access_token, operations, verify)
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
                    print(json_response["data"]["exportDeliveryStatus"]["errors"])
                    break
            else:
                print(response)
                break    
    
