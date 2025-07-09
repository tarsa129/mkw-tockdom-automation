import csv

def write_csv_file(file, csv_info):
    if not isinstance(csv_info[0], dict):
        csv_info = [vars(entry) for entry in csv_info]

    if not file:
        raise RuntimeError("File {} must be defined".format(file))

    with open(file, "w", newline='', encoding="utf8") as f:
        w = csv.DictWriter(f, csv_info[0].keys())
        w.writeheader()
        w.writerows(csv_info)
