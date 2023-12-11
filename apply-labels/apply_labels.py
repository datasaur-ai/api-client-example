import fire
from dotenv import load_dotenv

from src.entrypoint import check_login_and_teams, validate_project

load_dotenv()


if __name__ == "__main__":
    fire.Fire(
        {"check_teams": check_login_and_teams, "validate_project": validate_project}
    )
