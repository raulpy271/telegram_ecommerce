from json import load


def load_json_file(path):
    with open(path, "r") as json_string:
        return load(json_string)


