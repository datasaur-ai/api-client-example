import logging
from src.helpers.rest_client import AdminRESTClient
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

    labelers_need_credentials = []

    for labeler in data_from_file["labelers"]:
        if (labeler["client_id"] is None) or (labeler["client_secret"] is None):
            logging.warning(
                f"missing client_id or client_secret for {labeler['email']}, generating new credential for them"
            )
            labelers_need_credentials.append(labeler)
        else:
            labeler_with_credentials.append(labeler)

    if (len(labelers_need_credentials)) > 0:
        credentials = UserOAuthCredentials(rest_client).generate_oauth_credentials(
            emails=[labeler["email"] for labeler in labelers_need_credentials]
        )

        map_of_credentials = {
            credential["email"]: {
                "client_id": credential["client_id"],
                "client_secret": credential["client_secret"],
            }
            for credential in credentials
        }

        for labeler in labelers_need_credentials:
            try:
                labeler["client_id"] = map_of_credentials[labeler["email"]]["client_id"]
                labeler["client_secret"] = map_of_credentials[labeler["email"]][
                    "client_secret"
                ]
                labeler_with_credentials.append(labeler)
            except Exception as e:
                logging.error(
                    f"failed to generate credential for {labeler['email']}, {e}"
                )

    return labeler_with_credentials
