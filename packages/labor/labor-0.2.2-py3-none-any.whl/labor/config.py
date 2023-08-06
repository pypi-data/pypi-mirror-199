import json
import os


def get_config_path():
    # Current path
    path = os.path.dirname(os.path.abspath(__file__))
    # New path
    return os.path.join(path, 'config.json')


def write(json_file):
    config_path = get_config_path()

    with open(config_path, 'w') as file:
        json.dump(json_file, file)


def load():
    config_path = get_config_path()

    with open(config_path, 'r') as file:
        return json.load(file)
