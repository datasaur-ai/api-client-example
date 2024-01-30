import time
from urllib.parse import urljoin

import requests

from .get_access_token import get_access_token
from .loggable import loggable_with_args


class AdminRESTClient:
    def __init__(
        self, base_url: str, admin_client_id: str, admin_client_secret: str
    ) -> None:
        self.url = base_url
        self.client_id = admin_client_id
        self.client_secret = admin_client_secret
        self.token = None

    @loggable_with_args
    def call_rest(self, path: str, data, method="POST"):
        if self.__should_set_self_token():
            self.token = get_access_token(self.client_id, self.client_secret, self.url)

        assert self.token is not None
        headers = {
            "Authorization": f'Bearer {self.token["access_token"]}',
            "User-Agent": "api-client/apply-labels AdminRESTClient",
        }
        return requests.request(
            method=method,
            url=urljoin(self.url, path),
            data=data,
            headers=headers,
        )

    def __should_set_self_token(self) -> bool:
        return self.token is None or self.token["expires_at"] < time.time()
