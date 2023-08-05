import os
from pathlib import Path

import typer

from lemay_hire_me.utils.styled_text import styled_ascii_text


class FolderCreator:
    def __init__(self):
        pass

    @staticmethod
    def create_project_folder(ACTUAL_WORKING_DIR):
        project_workspace_path = Path(ACTUAL_WORKING_DIR / "LemayProjectWorkspace")
        project_workspace_path.mkdir(exist_ok=True)

        return project_workspace_path.absolute()

    def return_stuff_folder_path(self):
        pass