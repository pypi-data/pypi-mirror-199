import platform
from datetime import datetime
from pathlib import Path

import os
import git
from git import GitCommandError

import hashlib

from lemay_hire_me.utils.db.jsondb import JSONDatabase


def compare_files_changes(folder_path: Path):
    folder_hashes = {}
    for root, dirs, filenames in os.walk(folder_path):
        json_files = [filename for filename in filenames if filename.endswith('.json')]
        for json_file in json_files:
            file_path = os.path.join(root, json_file)
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            folder_path = os.path.relpath(root, folder_path)
            folder_hashes.setdefault(folder_path, []).append(file_hash)
    return folder_hashes


def clone_assignment_git(git_url: str, destination_folder: Path, save_info_to: JSONDatabase):
    assignment_folder_name = 'assignment'
    assignment_folder_path = Path(destination_folder / assignment_folder_name)
    assignment_folder_path.mkdir(exist_ok=True, parents=True)

    try:
        git.Repo.clone_from(git_url, assignment_folder_path.absolute())
    except GitCommandError:
        pass

    files_hash = compare_files_changes(destination_folder)
    save_info_to.create_new_record('assignment_absolut_path', assignment_folder_path.as_posix())
    save_info_to.create_new_record('json_file_changes', files_hash)


def list_folders(path):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]


def list_files(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def platform_information():
    return {
        'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'os_name': platform.system(),
        'pyinfo': {
            'py_version': platform.python_version(),
            'py_impl': platform.python_implementation()
        }
    }
