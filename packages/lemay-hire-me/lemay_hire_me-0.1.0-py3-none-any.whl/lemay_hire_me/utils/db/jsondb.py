import json
import os
from pathlib import Path


class JSONDatabase:
    def __init__(self, destination_path: Path):
        stuff_folder_name = '.interview'
        config_file_name = 'config.json'
        stuff_folder_path = Path(destination_path / stuff_folder_name)
        stuff_folder_path.mkdir(parents=True, exist_ok=True)

        self.config_file_path = Path(destination_path / stuff_folder_name / config_file_name)
        if not os.path.exists(self.config_file_path):
            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
            with open(self.config_file_path, 'w') as f:
                json.dump({}, f, indent=4)

    def _load_data(self):
        with open(self.config_file_path, 'r') as f:
            return json.load(f)

    def _save_data(self, data):
        with open(self.config_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def create_new_record(self, key, value):
        data = self._load_data()
        if key in data:
            raise KeyError(f"Record with key '{key}' already exists")
        data[key] = value
        self._save_data(data)

    def read_record(self, key):
        data = self._load_data()
        return data.get(key)

    def update_record(self, key, value):
        data = self._load_data()
        if key not in data:
            raise KeyError(f"Record with key '{key}' does not exist")
        data[key] = value
        self._save_data(data)

    def delete_record(self, key):
        data = self._load_data()
        if key not in data:
            raise KeyError(f"Record with key '{key}' does not exist")
        del data[key]
        self._save_data(data)

    def flatten_data(self, prefix=''):
        data = self._load_data()
        flattened = {}
        for key, value in data.items():
            new_key = prefix + '.' + key if prefix else key
            if isinstance(value, dict):
                flattened.update(data(value, new_key))
            else:
                flattened[new_key] = value
        return flattened
