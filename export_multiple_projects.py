import fire
import os

from get_projects import get_projects
from export import export_project


def export_multiple_projects(base_url, client_id, client_secret, export_file_name, export_format, output_dir):
    projects = get_projects(base_url, client_id, client_secret)

    for project in projects:
        project_id = project["id"]
        project_name = project["name"]
        export_name = "-".join([project_id, project_name, export_file_name])
        export_project(base_url, client_id, client_secret, project_id, export_name, export_format, output_dir)

    return "Success exporting the projects. Output files in " + output_dir


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    fire.Fire(export_multiple_projects)