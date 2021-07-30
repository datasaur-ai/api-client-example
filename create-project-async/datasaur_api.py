import fire
from os import environ
from src.project import Project
from src.job import Job
from src.helper import get_access_token

def create_project(base_url, client_id, client_secret, team_id):
    try:
        access_token = get_access_token(base_url, client_id, client_secret)
        url = base_url + "/graphql"
        project = Project()
        project.create(url, access_token, str(team_id))
    except Exception as e:
        raise SystemExit(e)

def get_job_status(base_url, client_id, client_secret, job_id):
    try:
        access_token = get_access_token(base_url, client_id, client_secret)
        url = base_url + "/graphql"
        job = Job()
        job.get_status(url, access_token, str(job_id))
    except Exception as e:
        raise SystemExit(e)

if __name__ == '__main__':
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    fire.Fire()
