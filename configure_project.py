import json
import yaml
import time
from fire import Fire

from logger import logger

import shutil

# Specify the source file path
source_path = "path/to/source/file.txt"

# Specify the destination file path
destination_path = "path/to/destination/file.txt"


def get_project_name(CONFIG):
    cohort_name = CONFIG["cohort_name"].replace(" ", "-")
    # project_name = f"{cohort_name}-0000"
    project_name = f"{cohort_name}-XXXX"
    return project_name


def read_config_file(path):
    with open(path, "r") as stream:
        res = yaml.safe_load(stream)
    stream.close()
    return res


def main(document_path: str, project_configuration_path: str, global_config_path: str):
    # Read the JSON file
    with open(project_configuration_path, "r") as file:
        data = json.load(file)

    # Read CONFIG
    CONFIG = read_config_file(global_config_path)

    new_document_path = f'./datasaur-api-client/create-project-async/documents/{document_path.split("/")[-1]}'
    # Move the file
    shutil.move(document_path, new_document_path)

    # Update the values for the specified keys
    data["variables"]["input"]["name"] = get_project_name(CONFIG)
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
    ] = f"Does this post reflect {CONFIG['positive_label']} opinion?"
    data["variables"]["input"]["documents"][0]["settings"]["questions"][0]["config"][
        "options"
    ][0]["label"] = CONFIG["positive_label"]
    data["variables"]["input"]["documents"][0]["settings"]["questions"][0]["config"][
        "options"
    ][0]["label"] = CONFIG["negative_label"]
    # Write the updated data back to the JSON file
    with open(
        "/root/datasaur-api-client/create-project-async/project_configuratioTEST.json",
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
