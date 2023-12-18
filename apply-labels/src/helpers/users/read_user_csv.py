import csv
import logging

from src.models import User


def read_users_csv(csv_path: str):
    with open(csv_path) as csvfile:
        logging.debug(f"reading {csv_path}...")
        users_csv_data = list(csv.reader(csvfile))

    users_data: dict[str, User] = dict()
    for user_csv in users_csv_data:
        user = User(
            id=user_csv[0],
            email=user_csv[1],
            client_id=user_csv[4],
            client_secret=user_csv[5],
        )
        users_data[user.email] = user

    return users_data
