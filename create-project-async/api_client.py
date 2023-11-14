from os import environ

import fire
from src.job import Job
from src.project import Project


def create_project(base_url, client_id, client_secret, team_id, documents_path="documents", operations_path="create_project.json"):
    try:
        Project(base_url=base_url, id=client_id, secret=client_secret).create(
            team_id=team_id,
            documents_path=documents_path,
            operations_path=operations_path,
        )
    except Exception as e:
        raise SystemExit(e)


def get_job_status(base_url, client_id, client_secret, job_id):
    try:
        Job.get_status(
            base_url,
            client_id,
            client_secret,
            job_id=str(job_id),
            operations_path="src/get_job_status.json",
        )
    except Exception as e:
        raise SystemExit(e)


if __name__ == "__main__":
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    fire.Fire()
