import json
import os

from src.graphql_document_creator import GraphQLDocument, GraphQLDocumentCreator
from src.graphql_utils import GraphQLUtils
from src.helper import get_access_token, get_operations


class Project:
    def __init__(self, base_url: str, id: str, secret: str, documents_path: str):
        if os.path.isfile(documents_path):
            raise NotImplementedError(
                "createProject with a list of documents is not yet implemented"
            )

        self.base_url = base_url
        self.graphql_url = f"{base_url}/graphql"
        self.proxy_url = f"{base_url}/api/static/proxy/upload"
        self.client_id = id
        self.client_secret = secret
        self.documents_path = documents_path

        access_token = get_access_token(
            self.base_url, self.client_id, self.client_secret
        )
        self.headers: dict[str, str] = {
            "Authorization": f"Bearer {access_token}",
        }

    def create(self, team_id: str, operations_path: str, name: str | None = None):
        gql_documents = GraphQLDocumentCreator(
            proxy_url=self.proxy_url, headers=self.headers, documents_path=self.documents_path).create()

        operations = self._get_operations(
            team_id, operations_path, gql_documents, name)

        gql = GraphQLUtils(base_url=self.base_url, headers=self.headers,
                           client_id=self.client_id, client_secret=self.client_secret)

        graphql_response = gql.call_graphql(
            data={
                "query": operations["query"],
                "variables": json.dumps(operations["variables"]),
                "operationName": operations.get(
                    "operationName", "Datasaur API client - createProject"
                ),
            }
        )

        gql.process_graphql_response(graphql_response)

    def _get_operations(self, team_id: str, operations_path: str, documents: list[GraphQLDocument], name: str | None):
        operations = get_operations(operations_path)
        operations["variables"]["input"]["teamId"] = team_id
        if name is not None:
            operations["variables"]["input"]["name"] = name

        operations["variables"]["input"]["documents"] = documents

        return operations
