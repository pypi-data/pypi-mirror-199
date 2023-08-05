from __future__ import annotations

import json
from typing import Optional

import requests
from requests import HTTPError

from rich import print_json


def find_value(nested_dict, key):
    """
    Recursively search for a value in a nested dictionary using a given key.

    Parameters:
        nested_dict (dict): The nested dictionary to search.
        key (str): The key to search for in the dictionary.

    Returns:
        The value associated with the key, or None if the key is not found.
    """
    for k, v in nested_dict.items():
        if k == key:
            return v
        elif isinstance(v, dict):
            result = find_value(v, key)
            if result is not None:
                return result
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    result = find_value(item, key)
                    if result is not None:
                        return result
    return None


def search_dict_by_key_value(nested_dict, key, value):
    """
    Search a list of dictionaries nested within a dictionary by a given key-value pair,
    and return the dictionary that contains that key-value pair.

    Parameters:
        nested_dict (dict): The nested dictionary to search.
        key (str): The key to search for in the dictionaries within the nested dictionary.
        value (str): The value to search for in the dictionaries within the nested dictionary.

    Returns:
        The dictionary that contains the given key-value pair, or None if it is not found.
    """
    for item in nested_dict:
        if item.get(key) == value:
            return item
    return None


def path_to_files(string_list, substring) -> Optional[str | None]:
    for string in string_list:
        if substring in string:
            return string
    return None


def send_data_to_api(assignment_data: list[str], collected_data: dict):
    headers = {
        'accept': 'application/json',
    }

    params = dict()
    params.update(collected_data)

    assignment_answers_collected = {
        'part_1_Q1': '',
        'part_1_Q2': '',
        'part_1_Q3': '',
        'part_1_Q4': '',
        'part_1_Q5': '',
        'part_1_Q6': '',
        'part_2': '',
    }
    files = {
        'part_1_writing_sample': open(path_to_files(assignment_data, "writing_sample"), 'rb'),
        'part_3': open(path_to_files(assignment_data, "third_part"), 'rb'),
    }
    for file_path in assignment_data:
        if file_path.endswith(".json"):
            # del assignment_data[idx]
            with open(file_path, 'r') as file:
                answer_data = json.load(file)
                for task_number in assignment_answers_collected.keys():
                    returned_value = search_dict_by_key_value(answer_data['answers'], 'task_number', task_number)
                    if returned_value:
                        assignment_answers_collected[task_number] = returned_value['source']

    params.update(assignment_answers_collected)
    # print_json(data=params)

    try:
        response = requests.post('https://applications.lemay.ai/submit', params=params,
                                 headers=headers, files=files, verify=False)
        response.raise_for_status()
        print(response.text)
    except HTTPError as e:
        print(f'HTTP error: {e}')
    except requests.exceptions.RequestException as e:
        print(f'Request error: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')
