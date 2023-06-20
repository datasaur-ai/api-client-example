import json
import yaml
import string
import random
import time
from fire import Fire

from logger import logger

import shutil

# Specify the source file path
source_path = "path/to/source/file.txt"

# Specify the destination file path
destination_path = "path/to/destination/file.txt"


def random_string():
    characters = string.ascii_letters + string.digits
    random_chars = random.choices(characters, k=4)
    random_string = "".join(random_chars)
    return random_string


def get_project_name(cohort_name):
    cohort_name = cohort_name.replace(" ", "-")
    project_name = f"{cohort_name}-{random_string()}"
    logger.info(f"PROJECT NAME: {project_name}")
    return project_name


def read_config_file(path):
    with open(path, "r") as stream:
        res = yaml.safe_load(stream)
    stream.close()
    return res


def main(
    document_path: str,
    project_template: str,
    positive_label: str,
    negative_label: str,
    cohort_name: str = "none",
):
    # Read the JSON file
    with open(project_template, "r") as file:
        data = json.load(file)

    # # Read CONFIG
    # CONFIG = read_config_file(global_config_path)
    logger.info(f"COHORT NAME: {cohort_name}")
    logger.info(f"POSITIVE LABEL: {positive_label}")
    logger.info(f"NEGATIVE LABEL: {negative_label}")

    new_document_path = f'./datasaur-api-client/create-project-async/documents/{document_path.split("/")[-1]}'
    # Move the file
    shutil.move(document_path, new_document_path)

    # Update the values for the specified keys
    data["variables"]["input"]["name"] = get_project_name(cohort_name)
    data["variables"]["input"]["documents"][0]["fileName"] = new_document_path.split(
        "/"
    )[-1]
    data["variables"]["input"]["documents"][0]["name"] = new_document_path.split("/")[
        -1
    ]
    for i in data["variables"]["input"]["documentAssignments"]:
        i["documents"][0]["fileName"] = new_document_path.split("/")[-1]
    data["variables"]["input"]["documents"][0]["file"]["path"] = new_document_path
    data["variables"]["input"]["documents"][0]["settings"]["questions"][0][
        "label"
    ] = f"Does this post reflect {positive_label} opinion?"
    data["variables"]["input"]["documents"][0]["settings"]["questions"][0]["config"][
        "options"
    ][0]["label"] = positive_label
    data["variables"]["input"]["documents"][0]["settings"]["questions"][0]["config"][
        "options"
    ][1]["label"] = negative_label
    # Write the updated data back to the JSON file
    with open(
        "./datasaur-api-client/create-project-async/project_configuration.json",
        "w",
    ) as file:
        # with open(project_configuration_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    logger.info("Datasaur Project Configuration")
    start_time = time.time()
    Fire(main)
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    logger.info(f"Project configuration elapsed time: {elapsed_time:.2f} seconds")
