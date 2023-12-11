from os import getenv
from os import path as ospath

from .get_operations import *
from .graphql_client import *
from .load_jsonc import *
from .loggable import *


def read_config(base_url, client_id, client_secret):
    base_url = base_url or getenv("BASE_URL")
    client_id = client_id or getenv("CLIENT_ID")
    client_secret = client_secret or getenv("CLIENT_SECRET")

    if not base_url or not client_id or not client_secret:
        raise ValueError("base_url, client_id, and client_secret are required")

    return dict(
        base_url=base_url,
        client_id=client_id,
        client_secret=client_secret,
    )


def inspect_filepath(filepath: str):
    head, tail = ospath.split(filepath)
    filename, extension = ospath.splitext(tail)
    return (head, tail, dict(filename=filename, extension=extension))
