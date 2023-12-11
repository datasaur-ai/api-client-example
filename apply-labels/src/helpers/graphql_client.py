from collections import namedtuple

from .call_graphql import call_graphql
from .get_access_token import get_access_token

OAuthCredentials = namedtuple("OAuthCredentials", ["client_id", "client_secret"])


class GraphQLClient:
    def __init__(
        self, base_url: str, client_id: str, client_secret: str, verbose: bool = False
    ):
        self.url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.verbose = verbose

    def call_graphql(self, data, call_as: OAuthCredentials | None = None):
        if call_as is None:
            token = get_access_token(
                self.client_id, self.client_secret, self.url, verbose=self.verbose
            )
        else:
            token = get_access_token(
                client_id=call_as.client_id,
                client_secret=call_as.client_secret,
                base_url=self.url,
                verbose=self.verbose,
            )

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "api-client/apply-labels",
        }
        return call_graphql(
            f"{self.url}/graphql", headers, data=data, verbose=self.verbose
        )
