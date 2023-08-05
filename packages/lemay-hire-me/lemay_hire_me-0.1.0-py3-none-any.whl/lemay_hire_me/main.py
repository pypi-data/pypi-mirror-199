import os
import typer

from lemay_hire_me.schemas import poll

from pathlib import Path

from rich.console import Console
from rich.table import Table

from lemay_hire_me.utils.api import send_data_to_api
from lemay_hire_me.utils.config.config import FolderCreator
from lemay_hire_me.utils.db.jsondb import JSONDatabase
from lemay_hire_me.utils.depend_files import platform_information, clone_assignment_git
from lemay_hire_me.utils.styled_text import styled_ascii_text, field_name_format

app = typer.Typer()
console = Console()

ACTUAL_WORKING_DIR = Path.cwd()
folder_creator = FolderCreator()

# db = JSONDatabase(destination_path=Path(Path.cwd() / 'LemayProjectWorkspace'))


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def init():
    """
    Initialization command. Requests the user's personal data and provides the task.
    """
    styled_ascii_text("Lemay AI", color="blue", figlet=True)
    styled_ascii_text("Hiring CLI App", "green")

    is_folder_empty = len(os.listdir(ACTUAL_WORKING_DIR)) == 0  # Create if folder is empty

    WORKSPACE_PATH = None
    if is_folder_empty:
        styled_ascii_text("This directory is empty. Creating project workspace.", color='green')
        WORKSPACE_PATH = folder_creator.create_project_folder(ACTUAL_WORKING_DIR)
    else:
        is_not_empty_folder_action = typer.confirm(
            "Actual folder is not empty. Are you sure you want to create a folder here and continue?")

        if not is_not_empty_folder_action:
            styled_ascii_text('Please, change or create empty folder and run init command!', "red")
            raise typer.Abort()
        else:
            WORKSPACE_PATH = folder_creator.create_project_folder(ACTUAL_WORKING_DIR)
            styled_ascii_text("New folder named 'LemayProjectWorkspace' created in the current directory!", "green")

    db = JSONDatabase(destination_path=WORKSPACE_PATH)  # Define ops with config.json
    db.create_new_record('workspace_absolut_path', WORKSPACE_PATH.as_posix())

    styled_ascii_text("To start, please provide your personal details and salary expectations", color="red")
    personal_information_poll = poll.ask_personal_info()
    del personal_information_poll['send']

    db.create_new_record("personal_data", personal_information_poll)
    db.create_new_record("additional_data", platform_information())

    styled_ascii_text(
        "Your personal data has been saved in local storage. After completing the task, use the command 'lemay-hire-me push'",
        color='green')

    clone_assignment_git("https://github.com/belochenko/fizzbuzz_test", WORKSPACE_PATH,
                         save_info_to=db)  # TODO: Repo URL

    styled_ascii_text("Cloning your assignment", color='green')


@app.command()
def update(
        full_name: str = typer.Option(None, "--full_name", "-n"),
        email: str = typer.Option(None, "--email", "-e"),
        linkedin_profile: str = typer.Option(None, "--linkedin_profile", "-l"),
        salary_range: str = typer.Option(None, "--salary_range", "-s")
):
    if full_name is None and email is None and linkedin_profile is None and salary_range is None:
        typer.echo("Please specify the data you wish to update")
        return

    typer.echo(f"Updating with the following details:")
    to_update = dict()
    if full_name:
        to_update.update({"full_name": full_name})
    if email:
        to_update.update({"email": email})
    if linkedin_profile:
        to_update.update({"linkedin_profile_link": linkedin_profile})
    if salary_range:
        to_update.update({"salary": salary_range})


@app.command()
def push():
    """
    The command is intended to send data after the tasks are done.
    """

    not_allowed_files_to_push = ['README.md']
    allowed_folder_to_list = ['first_part', 'second_part', 'third_part', 'writing_sample']

    db = JSONDatabase(destination_path=Path(Path.cwd() / 'LemayProjectWorkspace'))

    x = db.read_record("assignment_absolut_path")
    assignment_path = Path(x)

    def is_file_allowed(file_path):
        file_name = os.path.basename(file_path)
        return file_name not in not_allowed_files_to_push

    # Function to parse through allowed folders and return list of files
    def get_allowed_files():
        allowed_files = []
        for folder in allowed_folder_to_list:
            for root, dirs, files in os.walk(assignment_path / folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    if is_file_allowed(file_path):
                        allowed_files.append(os.path.abspath(file_path))
        return allowed_files

    confirmation = typer.confirm(
        "Do you confirm that the task has been completed and are you ready to submit it?")

    if confirmation:
        allowed_files = get_allowed_files()
        send_data_to_api(allowed_files, db.read_record('personal_data'))
    else:
        styled_ascii_text("Take your time and when you're ready type 'lemay-hire-me push'", color='green')
        raise typer.Abort()


if __name__ == '__main__':
    push()
