from json import dumps
from typing import Any

from src.helpers import GraphQLClient, OAuthCredentials, get_operations
from src.jobs import Jobs


def replicate_cabinet(client: GraphQLClient, project, labelers: list[dict]):
    labeler_cabinets: list[dict[str, Any]] = project["labelerCabinets"]

    ongoing_replication: list[str] = []

    for labeler in labelers:
        filtered_cabinet = [
            cabinet
            for cabinet in labeler_cabinets
            if cabinet["owner"]["email"] == labeler["email"]
        ]

        if len(filtered_cabinet) == 0:
            replicate_operation = get_operations("src/project/replicate_cabinet.json")
            replicate_operation["variables"] = dumps(
                {
                    "projectId": project["id"],
                    "role": "LABELER",
                }
            )

            response = client.call_graphql(
                data=replicate_operation,
                call_as=OAuthCredentials(
                    client_id=labeler["client_id"],
                    client_secret=labeler["client_secret"],
                ),
            )
            print(f"Replicate cabinet for {labeler['email']}")
            print(f"{response=}")
            ongoing_replication.append(response["data"]["result"]["id"])

        else:
            print(f"Cabinet for {labeler['email']} already exists")

    if len(ongoing_replication) > 0:
        Jobs(client).poll_and_wait(ongoing_replication, call_as=None)
