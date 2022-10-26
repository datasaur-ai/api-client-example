import fire
from os import environ
from src.project import Project
from src.export import Export
from src.job import Job
from typing import List
from dotenv import load_dotenv

def create_project(base_url, client_id, client_secret, team_id):
    try:
        Project.create(
            base_url.strip(' /'), client_id, client_secret,
            team_id=str(team_id),
            operations_path='project_graphql.json', documents_path='documents')
    except Exception as e:
        raise SystemExit(e)

def export_single_project(base_url, client_id, client_secret, project_id, export_file_name, export_format, output_dir):
    try:
        Export.export_single_project(base_url.strip(' /'), client_id, client_secret, project_id, export_file_name, export_format, output_dir)        
    except Exception as e:
        raise SystemExit(e)

def export_projects(base_url, client_id, client_secret, team_id, project_status: List[str], export_format, output_dir):
    try:
        Export.export_projects(base_url.strip(' /'), client_id, client_secret, team_id, project_status, export_format, output_dir)        
    except Exception as e:
        raise SystemExit(e)


def get_job_status(base_url, client_id, client_secret, job_id):
    try:
        Job.get_status(base_url.strip(' /'), client_id, client_secret, job_id=str(
            job_id), operations_path='src/get_job_status.json')
    except Exception as e:
        raise SystemExit(e)


if __name__ == '__main__':
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    load_dotenv()
    fire.Fire()
