import json


def js_write(data):
    try:
        with open("options.json", "w") as write_file:
            json.dump(data, write_file)
    except FileNotFoundError:
        pass


def js_read():
    try:
        with open("options.json", "r") as read_file:
            return json.load(read_file)
    except FileNotFoundError:
        return {}
