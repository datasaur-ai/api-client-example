from http import HTTPStatus
from pprint import pprint
from src.helpers.rest_client import AdminRESTClient


class UserOAuthCredentials:
    def __init__(self, admin_client: AdminRESTClient):
        self.client = admin_client
        self.__check_access()

    def generate_oauth_credentials(self, emails: list[str]):
        response = self.client.call_rest(
            path="/api/v1/users/oauth",
            method="POST",
            data={"emails": emails},
        )

        if response.status_code == HTTPStatus.OK:
            return response.json()

        raise Exception(
            "failed to generate OAuth credentials",
            {"status": response.status_code, "text": response.text},
        )

    def __check_access(self):
        try:
            self.client.call_rest(path="/api/v1/users", method="GET", data={})
        except Exception as e:
            pprint(e)
            raise e
