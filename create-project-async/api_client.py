import fire
from os import environ
from src.project import Project
from src.export import Export
from src.job import Job

def create_project(base_url, client_id, client_secret, team_id):
    try:
        Project.create(
            base_url, client_id, client_secret,
            team_id=str(team_id),
            operations_path='project_graphql.json', documents_path='documents')
    except Exception as e:
        raise SystemExit(e)

def export_single_project(base_url, client_id, client_secret, project_id, export_file_name, export_format, output_dir):
    try:
        Export.export(base_url, client_id, client_secret, project_id, export_file_name, export_format, output_dir)        
    except Exception as e:
        raise SystemExit(e)


def get_job_status(base_url, client_id, client_secret, job_id):
    try:
        Job.get_status(base_url, client_id, client_secret, job_id=str(
            job_id), operations_path='src/get_job_status.json')
    except Exception as e:
        raise SystemExit(e)


if __name__ == '__main__':
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    fire.Fire()
