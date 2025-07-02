import os.path
import csv

def write_csv_file(file, csv_info):
    if file is None:
        raise RuntimeError("File {} does not exist.".format(file))

    with open(file, "w", newline='', encoding="utf8") as f:
        w = csv.DictWriter(f, csv_info[0].keys())
        w.writeheader()
        w.writerows(csv_info)
