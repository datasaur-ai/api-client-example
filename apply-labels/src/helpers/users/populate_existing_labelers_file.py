import json
import logging

from pyjson5 import load as json5_load

from src.models import LabelerAssignment

from ..check_file_exist import check_file_exist
from .read_user_csv import read_users_csv


def populate_existing_labelers_file(users_csv: str, labelers_file: str):
    check_file_exist(users_csv)

    users_data = read_users_csv(users_csv)

    with open(labelers_file) as jsonfile:
        logging.debug(f"reading {labelers_file}...")
        json_data = json5_load(jsonfile)

    labelers_data: dict[str, LabelerAssignment] = dict()
    for labeler_json in json_data["labelers"]:
        labeler = LabelerAssignment(
            client_id=labeler_json.get("client_id", None),
            client_secret=labeler_json.get("client_secret", None),
            email=labeler_json["email"],
            documents=labeler_json["documents"],
        )
        labelers_data[labeler.email] = labeler

    for user_email, user in users_data.items():
        if labelers_data.get(user_email, None):
            logging.debug(
                f"found entry for {user_email} in {labelers_file}, updating client_id and client_secret"
            )
            labeler = labelers_data[user_email]
            labeler.client_id = user.client_id
            labeler.client_secret = user.client_secret
        else:
            logging.debug(f"adding entry for {user_email} in {labelers_file}")
            labeler = LabelerAssignment(
                client_id=user.client_id,
                client_secret=user.client_secret,
                email=user.email,
                documents="",
            )
            labelers_data[user_email] = labeler

    with open(labelers_file, "w") as jsonfile:
        json.dump(
            obj={"labelers": [labeler.__dict__ for labeler in labelers_data.values()]},
            fp=jsonfile,
            indent=2,
        )
