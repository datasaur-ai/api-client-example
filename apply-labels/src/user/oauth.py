from http import HTTPStatus

from src.helpers import AdminRESTClient, loggable_debug

_USER_PREFIX = "/api/v1/users"


class UserOAuthCredentials:
    def __init__(self, admin_client: AdminRESTClient):
        self.client = admin_client
        self.__check_access()

    @loggable_debug
    def generate_oauth_credentials(self, emails: list[str]):
        response = self.client.call_rest(
            path=f"{_USER_PREFIX}/oauth",
            method="POST",
            data={"emails": emails},
        )

        if response.status_code == HTTPStatus.OK:
            return response.json()["data"]

        raise Exception(
            "failed to generate OAuth credentials",
            {"status": response.status_code, "text": response.text},
        )

    def __check_access(self):
        response = self.client.call_rest(path=_USER_PREFIX, method="GET", data={})
        if response.status_code == HTTPStatus.OK:
            return True
        else:
            raise Exception(
                f"unable to access {_USER_PREFIX}, ensure your credentials in .env is from a super-admin user",
                {"status": response.status_code, "text": response.text},
            )
