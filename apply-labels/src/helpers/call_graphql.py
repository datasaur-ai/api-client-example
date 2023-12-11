import requests
from termcolor import colored


def call_graphql(url: str, headers: dict[str, str], data, verbose=False):
    if verbose:
        print(colored(f"{url=}", "grey"))
        print(colored(f"{data=}", "grey"))

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise ValueError(f"GraphQL request failed: {response.text}")

    return response.json()
