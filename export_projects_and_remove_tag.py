import fire
import os

from get_projects import get_projects
from export import export_project
from update_project_tags import remove_project_tags

from toolbox.get_operations import get_operations


def export_projects_and_remove_tag(base_url, client_id, client_secret, export_file_name, export_format, output_dir):
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