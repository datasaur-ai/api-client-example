import logging

from src.user.oauth import UserOAuthCredentials

from ..admin_rest_client import AdminRESTClient
from ..load_jsonc import load_jsonc
from ..loggable import loggable_with_args


@loggable_with_args
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
        labeler_client_id = labeler.get("client_id", None)
        labeler_client_secret = labeler.get("client_secret", None)
        if is_none_or_empty(labeler_client_id, labeler_client_secret):
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

        credentials_by_email = {
            credential["email"]: {
                "client_id": credential["clientId"],
                "client_secret": credential["clientSecret"],
            }
            for credential in credentials
        }

        for labeler in labelers_need_credentials:
            try:
                labeler["client_id"] = credentials_by_email[labeler["email"]][
                    "client_id"
                ]
                labeler["client_secret"] = credentials_by_email[labeler["email"]][
                    "client_secret"
                ]
                labeler_with_credentials.append(labeler)
            except Exception as e:
                logging.error(
                    f"failed to generate credential for {labeler['email']}, omitting them from the list of labelers",
                    e,
                )

    return labeler_with_credentials


def is_none_or_empty(*args):
    return any(arg is None or arg == "" for arg in args)
