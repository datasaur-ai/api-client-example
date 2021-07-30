import requests
import json
import time
from src.helper import get_operations


class Job():
    check_job_interval_seconds = 30

    def get_status(self, url, access_token, job_id):
        operations = get_operations('src/get_job_status.json')
        operations["variables"]["input"] = job_id
        data = json.dumps(operations)
        headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
        while True:
            response = requests.request("POST", url, headers=headers, data=data)
            if not 'json' in response.headers['content-type'] or response.status_code != 200:
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
                    time.sleep(self.check_job_interval_seconds)
