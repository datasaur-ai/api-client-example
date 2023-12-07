from src.helpers import get_access_token, call_graphql, get_operations


class Team:
    def __init__(
        self, base_url: str, client_id: str, client_secret: str, verbose: bool
    ):
        self.base_url = base_url
        self.graphql_url = f"{base_url}/graphql"
        self.client_id = client_id
        self.client_secret = client_secret
        self.verbose = verbose

    def fetch(self):
        team_query = get_operations("src/teams/get_all_teams.json")
        return self.__call_graphql(team_query)

    def __call_graphql(self, data):
        token = get_access_token(
            self.client_id, self.client_secret, self.base_url, verbose=self.verbose
        )
        headers = {"Authorization": f"Bearer {token}"}
        return call_graphql(self.graphql_url, headers, data, self.verbose)
