import json


def js_write(data):
    with open("options.json", "w") as write_file:
        json.dump(data, write_file)


def js_read():
    with open("options.json", "r") as read_file:
        return json.load(read_file)
