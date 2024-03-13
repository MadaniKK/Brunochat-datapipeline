import json


def load_data_from_json(filepath):
    with open(filepath, "r") as file:
        links_data_collection = json.load(file)
    return links_data_collection
