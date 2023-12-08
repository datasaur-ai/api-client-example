from json import dumps

from src.helpers import GraphQLClient, get_operations


class Project:
    def __init__(self, client: GraphQLClient) -> None:
        self.client = client

    def fetch(self, team_id: str, project_id: str):
        operation = get_operations("src/project/get_project.json")
        variables = dumps({"team_id": team_id, "project_id": project_id})
        operation["variables"] = variables
        return self.client.call_graphql(data=operation)

    def validate(self, team_id: str, project_id: str, labelers: list[str]):
        fetch_result = self.fetch(team_id=team_id, project_id=project_id)
        project = fetch_result["data"]["result"]

        assigned_user_emails = [
            assignee["teamMember"]["user"]["email"] for assignee in project["assignees"]
        ]

        not_assigned = []

        for labeler in labelers:
            if labeler not in assigned_user_emails:
                not_assigned.append(labeler)

        if len(not_assigned) > 0:
            raise Exception(
                f"Project {project_id} is not assigned to {not_assigned}. Please assign the project to them first."
            )

        print(assigned_user_emails)
