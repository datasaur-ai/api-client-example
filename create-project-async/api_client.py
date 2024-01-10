from os import environ

import fire
from src.helper import get_operations
from src.job import Job
from src.portioned_assignment import PortionedAssignment
from src.project import Project


def create_project(base_url, client_id, client_secret, team_id, documents_path="documents", operations_path="create_project.json"):
    try:
        operations = get_operations(operations_path)
        Project(base_url=base_url, id=client_id, secret=client_secret).create(
            team_id=team_id,
            documents_path=documents_path,
            operations=operations,
        )
    except Exception as e:
        raise SystemExit(e)

def create_project_portioned_assignment(
    base_url,
    client_id,
    client_secret,
    team_id,
    documents_path="documents",
    operations_path="create_project.json",
    multi_pass_prefix="multi-",
    single_pass_prefix="single-",
    multi_pass_labeler_count=2):
    try:
        operations = get_operations(operations_path)

        PortionedAssignment.validate(operations)

        new_assignments = PortionedAssignment(
            old_assignments=operations["variables"]["input"]["documentAssignments"],
            multi_pass_prefix=multi_pass_prefix,
            single_pass_prefix=single_pass_prefix,
            multi_pass_labeler_count=multi_pass_labeler_count
        ).create_new_assignments_by_documents(documents_path=documents_path)

        operations["variables"]["input"]["documentAssignments"] = new_assignments

        Project(base_url=base_url, id=client_id, secret=client_secret).create(
            team_id=team_id,
            documents_path=documents_path,
            operations=operations,
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
