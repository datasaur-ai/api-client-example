import time
from collections import namedtuple

from .call_graphql import call_graphql
from .get_access_token import get_access_token

OAuthCredentials = namedtuple("OAuthCredentials", ["client_id", "client_secret"])


class GraphQLClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: None | dict = None

    def call_graphql(self, data, call_as: OAuthCredentials | None = None):
        token = None
        if call_as is None:
            if self.__should_set_self_token():
                self.token = get_access_token(
                    self.client_id, self.client_secret, self.url
                )

            # silences Pylance's Object of type "None" is not subscriptable
            # checked in __should_set_self_token()
            assert self.token is not None
            token = self.token["access_token"]
        else:
            full_token = get_access_token(
                client_id=call_as.client_id,
                client_secret=call_as.client_secret,
                base_url=self.url,
            )
            token = full_token["access_token"]

        # token should be populated from before
        assert token is not None
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "api-client/apply-labels GraphQLClient",
        }
        return call_graphql(f"{self.url}/graphql", headers, data=data)

    def __should_set_self_token(self) -> bool:
        return self.token is None or self.token["expires_at"] < time.time()
