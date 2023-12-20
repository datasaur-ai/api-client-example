import json

from src.models import LabelerAssignment

from ..check_file_exist import check_file_exist
from .read_user_csv import read_users_csv


def create_labelers_file(csv_path: str, labelers_file: str):
    check_file_exist(csv_path)
    users_data = read_users_csv(csv_path)

    labelers: list[LabelerAssignment] = []
    for user in users_data.values():
        labelers.append(
            LabelerAssignment(
                client_id=user.client_id,
                client_secret=user.client_secret,
                email=user.email,
                documents="",
            )
        )

    with open(labelers_file, "w") as jsonfile:
        json.dump(
            obj={"labelers": [labeler.__dict__ for labeler in labelers]},
            fp=jsonfile,
            indent=2,
        )
