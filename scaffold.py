#!/usr/bin/env python3
import os
import typer
import pathlib
from enum import Enum
from rich import print
from rich.table import Table
from rich.console import Console
from django.core.management import call_command

err_console = Console(stderr=True)


class ProjectType(str, Enum):
    vue_vite = 'vue_vite'


def ask_project_name():
    project_name = typer.prompt("Please enter the project name")
    print(f"Project name: {project_name}")
    return project_name


def choose_project_type():
    project_types = list(ProjectType)

    def get_choice():
        print("Please choose a project type:")
        for i, project_type in enumerate(project_types, 1):
            print(f"{i}. {project_type.value}")
        choice = typer.prompt("Enter the number of your choice", type=int)
        return choice

    while True:
        choice = get_choice()
        if 1 <= choice <= len(project_types):
            selected_type = project_types[choice - 1]
            print(f"You chose: {selected_type.value}")
            return selected_type
        else:
            print("Invalid choice. Please choose a number between 1 and 3.")


def ask_for_project_path():
    project_path = typer.prompt("Please enter the path for the project. If left blank, the project will be created in", default="./test/")
    print(f"Project path: {project_path}")
    return project_path


def perform_validation(project_name: str, project_type: str, output_path: str):
    directory_name = os.path.split(output_path.rstrip('/'))[1]
    if directory_name == project_name:
        err_console.print('Project name cannot be the same as the directory in your output path')
        raise typer.Exit(code=1)
    if output_path == './test/':
        typer.confirm('Custom output path was not provided. This will generate your project in ./test/. Continue?', abort=True)


def create_project_dir(project_name: str, base_path: str):
    print(f'Creating base directory for the {project_name} project at {base_path}')
    create_dir(base_path)


def create_dir(path: str):
    if os.path.exists(path):
        err_console.print(f'Output path already exists ({path}); please delete it first')
        raise typer.Exit(code=1)
    else:
        os.makedirs(path)


def create_project(project_name: str, project_type: ProjectType, output_path: str):
    current_path = pathlib.Path(__file__).parent.resolve()
    base_template_path = os.path.join(current_path, 'templates')
    match project_type:
        case ProjectType.vue_vite:
            template_path = os.path.join(base_template_path, 'vue-vite')
        case _:
            template_path = os.path.join(base_template_path, 'django-only')
    call_command('startproject', f'--template={template_path}',
                 '--name=Dockerfile,Dockerfile.prod,docker-compose.yml,README.md,.env,package.json,index.html,navbar.html',
                 '-e=sh', '-x=.git', '-x=bundles', '-x=node_modules', '-x=staticfiles', project_name, output_path)


def create_api_app(project_name: str, output_path: str):
    app_path = create_api_app_dir(project_name, output_path)
    call_command('startapp', f'{project_name}_api', app_path)
    create_blank_api_urls_py(app_path)


def create_api_app_dir(project_name: str, base_path: str) -> str:
    app_name = f'{project_name}_api'
    app_path = os.path.join(base_path, 'src', app_name)
    print(f'Creating {app_name} app...')
    create_dir(app_path)
    return app_path


def create_blank_api_urls_py(app_path: str):
    with open(os.path.join(app_path, 'urls.py'), 'w') as f:
        f.write('urlpatterns = []')


def post_create_checklist_table(project_type=ProjectType) -> Table:
    table = Table(title='Post-create checklist')
    table.add_column('Item', style='cyan')
    table.add_row('- Create a superuser for testing locally: "docker-compose exec api python manage.py createsuperuser"')
    table.add_row('- Generate unique secret keys for each deployment environment')
    match project_type:
        case ProjectType.vue_vite:
            table.add_row('- Review dependencies listed in package.json and requirements.txt, bumping up versions or removing altogether as needed')
            table.add_row('- Generate and commit a package-lock.json to include in the repo; e.g. docker-compose exec frontend npm i --package-lock-only')
        case _:
            table.add_row('- Review dependencies listed in requirements.txt, bumping up versions or removing altogether as needed')
    table.add_row('- "git init", set your upstream repository, and push your main branch up; e.g. git remote add origin git@github.com:... && git push')
    return table


def main():
    project_name = ask_project_name()
    project_type = choose_project_type()
    project_path = ask_for_project_path()
    perform_validation(project_name, project_type, project_path)
    create_project_dir(project_name, project_path)
    create_project(project_name, project_type, project_path)
    create_api_app(project_name, project_path)
    print('Done! 🎉🎉🎉')
    print(post_create_checklist_table(project_type))


if __name__ == '__main__':
    try:
        typer.run(main)
    except Exception as ex:
        err_console.print('Something went wrong. Try your command again after re-running init.sh.')
        raise ex
