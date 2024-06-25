import glob
import os

from typing import TypedDict
from requests import post


class GraphQLDocument(TypedDict):
    document: dict
    extras: list[dict] | None


class GraphQLDocumentCreator:
    def __init__(self, proxy_url: str, headers: dict[str, str], documents_path: str):
        self.proxy_url = proxy_url
        self.headers = headers
        self.documents_path = documents_path

    def create(self):
        mapped_documents = self.__get_mapped_documents()
        return self.__get_graphql_documents(mapped_documents)

    def __get_mapped_documents(self):
        filepaths = list(glob.iglob(f"{self.documents_path}/*"))
        sorted_filepaths = self.__sort_possible_extra_files_last(filepaths)
        mapped_documents = self.__map_documents(sorted_filepaths)
        return mapped_documents

    def __get_graphql_documents(self, mapped_documents: dict[str, dict]):
        graphql_documents: list[GraphQLDocument] = []
        for key in mapped_documents:
            upload_document_response = self.__upload_file(
                filepath=mapped_documents[key]["document"]
            )
            documents: GraphQLDocument = {
                "document": {
                    "name": os.path.basename(mapped_documents[key]["document"]),
                    "objectKey": upload_document_response["objectKey"],
                },
                "extras": None
            }

            if "extra" in mapped_documents[key]:
                upload_extra_response = self.__upload_file(
                    filepath=mapped_documents[key]["extra"]
                )
                documents["extras"] = [
                    {
                        "name": os.path.basename(mapped_documents[key]["extra"]),
                        "objectKey": upload_extra_response["objectKey"],
                    }
                ]

            graphql_documents.append(documents)

        return graphql_documents

    def __upload_file(self, filepath: str):
        print("Uploading file: ", os.path.basename(filepath))
        with post(
            url=self.proxy_url,
            headers=self.headers,
            files=[("file", open(filepath, "rb"))],
        ) as response:
            response.raise_for_status()
            return response.json()

    def __sort_possible_extra_files_last(self, filepaths: list[str]):
        # Sort file paths ending with .json or .txt to be at the end
        filepaths.sort(key=lambda x: (
            x.endswith(".json") or x.endswith(".txt"), x))
        return filepaths

    def __map_documents(self, filepaths: list[str]):
        mapped_documents: dict[str, dict] = {}
        for filepath in filepaths:
            filename = os.path.basename(filepath).split(".")[0]
            if filename in mapped_documents:
                mapped_documents[filename]["extra"] = filepath
            else:
                mapped_documents[filename] = {"document": filepath}
        return mapped_documents
