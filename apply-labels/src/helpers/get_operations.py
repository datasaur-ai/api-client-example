import json


def get_operations(file_name: str):
    return json.load(open(file_name, mode="r", encoding="utf-8"))
