from pprint import pprint
from src.helpers.rest_client import AdminRESTClient


class UserOAuthCredentials:
    def __init__(self, admin_client: AdminRESTClient):
        self.client = admin_client
        self.__check_access()

    def generate_oauth_credentials(self, email: str):
        return self.client.call_rest(
            path="/api/v1/users/oauth",
            method="POST",
            data={"email": email},
        ).json()

    def __check_access(self):
        try:
            self.client.call_rest(path="/api/v1/users", method="GET", data={})
        except Exception as e:
            pprint(e)
