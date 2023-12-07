import requests


def call_graphql(url: str, headers: dict[str, str], data, verbose=False):
    if verbose:
        print(f"{url=} {headers=} {data=}")

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise ValueError(f"GraphQL request failed: {response.text}")

    return response.json()
