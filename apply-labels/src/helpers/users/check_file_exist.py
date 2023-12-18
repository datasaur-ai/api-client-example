import os


def check_file_exist(filepath: str):
    if not os.path.isfile(filepath):
        raise Exception("File does not exist")
