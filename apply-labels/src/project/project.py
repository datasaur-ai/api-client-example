from collections import namedtuple
from json import dumps

from src.helpers import GraphQLClient, get_operations, loggable

from .cabinet import Cabinet
from .row_document import RowProjectDocument


class Project:
    def __init__(self, client: GraphQLClient) -> None:
        self.client = client

    def apply_row_answers(
        self, team_id: str, project_id: str, labelers: list[dict[str, str]]
    ):
        emails = [l["email"] for l in labelers]
        project = self.fetch_and_validate(
            team_id=team_id, project_id=project_id, labelers=emails, kinds=["ROW_BASED"]
        )
        self.replicate_cabinet(project=project, labelers=labelers)

        for labeler in labelers:
            self.apply_row_answer_for_labeler(project, labeler)

    def apply_row_answer_for_labeler(self, project, labeler):
        question_set = self.get_project_row_questionset(project_id=project["id"])
        cabinet = Cabinet(
            client=self.client,
            project=project,
        ).fetch(labeler=labeler)
        labeler_client = GraphQLClient(
            base_url=self.client.url,
            client_id=labeler["client_id"],
            client_secret=labeler["client_secret"],
        )
        return RowProjectDocument(
            client=labeler_client,
            cabinet=cabinet,
            question_set=question_set,
            metas=get_document_metas(client=labeler_client, cabinet_id=cabinet["id"]),
        ).apply_row_answers(
            labeler=labeler,
        )

    def get_project_row_questionset(self, project_id: str):
        operation = get_operations("src/project/get_row_questions.json")
        variables = dumps({"projectId": project_id})
        operation["variables"] = variables
        qset = self.client.call_graphql(data=operation)["data"]["result"]

        signature = qset["signature"]
        questions = [(f"Q{q['id']}", q) for q in qset["questions"]]

        return (signature, questions)

    @loggable
    def fetch_and_validate(
        self, team_id: str, project_id: str, labelers: list[str], kinds: list[str]
    ):
        fetch_result = self.fetch(team_id=team_id, project_id=project_id)
        project = fetch_result["data"]["result"]
        self.__validate(project=project, labelers=labelers, kinds=kinds)
        return project

    def fetch(self, team_id: str, project_id: str):
        operation = get_operations("src/project/get_project.json")
        variables = dumps({"team_id": team_id, "project_id": project_id})
        operation["variables"] = variables
        return self.client.call_graphql(data=operation)

    def __validate(self, project, labelers, kinds):
        for k in kinds:
            assert k in project["workspaceSettings"]["kinds"]

        assigned_user_emails = [
            assignee["teamMember"]["user"]["email"]
            for assignee in project["assignees"]
            if assignee["role"] == "LABELER"
            or assignee["role"] == "LABELER_AND_REVIEWER"
        ]

        not_assigned = []

        for labeler in labelers:
            if labeler not in assigned_user_emails:
                not_assigned.append(labeler)

        if len(not_assigned) > 0:
            raise Exception(
                f"Project {project['id']} is not assigned to {not_assigned}. Please assign the project to them first."
            )

    @loggable
    def replicate_cabinet(self, project, labelers):
        return Cabinet(client=self.client, project=project).replicate_cabinet(
            labelers=labelers
        )


def get_document_metas(client: GraphQLClient, cabinet_id: str):
    """
    See get_document_metas.result.json for example response
    """
    operation = get_operations("src/project/get_document_metas.json")
    variables = dumps({"cabinetId": cabinet_id})
    operation["variables"] = variables
    response = client.call_graphql(data=operation)
    return response["data"]["result"]
