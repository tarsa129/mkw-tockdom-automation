import os.path
import csv

def read_csv_file(file):
    if file is None or not os.path.exists(file):
        raise RuntimeError("File {} does not exist.".format(file))

    commands = {}

    with open(file, newline='', encoding="utf8") as f:
        commands = [{k:v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

    return commands