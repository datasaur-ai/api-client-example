from src.helpers import GraphQLClient, get_operations
from json import dumps


class Project:
    def __init__(self, client: GraphQLClient) -> None:
        self.client = client

    def fetch(self, team_id: str, project_id: str):
        operation = get_operations("src/project/get_project.json")
        variables = dumps({"team_id": team_id, "project_id": project_id})
        operation["variables"] = variables
        return self.client.call_graphql(data=operation)
