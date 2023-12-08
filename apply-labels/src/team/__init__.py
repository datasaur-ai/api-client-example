from src.helpers import GraphQLClient, get_operations


class Team:
    def __init__(self, client: GraphQLClient, base_url: str):
        self.base_url = base_url
        self.client = client

    def fetch(self):
        team_query = get_operations("src/team/get_all_teams.json")
        return self.client.call_graphql(team_query)
