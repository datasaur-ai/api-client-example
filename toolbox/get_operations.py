import json


def get_operations(file_name):
    with open(file_name, "r") as file:
        return json.loads(file.read())
