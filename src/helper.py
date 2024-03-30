import json


# load value from json file with given key
def load_value_from_json_file(key):
    with open('config.json', 'r') as f:
        data = json.load(f)

    if key not in data:
        return None

    return data[key]
