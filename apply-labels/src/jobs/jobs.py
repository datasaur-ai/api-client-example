import logging
from json import dumps
from random import randint
from time import sleep

from src.helpers import GraphQLClient, OAuthCredentials, get_operations


class Jobs:
    def __init__(self, client: GraphQLClient) -> None:
        self.client = client

    def poll_and_wait(
        self, ids_to_query_next: list[str], call_as: OAuthCredentials | None
    ):
        operation = get_operations("src/jobs/get_jobs.json")

        while len(ids_to_query_next) > 0:
            operation["variables"] = dumps({"jobIds": ids_to_query_next})
            response = self.client.call_graphql(data=operation, call_as=call_as)
            ids_to_query_next = [
                job["id"]
                for job in response["data"]["result"]
                if job["status"] not in ["DELIVERED", "FAILED"]
            ]

            failed_jobs = [
                job for job in response["data"]["result"] if job["status"] == "FAILED"
            ]

            if (len(failed_jobs)) > 0:
                logging.warning(f"{failed_jobs=}")
                raise Exception("Some job failed")

            delivered_jobs = [
                job
                for job in response["data"]["result"]
                if job["status"] == "DELIVERED"
            ]
            logging.debug(f"{delivered_jobs=}")
            logging.debug(f"{ids_to_query_next=}")

            if (len(ids_to_query_next)) > 0:
                sleep(randint(1, 3))
