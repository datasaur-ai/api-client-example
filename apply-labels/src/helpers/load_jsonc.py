from pyjson5 import load as pyjson5_load


def load_jsonc(filepath: str):
    with open(filepath, "r") as f:
        data = pyjson5_load(f)

    return data
