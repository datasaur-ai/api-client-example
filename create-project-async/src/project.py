import json
import os

from typing import TypedDict
from src.graphql_document_creator import GraphQLDocumentCreator
from src.graphql_utils import GraphQLUtils
from src.helper import get_access_token, get_operations


class GraphQLDocument(TypedDict):
    document: dict
    extras: list[dict] | None


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
        self.headers = None
        self.documents_path = documents_path

    def create(self, team_id, operations_path, name=None):
        access_token = get_access_token(
            self.base_url, self.client_id, self.client_secret
        )

        self.headers = self.__add_headers(
            key="Authorization", value=f"Bearer {access_token}"
        )

        gql_documents = GraphQLDocumentCreator(
            proxy_url=self.proxy_url, headers=self.headers, documents_path=self.documents_path).create()

        operations = self.__get_operations(
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

    def __get_operations(self, team_id, operations_path, documents, name):
        operations = get_operations(operations_path)
        operations["variables"]["input"]["teamId"] = team_id
        if name is not None:
            operations["variables"]["input"]["name"] = name

        operations["variables"]["input"]["documents"] = documents

        return operations

    def __add_headers(self, key, value):
        if self.headers is None:
            self.headers = {key: value}
        else:
            self.headers[key] = value

        return self.headers
