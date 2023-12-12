import requests
from termcolor import colored


def call_graphql(url: str, headers: dict[str, str], data, verbose=False):
    operation_name = data.get("operationName", None)
    decorated_url = f"{url}?operationName={operation_name}"
    if verbose:
        print(colored(f"url={decorated_url}", "grey"))
        if operation_name is not None:
            print(colored(f"{operation_name=}", "grey"))
        else:
            print(colored(f"{data=}", "grey"))

    response = requests.post(decorated_url, headers=headers, data=data)

    if response.status_code != 200:
        raise ValueError(f"GraphQL request failed: {response.text}")

    return response.json()
