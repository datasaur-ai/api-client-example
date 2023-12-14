import logging
import os
from csv import reader
from json import dumps
from typing import Any

from termcolor import colored

from src.helpers import GraphQLClient, get_operations, inspect_filepath
from src.helpers.loggable import loggable_with_args

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 100))


class RowProjectDocument:
    def __init__(
        self,
        client: GraphQLClient,
        cabinet,
        question_set: tuple[str, list],
        metas: list[dict[str, Any]],
    ) -> None:
        self.client = client
        self.cabinet = cabinet
        self.question_set = question_set
        self.metas = metas

    def apply_row_answers(
        self,
        labeler: dict[str, Any],
    ):
        json_documents, cabinet_documents = self._prepare_documents(
            answer_files=labeler["documents"], cabinet=self.cabinet
        )

        for json_document in json_documents:
            _, filename, _ = inspect_filepath(json_document["filePath"])
            matching_documents = [
                d for d in cabinet_documents if d["fileName"] == filename
            ]

            if len(matching_documents) == 0:
                logging.info(f"document {json_document} not found in cabinet")
                continue

            doc = matching_documents[0]

            self.apply_answer_per_document(
                doc_id=doc["id"],
                filepath=json_document["filePath"],
                labeler_email=labeler["email"],
            )

    @loggable_with_args
    def apply_answer_per_document(self, doc_id: str, filepath: str, labeler_email: str):
        valid_data = self.validate_columns(filepath)
        logging.info(
            f"applying answer for labeler: {labeler_email}, document: {doc_id} from {filepath}"
        )
        return self.__apply_answer_per_document_in_batches(
            doc_id, valid_data, self.question_set
        )

    def __apply_answer_per_document_in_batches(
        self, doc_id: str, valid_data: list[list[str]], question_set: tuple[str, list]
    ):
        _, data = valid_data[0], valid_data[1:]

        # python 3.12 have itertools.batched, but it's very new
        # manual batching for now
        batched_data = [
            data[i : i + CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)
        ]

        logging.debug(
            f"total rows in file: {len(valid_data)}, batched to {len(batched_data)}"
        )

        for i, batch in enumerate(batched_data):
            self.__apply_answer_per_document(
                doc_id=doc_id,
                batch_data=batch,
                question_set=question_set,
                starting_index=i * CHUNK_SIZE,
            )

    def __apply_answer_per_document(
        self,
        doc_id: str,
        batch_data: list[list[str]],
        question_set: tuple[str, list],
        starting_index=0,
    ):
        signature, questions = question_set
        row_answers = []
        for line_index, row in enumerate(batch_data):
            answer = {}
            for q in questions:
                try:
                    answer[q[0]] = row[q[1]["id"]]
                except IndexError:
                    # index error here means the prelabeled file does not have the answer for this question
                    pass
            row_answers.append({"line": line_index + starting_index, "answers": answer})

        return self.call_graphql(
            document_id=doc_id, row_answers=row_answers, signature=signature
        )

    def call_graphql(self, document_id: str, row_answers: list[dict], signature: str):
        operation = get_operations("src/project/update_multi_row_answer.json")
        operation["variables"] = dumps(
            {
                "input": dict(rowAnswers=row_answers, textDocumentId=document_id),
                "questionSetSignature": signature,
            }
        )
        response = self.client.call_graphql(data=operation)
        return response["data"]["result"]

    def _prepare_documents(self, answer_files: list[str], cabinet: dict[str, Any]):
        documents_from_json = [{"filePath": document} for document in answer_files]
        documents_in_cabinet = [
            {
                "fileName": document["fileName"],
                "id": document["id"],
                "signature": document["signature"],
            }
            for document in cabinet["documents"]
        ]
        return (documents_from_json, documents_in_cabinet)

    def validate_columns(self, answerFile: str):
        with open(answerFile, "r") as read_obj:
            data = list(reader(read_obj, delimiter=","))

        headers = data[0]
        valid_columns = [
            index
            for index, header in enumerate(headers)
            if header_in_metas_and_is_question(header, self.metas)
        ]

        if len(valid_columns) == 0:
            raise Exception("No valid columns")

        valid_data = [[d[i] for i in valid_columns] for d in data]

        if len(valid_data) == 0:
            raise Exception("No valid data")

        return valid_data


def header_in_metas_and_is_question(header: str, metas: list[dict[str, Any]]):
    should_warn = True
    for meta in metas:
        if meta["name"] == header and meta["rowQuestionIndex"] is not None:
            return True
        if meta["name"] == header:
            should_warn = False

    if should_warn:
        logging.warn(colored(f"header {header} not found in metas", "yellow"))
    return False
