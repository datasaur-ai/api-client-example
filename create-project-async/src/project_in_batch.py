import json
from src.graphql_document_creator import GraphQLDocumentCreator
from src.graphql_utils import GraphQLUtils
from src.helper import get_access_token
from src.project import Project


class ProjectInBatch(Project):
    def __init__(self, base_url: str, id: str, secret: str, documents_path: str, document_batch_size=20):
        if not 1 <= document_batch_size <= 100:
            raise ValueError("document_batch_size must be between 1 and 100")

        super().__init__(base_url, id, secret, documents_path)
        self.document_batch_size = document_batch_size
        self.graphql_utils = GraphQLUtils(base_url=self.base_url, headers=self.headers,
                                          client_id=self.client_id, client_secret=self.client_secret)

    def create(self, team_id: str, operations_path: str, name: str | None = None):
        access_token = get_access_token(
            self.base_url, self.client_id, self.client_secret
        )

        self.headers = self._add_headers(
            key="Authorization", value=f"Bearer {access_token}"
        )

        chunked_gql_documents = self.__get_chunked_gql_documents()

        for index, gql_documents in enumerate(chunked_gql_documents):
            operations = self._get_operations(
                team_id, operations_path, gql_documents, name)

            name_with_batch_number = self.__get_name_with_batch_number(
                operations["variables"]["input"]["name"], index)
            operations["variables"]["input"]["name"] = name_with_batch_number

            self.__create_project_from_chunk(operations)

    def __get_chunked_gql_documents(self):
        gql_documents = GraphQLDocumentCreator(
            proxy_url=self.proxy_url, headers=self.headers, documents_path=self.documents_path).create()

        return [gql_documents[i:i + self.document_batch_size] for i in range(0, len(gql_documents), self.document_batch_size)]

    def __create_project_from_chunk(self, operations):
        graphql_response = self.graphql_utils.call_graphql(
            data={
                "query": operations["query"],
                "variables": json.dumps(operations["variables"]),
                "operationName": operations.get(
                    "operationName", "Datasaur API client - createProject"
                ),
            }
        )

        self.graphql_utils.process_graphql_response(graphql_response)

    def __get_name_with_batch_number(self, name: str, index: int):
        return f"{name} - batch {index + 1}" if name else None
