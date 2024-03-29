import fire
import os

from export import export_project
from get_projects import get_projects
from remove_project_tags import remove_project_tags

from toolbox.get_operations import get_operations


def export_projects_and_remove_tag(base_url, client_id, client_secret, export_file_name, export_format, output_dir):
    """Export projects with a specific tag and subsequently remove the tag from the exported projects

    Processes:
    1. Get projects by tag
    2. Export the selected projects
    3. Remove tag from those projects
    """
    operations = get_operations("get_projects.json")
    tags = operations["variables"]["input"]["filter"]["tags"]

    projects = get_projects(base_url, client_id, client_secret)
    if len(projects) == 0:
        return "No projects found."

    for project in projects:
        project_id = project["id"]
        exported_project_file_name = "-".join([export_file_name, project_id])
        export_project(base_url, client_id, client_secret, project_id, exported_project_file_name, export_format, output_dir)
        remove_project_tags(base_url, client_id, client_secret, project_id, tags)

    return "Success exporting the projects. Output files in " + output_dir


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    fire.Fire(export_projects_and_remove_tag)
