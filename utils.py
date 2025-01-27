import json


def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {file_path}.")
    return None


def gamedata_to_json():
    pass
