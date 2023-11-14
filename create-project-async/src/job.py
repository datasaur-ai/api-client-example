import requests
import json
import time
from .helper import get_access_token, get_operations

CHECK_JOB_INTERVAL_SECONDS = 5


class Job():
    @staticmethod
    def get_status(base_url, client_id, client_secret, job_id, operations_path):
        url = f'{base_url}/graphql'
        access_token = get_access_token(base_url, client_id, client_secret)
        operations = get_operations(operations_path)
        operations["variables"]["input"] = job_id
        data = json.dumps(operations)
        headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
        proxies = {'all': 'socks5://127.0.0.1:8900'}
        while True:
            response = requests.request("POST", url, headers=headers, data=data, proxies=proxies, verify=False)
            if response.status_code != 200 or not ('json' in response.headers['content-type']):
                print(response.text.encode('utf8'))
                return
            json_response = json.loads(response.text.encode('utf8'))
            job = json_response['data']['job']
            if job is None:
                print('job not found')
                break
            else:
                print(json.dumps(job, indent=1))
                if job['status'] == "DELIVERED":
                    break
                elif job['status'] == "FAILED":
                    print(json.dumps(job['errors']))
                    break
                else:
                    print('getting job status..')
                    time.sleep(CHECK_JOB_INTERVAL_SECONDS)
