import glob
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TypedDict

from requests import post


class GraphQLDocument(TypedDict):
    document: dict
    extras: list[dict] | None


class GraphQLDocumentCreator:
    MAX_WORKERS = 8

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
        print(f"uploading files using {self.MAX_WORKERS} workers")
        graphql_documents: list[GraphQLDocument] = []
        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            futures = [
                executor.submit(
                    self.__upload_and_create_document,
                    key=key,
                    mapped_documents=mapped_documents,
                )
                for key in mapped_documents.keys()
            ]

            uploaded = 0
            for future in as_completed(futures):
                gql_document = future.result()
                uploaded += 1
                print(f"uploaded {uploaded}/{len(futures)} files", end="\r")
                graphql_documents.append(gql_document)

            print()

        return graphql_documents

    def __upload_and_create_document(self, key: str, mapped_documents: dict[str, dict]):
        upload_document_response = self.__upload_file(mapped_documents[key]["document"])
        document: GraphQLDocument = {
            "document": {
                "name": os.path.basename(mapped_documents[key]["document"]),
                "objectKey": upload_document_response["objectKey"],
            },
            "extras": None,
        }

        if "extra" in mapped_documents[key]:
            upload_extra_response = self.__upload_file(
                filepath=mapped_documents[key]["extra"]
            )
            document["extras"] = [
                {
                    "name": os.path.basename(mapped_documents[key]["extra"]),
                    "objectKey": upload_extra_response["objectKey"],
                }
            ]
        return document

    def __upload_file(self, filepath: str):
        with post(
            url=self.proxy_url,
            headers=self.headers,
            files=[("file", open(filepath, "rb"))],
        ) as response:
            response.raise_for_status()
            return response.json()

    def __sort_possible_extra_files_last(self, filepaths: list[str]):
        # Sort file paths ending with .json, .txt, or .xml to be at the end
        EXTRA_FILES_EXTENSIONS = (".json", ".txt", ".xml")
        return sorted(
            filepaths,
            key=lambda x: (os.path.splitext(x)[-1] in EXTRA_FILES_EXTENSIONS, x),
        )

    def __map_documents(self, filepaths: list[str]):
        mapped_documents: dict[str, dict] = {}
        for filepath in filepaths:
            filename = os.path.basename(filepath).split(".")[0]
            if filename in mapped_documents:
                mapped_documents[filename]["extra"] = filepath
            else:
                mapped_documents[filename] = {"document": filepath}
        return mapped_documents
