import logging
from os import getenv

import requests
from termcolor import colored


def call_graphql(url: str, headers: dict[str, str], data):
    operation_name = data.get("operationName", None)
    decorated_url = f"{url}?operationName={operation_name}"
    logging.debug(colored(f"url={decorated_url}", "grey"))
    if operation_name is not None:
        logging.debug(colored(f"{operation_name=}", "grey"))
    else:
        logging.debug(colored(f"{data=}", "grey"))

    response = requests.post(
        decorated_url,
        headers=headers,
        data=data,
        verify=False if getenv("DISABLE_SSL_VERIFICATION") else True,
    )

    if response.status_code != 200:
        raise ValueError(f"GraphQL request failed: {response.text}")

    return response.json()
