import os


def check_file_exist(filepath: str):
    if not os.path.exists(filepath):
        raise Exception("File does not exist")
