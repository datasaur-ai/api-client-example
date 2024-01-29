import logging
from helpers.rest_client import AdminRESTClient
from models import LabelerAssignment, User
from src.helpers import load_jsonc
from user.oauth import UserOAuthCredentials


def load_labelers_and_populate_credentials(labelers_file: str, config: dict):
    data_from_file = load_jsonc(labelers_file)
    labeler_with_credentials = []
    rest_client = AdminRESTClient(
        base_url=config["base_url"],
        admin_client_id=config["client_id"],
        admin_client_secret=config["client_secret"],
    )

    for labeler in data_from_file["labelers"]:
        if (labeler["client_id"] is None) or (labeler["client_secret"] is None):
            logging.warning(
                f"missing client_id or client_secret for {labeler['email']}, generating new credential for them"
            )
            credential = UserOAuthCredentials(
                admin_client=rest_client
            ).generate_oauth_credentials(email=labeler["email"])

            labeler_with_credentials.append(
                {
                    **labeler,
                    "client_id": credential["client_id"],
                    "client_secret": credential["client_secret"],
                }
            )
        else:
            labeler_with_credentials.append(labeler)

    return labeler_with_credentials
