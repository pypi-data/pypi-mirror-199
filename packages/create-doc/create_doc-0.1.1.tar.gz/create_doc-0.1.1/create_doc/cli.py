import click
import json
import os
from dotenv import load_dotenv
import create_doc.analyze_with_gpt as gpt
import create_doc.analyze_module_dependencies as analyze_module_dependencies

@click.group()
def cli():
    pass


@cli.command()
def init():
    """Initialize the application"""
    click.echo('Initializing the application...')

    if os.path.isfile('./.create_doc.json'):
        confirm_overwrite = input('.create_doc.json already exists. Do you want to overwrite it? (y/n): ')
        if confirm_overwrite.lower() != 'y':
            exit()
    json_data = {
        "project_root_path": ".",
        "project_forms_paths": ["./src"],
        "project_webapp_paths": ["./src"],
        "output_path": "./docs",
        "gpt_model_id": "gpt-3.5-turbo",
        "gpt_model_token_limit": 4096,
        "gpt_prompt_html": "You are a technical writer of user manuals." +
                       "You are working on a project to create application documentation from HTML code." +
                       "The result is in markdown format." +
                       "The first part of the documentation should contain a concise " +
                       "description of the HTML page from a user perspective. " +
                       "The second part should contain instructions for using " +
                       "the HTML page. " +
                       "The third part should contain a technical description " +
                       "of the page, including function calls, and which classes "+
                       "are used to define the layout of elements on the page. " +
                       "You should describe how the page works internally, " +
                       "and what happens in case of an error.",
        "gpt_skip_html_router_outlet": True,
        "html_router_outlet_message": "This page contains angular router-outlet tag. " +
                                      "This means that this page contains subcomponents.",
        "content_title": "Content",
    }
    with open('./.create_doc.json', 'w') as file:
        json.dump(json_data, file, indent=4)

    click.echo("Created file .create_doc.json.")
    click.echo("This file will be used to configure the project documentation generation.")
    click.echo("Edit the file to your liking.")

    check_openapi_key()

    return 0


@cli.command()
def process_html():
    """Process HTML file"""
    click.echo('Processing html files...')
    check_openapi_key()
    config = get_config()
    gpt.init_env()
    # for all files in project forms paths
    for path in config['project_forms_paths']:
        gpt.analyze_html_files(config['project_root_path'], path, config['output_path'], config['gpt_model_id'],
                               config['gpt_model_token_limit'], config['gpt_prompt_html'],
                               config['gpt_skip_html_router_outlet'], config['html_router_outlet_message'],
                               config['content_title'])
    click.echo('Done processing html files')

@cli.command()
@click.argument('dependency', nargs=-1)
def process_dependencies(dependency):
    """Process application dependencies"""
    click.echo('Processing application dependencies...')
    config = get_config()
    project_directory_path = config['project_root_path']
    webapp_paths = config['project_forms_paths'][0]
    output_path = config['output_path']
    # for all paths in project webapp paths
    for path in config['project_webapp_paths']:
        analyze_module_dependencies.process_directory_dependencies(project_directory_path, path, output_path)

    click.echo('Done processing dependencies')



def read_config_file():
    with open('./.create_doc.json', 'r') as file:
        return json.load(file)


def get_config():
    config = read_config_file()

    # get current working directory
    cwd = os.getcwd()
    # get project root path
    project_root_path = config['project_root_path']
    # if project root path is not absolute, make it absolute
    if not os.path.isabs(project_root_path):
        project_root_path = os.path.join(cwd, project_root_path)
    # add project root path to config
    config['project_root_path'] = project_root_path
    # get project forms paths
    project_forms_paths = config['project_forms_paths']
    # if project forms paths are not absolute, make them absolute
    for i, path in enumerate(project_forms_paths):
        if not os.path.isabs(path):
            project_forms_paths[i] = os.path.join(cwd, path)
    # add project forms paths to config
    config['project_forms_paths'] = project_forms_paths
    # get project webapp paths
    project_webapp_paths = config['project_webapp_paths']
    # if project webapp paths are not absolute, make them absolute
    for i, path in enumerate(project_webapp_paths):
        if not os.path.isabs(path):
            project_webapp_paths[i] = os.path.join(cwd, path)
    # add project webapp paths to config
    config['project_webapp_paths'] = project_webapp_paths
    # get output path
    output_path = config['output_path']
    # if output path is not absolute, make it absolute
    if not os.path.isabs(output_path):
        output_path = os.path.join(cwd, output_path)
    # add output path to config
    config['output_path'] = output_path

    return config


def check_openapi_key():
    # read environment variable OPENAI_API_KEY


    load_dotenv()
    openapi_key = os.getenv('OPENAI_API_KEY')
    if not openapi_key:
        click.echo('OPENAI_API_KEY environment variable not set.')
        click.echo('Please set it to your OpenAPI key.')
        return False
    return True


if __name__ == '__main__':
    cli()
