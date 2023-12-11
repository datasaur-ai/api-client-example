from json import dumps
from typing import Any

from src.helpers import GraphQLClient, OAuthCredentials, get_operations
from src.jobs.jobs import Jobs


class Cabinet:
    def __init__(self, client: GraphQLClient, project: dict[str, Any]):
        self.client = client
        self.project = project

    def replicate_cabinet(self, labelers: list[dict[str, Any]]):
        labeler_cabinets: list[dict[str, Any]] = self.project["labelerCabinets"]
        ongoing_replication: list[str] = []
        replicate_operation = get_operations("src/project/replicate_cabinet.json")

        for labeler in labelers:
            filtered_cabinet = [
                cabinet
                for cabinet in labeler_cabinets
                if cabinet["owner"]["email"] == labeler["email"]
            ]

            if len(filtered_cabinet) == 0:
                replicate_operation["variables"] = dumps(
                    {
                        "projectId": self.project["id"],
                        "role": "LABELER",
                    }
                )

                response = self.client.call_graphql(
                    data=replicate_operation,
                    call_as=OAuthCredentials(
                        client_id=labeler["client_id"],
                        client_secret=labeler["client_secret"],
                    ),
                )
                if self.client.verbose:
                    print(f"Replicate cabinet for {labeler['email']}")
                    print(f"{response=}")
                ongoing_replication.append(response["data"]["result"]["id"])
            else:
                if self.client.verbose:
                    print(f"Cabinet for {labeler['email']} already exists")

        if len(ongoing_replication) > 0:
            Jobs(self.client).poll_and_wait(ongoing_replication, call_as=None)

    def fetch(self, labeler: dict[str, Any]):
        credentials = OAuthCredentials(
            client_id=labeler["client_id"], client_secret=labeler["client_secret"]
        )
        get_cabinet = get_operations("src/project/get_cabinet.json")
        get_cabinet["variables"] = dumps(
            {"projectId": self.project["id"], "role": "LABELER"}
        )
        response = self.client.call_graphql(call_as=credentials, data=get_cabinet)

        return response["data"]["result"]
