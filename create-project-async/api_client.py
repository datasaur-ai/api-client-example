import logging
import traceback
import fire

from os import environ
from src.batched_project import DEFAULT_BATCH_SIZE, BatchedProject
from src.helper import parse_multiple_config
from src.job import Job
from src.logger import log as log
from src.project import Project

DEFAULT_OPERATIONS_PATH = "create_project.json"
DEFAULT_DOCUMENTS_PATH = "documents"


def log_error(message, level=logging.ERROR, **kwargs):
    logger = logging.getLogger("api_client")
    return log(logger=logger, level=level, message=message, **kwargs)


def create_project(
    base_url,
    client_id,
    client_secret,
    team_id,
    documents_path=DEFAULT_DOCUMENTS_PATH,
    operations_path=DEFAULT_OPERATIONS_PATH,
):
    try:
        Project(base_url=base_url, id=client_id, secret=client_secret, documents_path=documents_path).create(
            team_id=team_id,
            operations_path=operations_path,
        )
    except Exception as e:
        raise SystemExit(e)


def create_batched_projects(
    base_url,
    client_id,
    client_secret,
    team_id,
    documents_path=DEFAULT_DOCUMENTS_PATH,
    operations_path=DEFAULT_OPERATIONS_PATH,
    document_batch_size=DEFAULT_BATCH_SIZE,
):
    try:
        BatchedProject(base_url=base_url, id=client_id, secret=client_secret, documents_path=documents_path, document_batch_size=document_batch_size).create(
            team_id=team_id,
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


def create_multiple_projects(
    base_url,
    client_id,
    client_secret,
    team_id,
    operations_path=DEFAULT_OPERATIONS_PATH,
    config="config.csv",
):
    project_configs = parse_multiple_config(config)
    for name, documents_path in project_configs:
        try:
            Project(base_url=base_url, id=client_id, secret=client_secret, documents_path=documents_path).create(
                team_id=team_id,
                operations_path=operations_path,
                name=name,
            )
        except Exception as e:
            log_error(
                message=f"Error creating project: {name}",
                exception=traceback.format_exception(e),
            )


if __name__ == "__main__":
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    fire.Fire()
